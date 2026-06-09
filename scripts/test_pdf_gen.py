import json, subprocess
from pathlib import Path

# Simular el contenido que generaría el script original
mock_md = """# Auditoría de Accesibilidad
## Resumen
El sitio cumple con los estándares básicos pero requiere mejoras en contraste.
## Hallazgos
1. Falta de etiquetas alt en imágenes.
2. Contraste de color insuficiente en botones de acción.
"""

spec = {
    "title": "Auditoría de Accesibilidad - Test",
    "content": mock_md,
    "branding": {
        "logo_path": "/Users/emilioranucoli/Apps/ranukita-bridge/assets/ranukita-logo.png",
        "watermark_logo": "/Users/emilioranucoli/Apps/ranukita-bridge/assets/minilogo2.png",
        "footer": "Ranukita Bot — Propiedad de Ranuk IT Solutions | ranuk.dev | ranukorbit.com"
    },
    "styles": {
        "background_color": "#1a1a2e",
        "primary_color": "#00d4ff",
        "accent_color": "#ffd700"
    }
}

pdf_path = Path("/Users/emilioranucoli/Desktop/Oficina_Ranuk/ADA-AUDITS/entregables/test_report.pdf")
pdf_path.parent.mkdir(parents=True, exist_ok=True)

print(f"→ Generando PDF de prueba en {pdf_path}...")
try:
    subprocess.run([
        "python3", "/Users/emilioranucoli/Apps/ranukita-bridge/scripts/ranukita_report.py",
        "--spec", json.dumps(spec),
        "--output", str(pdf_path)
    ], check=True)
    print(f"✅ PDF generado con éxito: {pdf_path}")
except Exception as e:
    print(f"❌ Error: {e}")
