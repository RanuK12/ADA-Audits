#!/usr/bin/env python3
"""Genera follow-ups para leads con PDF ya enviado.

Busca en leads_us_curados.json los leads marcados como 'contactado_campana_current' 
y con PDF existente en output/, genera follow-up emails y los añade al outbox.
"""
import csv
import json
import re
from datetime import datetime, timedelta
from pathlib import Path

ROOT = Path('/Users/emilioranucoli/Desktop/Oficina_Ranuk/ADA-AUDITS')
OUTBOX = ROOT / 'prospectos' / 'outbox'
INDEX = OUTBOX / 'index.json'
LEADS_CURATED = Path.home() / '.ranukita' / 'ada_outreach' / 'leads_us_curados.json'

def load_leads_curated():
    if LEADS_CURATED.exists():
        return json.load(open(LEADS_CURATED))
    return {"leads": []}

def load_index():
    if INDEX.exists():
        return json.load(open(INDEX))
    return []

def save_index(data):
    json.dump(data, open(INDEX, 'w'), indent=2)

def generate_follow_up(lead, follow_type='followup'):
    # Extract first name from email if possible
    first_name = lead.get('first_name')
    if not first_name:
        # Try to extract from email (alice@... → Alice)
        email_user = lead['email'].split('@')[0]
        if '.' in email_user:
            first_name = email_user.split('.')[0].capitalize()
        elif len(email_user) >= 3:
            first_name = email_user.capitalize()
        else:
            first_name = "there"
    
    # Template for follow-up
    templates = {
        'followup': {
            'subject': f'following up on {lead["domain"]}',
            'body': f"Hi {first_name},\n\nJust checking in — did you get my note about the accessibility issues on {lead['domain']} that put you at ADA Title III risk?\n\nThe three most critical issues are still unaddressed:\n\n1. {lead.get('top_issue_1', 'color contrast issues')}\n\n2. {lead.get('top_issue_2', 'missing alt text')}\n\n3. {lead.get('top_issue_3', 'form label issues')}\n\nI've helped similar businesses fix these exact issues. If you'd like the free audit report (no strings), just reply and I'll send it over.\n\n— Emilio Ranucoli\nSystems Engineer — accessibility & compliance audits\nranuk.dev  |  ranucoliemilio@gmail.com"
        },
        'last': {
            'subject': f'last note about {lead["domain"]}',
            'body': f"Hi {first_name},\n\nThis is my last attempt to reach you. The accessibility issues on {lead['domain']} that put you at ADA Title III risk are still present and carry legal exposure.\n\nThe three most critical issues remain:\n\n1. {lead.get('top_issue_1', 'color contrast issues')}\n\n2. {lead.get('top_issue_2', 'missing alt text')}\n\n3. {lead.get('top_issue_3', 'form label issues')}\n\nI'll be focusing on other businesses this week, but if you change your mind about the free audit report, you can reach me at ranucoliemilio@gmail.com.\n\nWishing you the best with your practice.\n\n— Emilio Ranucoli\nSystems Engineer — accessibility & compliance audits\nranuk.dev  |  ranucoliemilio@gmail.com"
        }
    }
    
    if follow_type not in templates:
        return None
    
    template = templates[follow_type]
    return {
        'url': f'https://{lead["domain"]}',
        'domain': lead['domain'],
        'business_name': lead['name'],
        'to': lead['email'],
        'subject': template['subject'],
        'first_name': first_name,
        'body': template['body'],
        'status': 'pending',
        'created': datetime.now().isoformat(),
        'filename': f"followup-{lead['domain'].replace('.','-')}.txt",
        'follow_type': follow_type,
        'original_contact': lead.get('fecha_envio_t1', 'unknown')
    }

def find_pdf_for_lead(lead, existing_pdfs):
    """Find matching PDF for a lead by fuzzy-matching name/domain against existing PDF filenames."""
    name = lead['name'].lower()
    domain = lead['domain'].lower()
    
    for pdf in existing_pdfs:
        pdf_name = pdf.stem.lower()  # e.g. 'ADA_Audit_Park_Slope_Taxes'
        pdf_name = pdf_name.replace('ada_audit_', '')
        
        # Try matching: check if key business name words appear in the PDF name
        # Extract key words from business name (skip common words)
        name_words = set(re.sub(r'[^a-z0-9\s]', ' ', name).split())
        pdf_words = set(re.sub(r'[^a-z0-9\s]', ' ', pdf_name).split())
        
        # If significant overlap, it's a match
        if len(name_words & pdf_words) >= 2:
            return pdf
        
        # Also try domain-based match
        domain_key = domain.split('.')[0]
        if domain_key in pdf_name:
            return pdf
    
    return None

def main():
    # Load curated leads
    curated = load_leads_curated()
    index = load_index()
    
    # Pre-scan all existing PDFs
    output_dir = ROOT / 'output'
    existing_pdfs = list(output_dir.glob('ADA_Audit_*.pdf'))
    
    # Find leads that were contacted in campaign and have PDF
    candidates = []
    for lead in curated['leads']:
        if (lead.get('contactado_campana_actual') and 
            lead.get('fecha_envio_t1')):
            
            if find_pdf_for_lead(lead, existing_pdfs):
                candidates.append(lead)
    
    if not candidates:
        print('✅ no hay leads con PDF y contacto previo')
        return
    
    # Generate follow-ups
    new_entries = []
    for lead in candidates:
        # Determine follow-up type based on when it was sent
        contact_date = datetime.fromisoformat(lead['fecha_envio_t1'].replace('Z', '+00:00'))
        days_ago = (datetime.now(contact_date.tzinfo) - contact_date).days
        
        if days_ago < 3:
            continue  # too early
        elif days_ago < 7:
            follow_type = 'followup'
        else:
            follow_type = 'last'
        
        entry = generate_follow_up(lead, follow_type)
        if entry:
            new_entries.append(entry)
    
    # Add to index
    if new_entries:
        max_n = max([e['n'] for e in index]) if index else 0
        for entry in new_entries:
            max_n += 1
            entry['n'] = max_n
            entry['filename'] = f"{max_n}-{entry['filename']}"
            index.append(entry)
        
        save_index(index)
        print(f'✅ añadidos {len(new_entries)} follow-ups al outbox')
    else:
        print('✅ no hay follow-ups que generar')

if __name__ == '__main__':
    main()
