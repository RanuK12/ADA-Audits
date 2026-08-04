#!/usr/bin/env python3
"""
Envío de outreach con manejo de límites y reintentos.
Uso: ada-outreach-with-retry.py --template email-template.html --leads leads_cleaned.csv --max 5
"""
import csv
import json
import subprocess
import sys
import os
import time
from pathlib import Path
from datetime import datetime, timedelta

ROOT = Path(__file__).resolve().parent.parent
TEMPLATE = ROOT / "outbox" / "email-template.html"
LEADS = ROOT / "prospectos" / "leads_cleaned.csv"
MAX_EMAILS = 5
RETRY_DELAY_HOURS = 24  # Esperar 24 horas antes de reintentar
GMAIL_LIMIT_ERROR = "Daily user sending limit exceeded"

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

def check_gmail_limit():
    """Verifica si hay límite de Gmail activo"""
    # Probar con un email de prueba
    test_email = "test@example.com"
    test_subject = "Test de envío"
    test_html = "<p>Test</p>"
    
    cmd = [
        "/Users/emilioranucoli/Apps/ranukita-bridge/scripts/rk-skymailer-send",
        "--to", test_email,
        "--subject", test_subject,
        "--html-file", "/dev/stdin"  # Usar stdin para evitar crear archivo
    ]
    
    try:
        result = subprocess.run(
            cmd, 
            input=test_html, 
            capture_output=True, 
            text=True, 
            timeout=30
        )
        
        if GMAIL_LIMIT_ERROR in result.stderr:
            print("⚠️ Límite de Gmail activo. Esperando para reintentar...")
            return True
        return False
        
    except Exception as e:
        print(f"⚠️ Error verificando límite: {str(e)}")
        return False

def send_email_with_retry(email, subject, html_content, lead, max_retries=3):
    """Envía email con reintentos si hay límite"""
    for attempt in range(max_retries):
        if attempt > 0:
            print(f"⏳ Esperando {RETRY_DELAY_HOURS} horas antes del reintento {attempt}...")
            time.sleep(RETRY_DELAY_HOURS * 3600)  # Esperar 24 horas
        
        # Verificar límite antes de cada intento
        if check_gmail_limit():
            continue
        
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
                if GMAIL_LIMIT_ERROR in result.stderr:
                    print(f"⚠️ Límite de Gmail detectado. Reintentando...")
                    continue
                else:
                    print(f"❌ Error enviando a {email}: {result.stderr}")
                    return False
                    
        except Exception as e:
            print(f"❌ Excepción enviando a {email}: {str(e)}")
            return False
    
    print(f"❌ Agotados reintentos para {email}")
    return False

def main():
    print("🔄 ADA Outreach con manejo de límites...")
    
    # Verificar límite inicial
    if check_gmail_limit():
        print(f"⚠️ Límite de Gmail activo. El sistema esperará {RETRY_DELAY_HOURS} horas antes de intentar enviar.")
        return
    
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
        
        if send_email_with_retry(email, subject, personalized_html, lead):
            sent_count += 1
            # Actualizar status del lead
            lead['status'] = 'sent'
            lead['email_sent_date'] = datetime.now().strftime('%Y-%m-%d')
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