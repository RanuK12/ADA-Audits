#!/usr/bin/env python3
"""
ADA Outreach Campaign - Script de envío masivo
Usa SkyMailer para enviar correos a la lista de prospectos filtrados
"""

import csv
import os
import subprocess
from pathlib import Path

# Rutas
SCRIPT_DIR = Path(__file__).parent
LEADS_FILE = SCRIPT_DIR / "prospectos" / "leads.csv"
TEMPLATE_FILE = SCRIPT_DIR / "EMAIL-TEMPLATE-PRO.html"

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

def send_email_to_prospect(prospect):
    """Enviar email a un prospecto específico usando SkyMailer"""
    # Aquí podrías personalizar el template con los datos del prospecto
    # Por ahora, envía el template base
    
    cmd = [
        "/Users/emilioranucoli/Apps/ranukita-bridge/scripts/rk-skymailer-send",
        "--to", prospect['email'],
        "--subject", f"Accessibility audit for {prospect['business_name']}",
        "--html-file", str(TEMPLATE_FILE)
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        return {
            'email': prospect['email'],
            'business_name': prospect['business_name'],
            'success': result.returncode == 0,
            'output': result.stdout
        }
    except subprocess.TimeoutExpired:
        return {
            'email': prospect['email'],
            'business_name': prospect['business_name'],
            'success': False,
            'error': 'Timeout'
        }
    except Exception as e:
        return {
            'email': prospect['email'],
            'business_name': prospect['business_name'],
            'success': False,
            'error': str(e)
        }

def main():
    """Función principal"""
    print("🚀 Iniciando campaña de outreach ADA...")
    
    # Obtener prospectos
    prospects = get_real_prospects()
    print(f"✅ Encontrados {len(prospects)} prospectos calificados")
    
    results = []
    successful = 0
    failed = 0
    
    # Enviar correos a cada prospecto
    for i, prospect in enumerate(prospects, 1):
        print(f"📧 Enviando correo {i}/{len(prospects)}: {prospect['business_name']} ({prospect['email']})")
        
        result = send_email_to_prospect(prospect)
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

if __name__ == "__main__":
    main()