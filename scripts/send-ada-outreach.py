#!/usr/bin/env python3
"""
Envío de outreach personalizado para ADA Audits usando SkyMailer.
Uso: send-ada-outreach.py --template email-template.html --leads leads_cleaned.csv --max 5
"""
import csv
import json
import subprocess
import sys
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEMPLATE = ROOT / "outbox" / "email-template.html"
LEADS = ROOT / "prospectos" / "leads_cleaned.csv"
MAX_EMAILS = 5

def load_leads():
    """Carga leads desde CSV"""
    with open(LEADS) as f:
        return list(csv.DictReader(f))

def personalize_email(template_path, lead):
    """Personaliza el template con datos del lead"""
    with open(template_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Reemplazar placeholders
    content = content.replace('{{business_name}}', lead.get('business_name', 'su sitio web'))
    content = content.replace('{{domain}}', lead.get('domain', ''))
    content = content.replace('{{industry}}', lead.get('industry', ''))
    content = content.replace('{{city}}', lead.get('city', ''))
    content = content.replace('{{state}}', lead.get('state', ''))
    
    return content

def send_email_with_skymailer(email, subject, html_content, lead):
    """Envía email usando SkyMailer"""
    try:
        # Crear archivo temporal con el contenido HTML
        temp_html = ROOT / "outbox" / f"temp_{email.replace('@', '_').replace('.', '_')}.html"
        with open(temp_html, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        # Enviar con SkyMailer
        cmd = [
            "/Users/emilioranucoli/Apps/ranukita-bridge/scripts/rk-skymailer-send",
            "--to", email,
            "--subject", subject,
            "--html-file", str(temp_html)
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        
        # Limpiar archivo temporal
        if temp_html.exists():
            temp_html.unlink()
        
        if result.returncode == 0:
            try:
                response = json.loads(result.stdout)
                if response.get('status') == 'sent':
                    print(f"✅ Email enviado a {email}")
                    return True
                else:
                    print(f"❌ Error en respuesta para {email}: {response}")
                    return False
            except:
                # Si no es JSON válido, asumimos que fue enviado si no hay error
                if "sent" in result.stdout.lower() or result.returncode == 0:
                    print(f"✅ Email enviado a {email}")
                    return True
                else:
                    print(f"❌ Error parseando respuesta para {email}: {result.stdout}")
                    return False
        else:
            print(f"❌ Error enviando a {email}: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Excepción enviando a {email}: {str(e)}")
        return False

def main():
    leads = load_leads()
    
    # Filtrar solo prospectos pendientes
    pending_leads = [lead for lead in leads if lead.get('status') == 'pending']
    
    if not pending_leads:
        print("❌ No hay prospectos pendientes para enviar")
        return
    
    # Limitar al máximo especificado
    selected_leads = pending_leads[:MAX_EMAILS]
    
    print(f"📧 Enviando emails a {len(selected_leads)} prospectos...")
    
    sent_count = 0
    for lead in selected_leads:
        email = lead.get('owner_email')
        if not email:
            print(f"⚠️ Lead sin email: {lead.get('business_name', 'Desconocido')}")
            continue
        
        # Personalizar email
        personalized_html = personalize_email(TEMPLATE, lead)
        subject = f"Propuesta de Accesibilidad Web para {lead.get('business_name', 'su negocio')}"
        
        print(f"🔄 Enviando a {email} ({lead.get('business_name', 'Desconocido')})...")
        
        if send_email_with_skymailer(email, subject, personalized_html, lead):
            sent_count += 1
            # Actualizar status del lead
            lead['status'] = 'sent'
            lead['email_sent_date'] = '2026-07-29'  # Fecha actual
        else:
            print(f"❌ Falló el envío a {email}")
    
    # Guardar CSV actualizado
    with open(LEADS, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=leads[0].keys())
        writer.writeheader()
        writer.writerows(leads)
    
    print(f"\n📊 Resumen: {sent_count} emails enviados exitosamente")

if __name__ == "__main__":
    main()