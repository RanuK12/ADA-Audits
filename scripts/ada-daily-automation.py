#!/usr/bin/env python3
"""
Automatización diaria para ADA Audits outreach.
Combina verificación, envío y seguimiento.
Uso: ada-daily-automation.py
"""
import csv
import json
import subprocess
import sys
import os
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parent.parent
LEADS = ROOT / "prospectos" / "leads_cleaned.csv"
TEMPLATE = ROOT / "outbox" / "email-template.html"
LOG_FILE = ROOT / "outbox" / "daily-log.json"

def load_leads():
    """Carga leads desde CSV"""
    with open(LEADS) as f:
        return list(csv.DictReader(f))

def log_action(action, details):
    """Registra acción en el log diario"""
    log_entry = {
        'timestamp': datetime.now().isoformat(),
        'action': action,
        'details': details
    }
    
    # Cargar log existente o crear nuevo
    if LOG_FILE.exists():
        with open(LOG_FILE) as f:
            log = json.load(f)
    else:
        log = []
    
    log.append(log_entry)
    
    # Guardar log (mantener solo últimos 30 días)
    with open(LOG_FILE, 'w') as f:
        json.dump(log[-30:], f, indent=2)

def verify_leads():
    """Verifica leads pendientes"""
    leads = load_leads()
    pending_leads = [lead for lead in leads if lead.get('status') == 'pending']
    
    log_action('verify_leads', {
        'total_leads': len(leads),
        'pending_leads': len(pending_leads)
    })
    
    return pending_leads

def send_outreach(leads_to_send):
    """Envía outreach a leads pendientes"""
    if not leads_to_send:
        log_action('send_outreach', {'status': 'no_leads'})
        return 0
    
    # Limitar a 5 emails por día para evitar límites
    daily_limit = min(5, len(leads_to_send))
    selected_leads = leads_to_send[:daily_limit]
    
    sent_count = 0
    
    for lead in selected_leads:
        email = lead.get('owner_email')
        if not email:
            continue
            
        # Preparar email
        business_name = lead.get('business_name', 'su negocio')
        subject = f"Propuesta de Accesibilidad Web para {business_name}"
        
        # Personalizar template
        with open(TEMPLATE, 'r', encoding='utf-8') as f:
            template_content = f.read()
        
        template_content = template_content.replace('{{business_name}}', business_name)
        template_content = template_content.replace('{{domain}}', lead.get('domain', ''))
        template_content = template_content.replace('{{industry}}', lead.get('industry', ''))
        
        # Crear archivo temporal
        temp_file = ROOT / "outbox" / f"temp_{email.replace('@', '_').replace('.', '_')}.html"
        with open(temp_file, 'w', encoding='utf-8') as f:
            f.write(template_content)
        
        # Enviar email
        cmd = [
            "/Users/emilioranucoli/Apps/ranukita-bridge/scripts/rk-skymailer-send",
            "--to", email,
            "--subject", subject,
            "--html-file", str(temp_file)
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            
            # Limpiar archivo temporal
            if temp_file.exists():
                temp_file.unlink()
            
            if result.returncode == 0:
                sent_count += 1
                lead['status'] = 'sent'
                lead['email_sent_date'] = datetime.now().strftime('%Y-%m-%d')
                print(f"✅ Enviado a {email}")
            else:
                print(f"❌ Error enviando a {email}: {result.stderr}")
                
        except Exception as e:
            print(f"❌ Excepción enviando a {email}: {str(e)}")
    
    # Guardar CSV actualizado
    with open(LEADS, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=leads_to_send[0].keys())
        writer.writeheader()
        writer.writerows(load_leads())
    
    log_action('send_outreach', {
        'attempted': len(selected_leads),
        'sent': sent_count,
        'limit_reached': sent_count >= 5
    })
    
    return sent_count

def run_followup_tracking():
    """Ejecuta seguimiento de respuestas"""
    try:
        subprocess.run([
            sys.executable, 
            str(ROOT / "scripts" / "ada-follow-up-tracker.py")
        ], check=True, capture_output=True)
        log_action('followup_tracking', {'status': 'success'})
    except subprocess.CalledProcessError as e:
        log_action('followup_tracking', {'status': 'error', 'error': str(e)})

def generate_daily_report():
    """Genera reporte diario"""
    report = {
        'date': datetime.now().strftime('%Y-%m-%d'),
        'total_leads': len(load_leads()),
        'pending_leads': len([l for l in load_leads() if l.get('status') == 'pending']),
        'sent_leads': len([l for l in load_leads() if l.get('status') == 'sent']),
        'replied_leads': len([l for l in load_leads() if l.get('replied')]),
        'log_entries': []
    }
    
    # Cargar entradas de log del día
    if LOG_FILE.exists():
        with open(LOG_FILE) as f:
            log = json.load(f)
        
        for entry in log:
            if entry['timestamp'].startswith(datetime.now().strftime('%Y-%m-%d')):
                report['log_entries'].append(entry)
    
    # Guardar reporte
    with open(ROOT / "outbox" / "daily-report.json", 'w') as f:
        json.dump(report, f, indent=2)
    
    return report

def main():
    print("🔄 ADA Daily Automation - Iniciando proceso...")
    
    # 1. Verificar leads pendientes
    pending_leads = verify_leads()
    
    # 2. Enviar outreach (si hay pendientes)
    if pending_leads:
        sent_count = send_outreach(pending_leads)
        print(f"📧 Enviados {sent_count} emails")
    else:
        print("📧 No hay leads pendientes para enviar")
    
    # 3. Ejecutar seguimiento
    print("🔄 Ejecutando seguimiento de respuestas...")
    run_followup_tracking()
    
    # 4. Generar reporte
    report = generate_daily_report()
    
    print("\n📊 Reporte diario:")
    print(f"   - Total leads: {report['total_leads']}")
    print(f"   - Pendientes: {report['pending_leads']}")
    print(f"   - Enviados: {report['sent_leads']}")
    print(f"   - Respuestas: {report['replied_leads']}")
    
    log_action('daily_automation_complete', {
        'report': report,
        'status': 'success'
    })

if __name__ == "__main__":
    main()