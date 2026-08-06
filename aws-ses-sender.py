#!/usr/bin/env python3
# aws-ses-sender.py - Script para enviar correos mediante AWS SES
# Reemplaza a rk-skymailer-send cuando Gmail alcanza límites

import boto3
import json
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from pathlib import Path

def send_via_ses(to_email, subject, html_content, image_path=None):
    """Envía correo mediante AWS SES"""
    try:
        # Configura el cliente SES
        client = boto3.client('ses', region_name='us-east-1')
        
        # Crea el mensaje
        msg = MIMEMultipart('related')
        msg['Subject'] = subject
        msg['From'] = 'emilio@ranuk.dev'
        msg['To'] = to_email
        
        # Adjunta el HTML
        html_part = MIMEText(html_content, 'html')
        msg.attach(html_part)
        
        # Adjunta la imagen si se proporciona
        if image_path and os.path.exists(image_path):
            with open(image_path, 'rb') as f:
                img = MIMEImage(f.read())
                img.add_header('Content-ID', '<ranuklogo>')
                msg.attach(img)
        
        # Envía el correo
        response = client.send_raw_email(
            Source='emilio@ranuk.dev',
            Destinations=[to_email],
            RawMessage={'Data': msg.as_string()}
        )
        
        return {"status": "sent", "response": response}
    except Exception as e:
        return {"status": "error", "error": str(e)}

def send_test_email():
    """Envía un correo de prueba a emilio@ranuk.dev"""
    BRIDGE = Path.home() / "Apps" / "ranukita-bridge"
    ADA = Path.home() / "Desktop" / "Oficina_Ranuk" / "ADA-AUDITS"
    TEMPLATE = ADA / "prospectos" / "EMAIL-TEMPLATE-PRO.html"
    LOGO = BRIDGE / "assets" / "Banner.jpeg"
    
    try:
        with open(TEMPLATE, 'r') as f:
            html_content = f.read()
        
        result = send_via_ses(
            to_email="emilio@ranuk.dev",
            subject="test aws ses",
            html_content=html_content,
            image_path=str(LOGO)
        )
        
        print(json.dumps(result, indent=2, default=str))
        
        if result["status"] == "sent":
            print("✅ Prueba de envío exitosa")
            return True
        else:
            print(f"❌ Error: {result['error']}")
            return False
            
    except Exception as e:
        print(f"❌ Error al enviar: {str(e)}")
        return False

if __name__ == "__main__":
    send_test_email()