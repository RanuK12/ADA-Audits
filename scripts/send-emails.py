#!/usr/bin/env python3
"""
Envío automatizado de emails de ADA Audits usando SkyMailer.
Procesa el archivo leads.csv y envía emails personalizados.

Uso:
    python3 send-emails.py --leads-file prospectos/leads.csv --template 1
    python3 send-emails.py --leads-file prospectos/leads.csv --template 2 --days-since 3
"""

import csv
import json
import os
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path

def load_template(template_number):
    """Carga una plantilla de email desde EMAIL-TEMPLATES.md"""
    template_file = Path(__file__).parent.parent / "EMAIL-TEMPLATES.md"
    
    with open(template_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extraer plantilla específica
    template_start = f"## Template {template_number}: Cold Outreach"
    if template_number > 1:
        template_start = f"## Template {template_number}:"
    
    template_end = "## Template "
    template_section = content.split(template_start)[1].split(template_end)[0]
    
    # Extraer solo el contenido entre triple backticks
    if "```" in template_section:
        template_body = template_section.split("```")[1]
    else:
        template_body = template_section.strip()
    
    return template_body

def send_email(to_email, subject, body, template_number=1):
    """Envía un email usando SkyMailer"""
    try:
        # Crear archivo temporal con el cuerpo del email
        temp_file = f"/tmp/email-template-{template_number}.html"
        with open(temp_file, 'w', encoding='utf-8') as f:
            f.write(body)
        
        # Comando para enviar con SkyMailer
        cmd = [
            "python3", 
            "~/Apps/ranukita-bridge/scripts/rk-skymailer-send",
            "--to", to_email,
            "--subject", subject,
            "--html-file", temp_file
        ]
        
        # Ejecutar comando
        result = subprocess.run(
            cmd, 
            capture_output=True, 
            text=True,
            cwd="/Users/emilioranucoli/Desktop/Oficina_Ranuk/SkyMailer"
        )
        
        # Limpiar archivo temporal
        os.unlink(temp_file)
        
        # Parsear respuesta JSON
        if result.stdout:
            response = json.loads(result.stdout.strip())
            return response
        else:
            return {"status": "error", "error": "No output from command"}
    
    except Exception as e:
        return {"status": "error", "error": str(e)}

def process_leads(leads_file, template_number, days_since=None):
    """Procesa archivo CSV de leads y envía emails"""
    leads_file = Path(leads_file)
    
    if not leads_file.exists():
        print(f"Error: El archivo {leads_file} no existe")
        return
    
    with open(leads_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        leads = list(reader)
    
    template_body = load_template(template_number)
    sent_count = 0
    error_count = 0
    
    for lead in leads:
        # Verificar si se debe enviar (por días desde último envío)
        if days_since:
            email_sent_date = lead.get('email_sent_date', '')
            if email_sent_date:
                try:
                    sent_date = datetime.strptime(email_sent_date, '%Y-%m-%d')
                    if (datetime.now() - sent_date).days < days_since:
                        continue
                except ValueError:
                    pass
        
        # Extraer datos del lead
        business_name = lead.get('Business Name', '')
        email = lead.get('Email', '')
        city = lead.get('City', '')
        
        if not email or 'example.com' in email:
            print(f"Saltando lead {business_name}: email inválido")
            continue
        
        # Personalizar plantilla
        personalized_body = template_body.replace('{{first_name}}', 'Dr.')  # Podría extraerse del nombre
        personalized_body = personalized_body.replace('{{domain}}', email.split('@')[1])
        personalized_body = personalized_body.replace('{{city}}', city)
        
        # Asunto personalizado
        subject = f"quick note about {email.split('@')[1]}"
        
        print(f"Enviando email a {email} ({business_name})...")
        
        # Enviar email
        result = send_email(email, subject, personalized_body, template_number)
        
        if result.get('status') == 'sent':
            sent_count += 1
            print(f"✅ Enviado a {email}")
            
            # Actualizar fecha de envío en el CSV
            lead['email_sent_date'] = datetime.now().strftime('%Y-%m-%d')
        else:
            error_count += 1
            print(f"❌ Error enviando a {email}: {result.get('error', 'Unknown error')}")
    
    # Guardar CSV actualizado
    with open(leads_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=leads[0].keys())
        writer.writeheader()
        writer.writerows(leads)
    
    print(f"\nResumen:")
    print(f"📧 Enviados: {sent_count}")
    print(f"❌ Errores: {error_count}")

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Envío automatizado de emails de ADA Audits')
    parser.add_argument('--leads-file', default='prospectos/leads.csv', 
                       help='Archivo CSV con los leads')
    parser.add_argument('--template', type=int, default=1,
                       help='Número de plantilla a usar (1-8)')
    parser.add_argument('--days-since', type=int,
                       help='Solo enviar a emails enviados hace X días o más')
    
    args = parser.parse_args()
    
    if args.template < 1 or args.template > 8:
        print("Error: El número de plantilla debe estar entre 1 y 8")
        sys.exit(1)
    
    process_leads(args.leads_file, args.template, args.days_since)

if __name__ == "__main__":
    main()