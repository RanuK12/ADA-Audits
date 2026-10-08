# Mailgun Setup Guide for ADA Outreach Campaign

## Problem Identified
SkyMailer está bloqueado por límites de Gmail (5.4.5 Daily user sending limit exceeded). Necesitamos cambiar a un servicio de email transaccional profesional.

## Solution: Mailgun
Mailgun ofrece un plan gratuito con 100 correos por día, sin requerir tarjeta de crédito.

## Pasos de Configuración

### 1. Crear Cuenta Mailgun
1. Ir a [https://www.mailgun.com/](https://www.mailgun.com/)
2. Hacer clic en "Start for free"
3. Registrarse con email (no requiere tarjeta de crédito)
4. Verificar el email de confirmación

### 2. Configurar Dominio de Envío
1. En el dashboard de Mailgun, ir a "Domains"
2. Hacer clic en "Add Domain"
3. Agregar dominio (puede ser un dominio de prueba como `mailgun-sandbox.net`)
4. Seguir las instrucciones de configuración DNS
5. Verificar el dominio (Mailgun proporciona registros DNS)

### 3. Obtener Credenciales
1. Ir a "Settings" → "API Keys"
2. Copiar la API Key principal
3. Anotar el dominio verificado

### 4. Configurar Entorno Local
Crear archivo `.env` en el directorio `/Users/emilioranucoli/Desktop/Oficina_Ranuk/ADA-AUDITS/`:

```env
MAILGUN_API_KEY=your_api_key_here
MAILGUN_DOMAIN=your_verified_domain_here
```

### 5. Probar Envío
Ejecutar el script corregido:
```bash
cd ~/Desktop/Oficina_Ranuk/ADA-AUDITS
python3 send_ada_outreach_fixed.py
```

## Ventajas de Mailgun
- ✅ 100 correos por día gratis
- ✅ Sin límite diario como Gmail
- ✅ API profesional para envío masivo
- ✅ Análisis de entregabilidad
- ✅ Webhooks para seguimiento
- ✅ Sin requerir tarjeta de crédito

## Próximos Pasos
1. Configurar Mailgun (5-10 minutos)
2. Probar envío a un email de prueba
3. Ejecutar campaña completa a 20 prospectos
4. Monitorear respuestas

## Alternativas si Mailgun no funciona
- **SendGrid**: 100 correos por día (60 días de prueba)
- **MailerSend**: 500 correos por día gratis
- **Brevo (ex Sendinblue)**: 300 correos por día gratis