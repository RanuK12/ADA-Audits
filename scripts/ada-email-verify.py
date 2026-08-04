#!/usr/bin/env python3
"""
Verificación de emails para ADA Audits con rk_email_verify.
Filtra emails inválidos antes de enviar para no quemar reputación.
Uso: ada-email-verify.py --leads leads.csv --out verified-leads.csv
"""
import csv
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LEADS = ROOT / "prospectos" / "leads.csv"
OUTBOX = ROOT / "prospectos" / "outbox"
INDEX = OUTBOX / "index.json"
VERIFIED_LEADS = ROOT / "prospectos" / "verified-leads.csv"

def load_leads():
    """Carga emails desde valid_emails.txt"""
    valid_emails_file = ROOT / "outbox" / "valid_emails.txt"
    with open(valid_emails_file) as f:
        emails = [line.strip() for line in f if line.strip()]
    
    # Convertir emails a formato lead
    leads = []
    for email in emails:
        lead = {
            'owner_email': email,
            'domain': email.split('@')[1] if '@' in email else '',
            'business_name': '',
            'owner_name': '',
            'city': '',
            'state': '',
            'industry': '',
            'scan_score': 0,
            'critical_count': 0,
            'top_issue_1': '',
            'top_issue_2': '',
            'top_issue_3': '',
            'email_sent_date': '',
            'replied': False,
            'closed': False,
            'amount_usd': 0,
            'notes': ''
        }
        leads.append(lead)
    
    return leads

def verify_email(email):
    """Verifica email usando rk_email_verify"""
    try:
        cmd = [
            "python3",
            "/Users/emilioranucoli/Apps/ranukita-bridge/scripts/rk_email_verify.py",
            email
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            try:
                resp = json.loads(result.stdout.strip())
                # Solo consideramos válidos los emails de persona ('real')
                if resp.get('status') == 'real':
                    return True, resp
                return False, resp
            except:
                return False, {"error": "parse_failed"}
        else:
            return False, {"error": result.stderr.strip()}
    except Exception as e:
        return False, {"error": str(e)}

def main():
    leads = load_leads()
    verified = []
    rejected = []
    
    print(f"🔍 Verificando {len(leads)} emails...")
    
    for lead in leads:
        if not lead.get('owner_email'):
            continue
            
        email = lead['owner_email']
        is_valid, info = verify_email(email)
        
        if is_valid:
            verified.append(lead)
            print(f"✅ {email} - válido")
        else:
            rejected.append({
                'email': email,
                'reason': info.get('error', 'unknown'),
                'lead': lead
            })
            print(f"❌ {email} - {info.get('error', 'unknown')}")
    
    # Guardar leads verificados
    if verified:
        with open(VERIFIED_LEADS, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=leads[0].keys())
            writer.writeheader()
            writer.writerows(verified)
        print(f"✅ Guardados {len(verified)} leads verificados en verified-leads.csv")
    
    # Guardar rechazados para análisis
    if rejected:
        with open(VERIFIED_LEADS.parent / 'rejected-emails.json', 'w') as f:
            json.dump(rejected, f, indent=2)
        print(f"❌ Rechazados {len(rejected)} emails (ver rejected-emails.json)")
    
    print(f"📊 Resumen: {len(verified)} válidos, {len(rejected)} inválidos, {len(leads)} totales")

if __name__ == "__main__":
    main()