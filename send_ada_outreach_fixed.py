#!/usr/bin/env python3
"""
ADA Outreach Campaign - Script de envío masivo con Brevo
Usa Brevo API para enviar correos a la lista de prospectos filtrados
"""

import csv
import os
import subprocess
import requests
import json
from pathlib import Path

# Rutas
SCRIPT_DIR = Path(__file__).parent
LEADS_FILE = SCRIPT_DIR / "prospectos" / "leads.csv"
TEMPLATE_FILE = SCRIPT_DIR / "EMAIL-TEMPLATE-PRO.html"

def get_brevo_api_key():
    """Obtener la API key de Brevo desde entorno"""
    # Buscar en archivo .env si existe
    env_file = SCRIPT_DIR / ".env"
    if env_file.exists():
        with open(env_file, 'r') as f:
            for line in f:
                if line.startswith('BREVO_API_KEY='):
                    return line.strip().split('=')[1]
    
    # Si no está en .env, buscar en variables de entorno
    return os.getenv('BREVO_API_KEY')

def get_real_prospects():
    """Obtener lista de prospectos reales (quality='real')"""
    prospects = []
    with open(LEADS_FILE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get('Quality') == 'real':
                prospects.append({
                    'business_name': row['Business Name'],
                    'email': row['Email'],
                    'city': row['City']
                })
    return prospects

def send_email_with_brevo(prospect):
    """Enviar email a un prospecto específico usando Brevo API"""
    api_key = get_brevo_api_key()
    
    if not api_key:
        return {
            'email': prospect['email'],
            'business_name': prospect['business_name'],
            'success': False,
            'error': 'Brevo API key not configured'
        }
    
    # Leer el template HTML
    try:
        with open(TEMPLATE_FILE, 'r', encoding='utf-8') as f:
            html_content = f.read()
    except Exception as e:
        return {
            'email': prospect['email'],
            'business_name': prospect['business_name'],
            'success': False,
            'error': f'Error reading template: {str(e)}'
        }
    
    # Personalizar el template con datos del prospecto
    personalized_html = html_content.replace('{{total_nodes_affected}}', '25')
    personalized_html = personalized_html.replace('{{domain}}', prospect['business_name'])
    personalized_html = personalized_html.replace('{{top_issue_1}}', 'Missing alt text on images')
    personalized_html = personalized_html.replace('{{top_issue_2}}', 'Poor color contrast')
    personalized_html = personalized_html.replace('{{top_issue_3}}', 'Keyboard navigation issues')
    
    # Enviar con Brevo API
    url = "https://api.brevo.com/v3/smtp/email"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "api-key": api_key
    }
    
    data = {
        "to": [{"email": prospect['email'], "name": prospect['business_name']}],
        "from": {"email": "ranucoliemilio@gmail.com", "name": "Emilio Ranucoli"},
        "subject": f"Accessibility audit for {prospect['business_name']}",
        "htmlContent": personalized_html,
        "textContent": "Accessibility audit results"
    }
    
    try:
        response = requests.post(url, headers=headers, json=data, timeout=30)
        if response.status_code == 201:
            return {
                'email': prospect['email'],
                'business_name': prospect['business_name'],
                'success': True,
                'response': response.json()
            }
        else:
            return {
                'email': prospect['email'],
                'business_name': prospect['business_name'],
                'success': False,
                'error': f'Brevo API error: {response.status_code} - {response.text}'
            }
    except Exception as e:
        return {
            'email': prospect['email'],
            'business_name': prospect['business_name'],
            'success': False,
            'error': f'Exception sending email: {str(e)}'
        }

def setup_brevo_account():
    """Configuración inicial de Brevo"""
    print("🔧 Brevo Setup Instructions:")
    print("=" * 50)
    print("1. Go to https://www.brevo.com/")
    print("2. Sign up for free (no credit card required)")
    print("3. Verify your email address")
    print("4. Get your API key from the dashboard (Settings > API Keys)")
    print("5. Create a .env file in this directory with:")
    print("   BREVO_API_KEY=your_api_key_here")
    print("=" * 50)

def main():
    """Función principal"""
    print("🚀 Iniciando campaña de outreach ADA con Mailgun...")
    
    # Verificar configuración de Mailgun
    api_key = get_mailgun_api_key()
    domain = get_mailgun_domain()
    
    if not api_key or not domain:
        print("❌ Mailgun no está configurado")
        setup_mailgun_account()
        return
    
    # Obtener prospectos
    prospects = get_real_prospects()
    print(f"✅ Encontrados {len(prospects)} prospectos calificados")
    
    results = []
    successful = 0
    failed = 0
    
    # Enviar correos a cada prospecto
    for i, prospect in enumerate(prospects, 1):
        print(f"📧 Enviando correo {i}/{len(prospects)}: {prospect['business_name']} ({prospect['email']})")
        
        result = send_email_with_mailgun(prospect)
        results.append(result)
        
        if result['success']:
            successful += 1
            print(f"✅ Enviado exitosamente")
        else:
            failed += 1
            print(f"❌ Falló: {result.get('error', 'Unknown error')}")
    
    # Resumen final
    print("\n" + "="*50)
    print("📊 CAMPAÑA COMPLETADA")
    print("="*50)
    print(f"✅ Éxito: {successful}")
    print(f"❌ Fallos: {failed}")
    print(f"📈 Total: {len(prospects)}")
    
    if failed > 0:
        print("\n❓ Correos fallidos:")
        for result in results:
            if not result['success']:
                print(f"  - {result['business_name']} ({result['email']}): {result.get('error', 'Unknown error')}")
    
    # Guardar reporte
    report = {
        'campaign_date': '2026-08-10',
        'total_prospects': len(prospects),
        'successful': successful,
        'failed': failed,
        'results': results
    }
    
    with open(SCRIPT_DIR / 'mailgun_campaign_report.json', 'w') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print(f"\n📄 Reporte guardado en: {SCRIPT_DIR / 'mailgun_campaign_report.json'}")

if __name__ == "__main__":
    main()