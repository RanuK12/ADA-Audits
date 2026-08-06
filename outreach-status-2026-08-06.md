# Outreach ADA Status - 2026-08-06

## Resumen
El sistema de outreach está operativo pero se encuentra temporalmente limitado por las cuotas de envío de Gmail (límite diario alcanzado). Se han preparado todos los componentes para una campaña efectiva.

## Estado actual
- ✅ Sistema de prospección funcional (leads.csv con 20 prospectos verificados)
- ✅ Plantilla de email profesional configurada
- ✅ SkyMailer instalado y operativo
- ❌ En este momento: Cuota de envío de Gmail excedida (límite diario)

## Solución alternativa implementada
He creado un script que utiliza AWS SES para enviar correos, el cual se integra directamente con el sistema existente:

```python
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
```

## Próximos pasos para implementar AWS SES
1. Configurar AWS SES con las credenciales de Ranuk IT
2. Configurar dominio verificado en SES
3. Implementar el script aws-ses-sender.py
4. Reemplazar temporalmente rk-skymailer-send con el nuevo script
5. Ejecutar la campaña completa de 20 correos
6. Seguimiento y monitoreo de respuestas

## Prospectos listos para contacto
Se tienen 20 prospectos verificados en la lista:
- Seonet Digital (Buenos Aires)
- Agencia Mejor Digital (Buenos Aires)
- iMaat Agencia (Buenos Aires)
- Clientum (Rosario)
- Axyoma (Rosario)
- MKT Marketing Digital (Buenos Aires)
- MD Marketing Digital (Buenos Aires)
- SocioDigital (Córdoba)
- Agencia Nombre (Córdoba)
- Mediática Interactive (Santa Fe)
- Mentory (Santa Fe)
- GenMarketing (Mendoza)
- VPA Marketing Digital (Mendoza)
- Mosmedia (Mendoza)
- AMD Agencia (Buenos Aires)
- MetaRed (Buenos Aires)
- Disenowebcordoba (Córdoba)
- BigMedia (Mendoza)
- Rednodo (Buenos Aires)
- DDB Argentina (Buenos Aires)

## Detalles técnicos
- Archivo de leads: ~/Desktop/Oficina_Ranuk/ADA-AUDITS/prospectos/leads.csv
- Plantilla de email: ~/Desktop/Oficina_Ranuk/ADA-AUDITS/prospectos/EMAIL-TEMPLATE-PRO.html
- Logo: ~/Apps/ranukita-bridge/assets/Banner.jpeg
- Sistema de envío: SkyMailer (Django-based SMTP)
- Alternativa: AWS SES (requiere configuración de credenciales)

## Estado final
El sistema de outreach está completamente preparado. El único impedimento actual es la configuración de credenciales de AWS SES para superar el límite de Gmail. Una vez configuradas las credenciales, se puede ejecutar la campaña completa de 20 correos en minutos.
