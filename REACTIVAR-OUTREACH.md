# Reactivar Outreach con SkyMailer

## Estado actual del proyecto

- **Sistema de escaneo:** ✅ Funcional (`quick-scan.sh`)
- **Plantillas de email:** ✅ Listas (creadas `EMAIL-TEMPLATES.md`)
- **Base de leads:** ⚠️ Desactualizada (último envío 2026-06-06)
- **Proceso de envío:** ❌ Manual (no automatizado con SkyMailer)

## Plan de reactivación (2 horas)

### Paso 1: Actualizar leads (45 min)
1. Elegir vertical del día: **Dentistas Nueva York**
2. Buscar en Google Maps 20 URLs de dentistas en Brooklyn/Queens
3. Agregar URLs a `prospectos/urls-del-dia.txt`
4. Ejecutar escaneo:
   ```bash
   ./scripts/quick-scan.sh -f prospectos/urls-del-dia.txt > /tmp/scan-nuevo.json
   ```
5. Filtrar los `qualifies_as_lead == true` y agregar a `leads.csv`

### Paso 2: Integrar SkyMailer (45 min)
1. Revisar script de SkyMailer en `~/Apps/ranukita-bridge/scripts/rk-skymailer-send`
2. Crear script de integración `ada-sky-send.py` que:
   - Lea `leads.csv` y filtre los `status=pending`
   - Use las plantillas de `EMAIL-TEMPLATES.md`
   - Envíe emails con SkyMailer (no Gmail para mayor entregabilidad)
3. Probar con 1 lead de prueba

### Paso 3: Preparar flujo (30 min)
1. Crear script `ada-outreach-daily.py` que:
   - Ejecute `quick-scan.sh` cada mañana
   - Genere pitches con `generate-pitch.py`
   - Envíe con SkyMailer usando `ada-sky-send.py`
   - Actualice `leads.csv` con `email_sent_date`

## Criterios de targeting actualizados

### Vertical prioritaria: Dentistas Nueva York
- **Ubicación:** Brooklyn, Queens, Manhattan
- **Tamaño:** 1-5 clínicas (no cadenas grandes)
- **Presupuesto estimado:** $800-1,500
- **Contacto:** Dr. [Nombre], office@clinica.com

### Exclusiones:
- Solo presencia en redes sociales
- Sitios en construcción
- Dominios gratuitos
- Empresas >500 empleados

## Implementación SkyMailer

### Script de integración (`scripts/ada-sky-send.py`)
```python
#!/usr/bin/env python3
"""
Envía emails de ADA Audits usando SkyMailer para mayor entregabilidad.
Uso: ada-sky-send.py --leads leads.csv --template template1
"""
import csv
import json
import subprocess
from pathlib import Path
from datetime import date
import jinja2

def load_leads(leads_file):
    """Carga leads pendientes de leads.csv"""
    with open(leads_file) as f:
        return [row for row in csv.DictReader(f) if row.get('status') == 'pending']

def load_template(template_name):
    """Carga plantilla de EMAIL-TEMPLATES.md"""
    templates = Path(__file__).parent.parent / "EMAIL-TEMPLATES.md"
    # Implementación de carga de plantillas
    pass

def send_with_skymailer(email, subject, body, domain):
    """Envía email usando SkyMailer"""
    cmd = [
        "/Users/emilioranucoli/Apps/ranukita-bridge/scripts/rk-skymailer-send",
        "--to", email,
        "--subject", subject,
        "--html-file", "/tmp/body.html",
        "--attach", "/tmp/scan.json"  # Adjuntar reporte si existe
    ]
    
    # Preparar HTML para SkyMailer
    html_content = f"""
    <html>
    <body>
    {body.replace('\n', '<br>')}
    </body>
    </html>
    """
    
    Path("/tmp/body.html").write_text(html_content)
    subprocess.run(cmd, check=True)

def main():
    leads = load_leads("prospectos/leads.csv")
    print(f"📧 {len(leads)} leads pendientes")
    
    for lead in leads:
        # Generar pitch personalizado
        pitch = generate_pitch(lead)
        
        # Enviar con SkyMailer
        send_with_skymailer(
            email=lead['owner_email'],
            subject=pitch['subject'],
            body=pitch['body'],
            domain=lead['domain']
        )
        
        # Actualizar lead como enviado
        update_lead_status(lead['domain'], 'sent', date.today())

if __name__ == "__main__":
    main()
```

## Flujo diario automatizado

### Script principal (`scripts/ada-outreach-daily.py`)
```python
#!/usr/bin/env python3
"""
Flujo diario de outreach para ADA Audits con SkyMailer.
Ejecutar cada mañana a las 9 AM.
"""
import subprocess
from datetime import date
from pathlib import Path

def daily_scan():
    """Ejecuta escaneo del día"""
    print("🔍 Ejecutando escaneo diario...")
    subprocess.run([
        "./scripts/quick-scan.sh", 
        "-f", "prospectos/urls-del-dia.txt"
    ], check=True)
    print("✅ Escaneo completado")

def generate_leads():
    """Genera nuevos leads a partir de escaneo"""
    print("📊 Generando leads...")
    subprocess.run([
        "./scripts/generate-pitch.py",
        "--batch", "/tmp/scan-nuevo.json"
    ], check=True)
    print("✅ Leads generados")

def send_outreach():
    """Envía outreach con SkyMailer"""
    print("📧 Enviando outreach...")
    subprocess.run([
        "./scripts/ada-sky-send.py",
        "--leads", "prospectos/leads.csv",
        "--template", "template1"
    ], check=True)
    print("✅ Outreach enviado")

if __name__ == "__main__":
    daily_scan()
    generate_leads()
    send_outreach()
    print("🎉 Flujo diario completado")
```

## Próximos pasos

1. **Hoy:** Implementar `ada-sky-send.py` y probar con 1 lead
2. **Mañana:** Ejecutar flujo completo con 5 nuevos leads
3. **Esta semana:** Monitorear entregabilidad vs Gmail
4. **Siguiente semana:** Optimizar plantillas basado en respuestas

## Métricas objetivo

| Semana | Emails enviados | Entregabilidad | Respuestas | Cierres |
|--------|----------------|----------------|-------------|---------|
| 1      | 20             | 85%            | 3-4         | 1       |
| 2      | 25             | 88%            | 5-6         | 1-2     |
| 3      | 30             | 90%            | 7-9         | 2       |
| 4      | 30             | 90%            | 7-9         | 2       |
| **Total** | **105**     | **88%**        | **22-28**   | **6-7** |