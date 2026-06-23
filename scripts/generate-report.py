#!/usr/bin/env python3
"""Genera auditoría completa usando Claude API + scan de axe-core.

Uso: generate-report.py <url>
Output: entregables/<domain>/reporte.md y reporte.pdf
"""
import json
import os
import re
import subprocess as sp
import sys
from datetime import date
from pathlib import Path

url = sys.argv[1]
domain = re.sub(r'^https?://(www\.)?', '', url).rstrip('/').split('/')[0]

# Cargar API key del .env del bot
env_path = Path("/Users/emilioranucoli/ranuk-agent/bot/.env")
api_key = None
if env_path.exists():
    for line in env_path.read_text().splitlines():
        if line.startswith("ANTHROPIC_API_KEY="):
            api_key = line.split("=",1)[1].strip().strip('"').strip("'")
            break
if not api_key:
    api_key = os.environ.get("ANTHROPIC_API_KEY")

if not api_key:
    print("❌ falta ANTHROPIC_API_KEY en ranuk-agent/bot/.env o env")
    sys.exit(1)

out_dir = Path("/Users/emilioranucoli/Desktop/ADA-AUDITS/entregables") / domain.replace('.','_')
out_dir.mkdir(parents=True, exist_ok=True)

# 1. Ejecutar axe profundo
print(f"→ corriendo axe sobre {url}…")
axe_json = out_dir / "axe-raw.json"
sp.run(
    ["axe", url, "--save", "axe-raw.json",
     "--tags", "wcag2a,wcag2aa,wcag21aa,best-practice",
     "--timeout", "60"],
    cwd=out_dir, check=False, capture_output=True
)
if not axe_json.exists() or axe_json.stat().st_size < 100:
    print("❌ axe falló. Verificá que el sitio responda.")
    sys.exit(1)

axe_data = json.loads(axe_json.read_text())
if isinstance(axe_data, list):
    axe_data = axe_data[0] if axe_data else {}

# 2. Preparar contexto compacto para Claude
violations = axe_data.get("violations", [])
compact = []
for v in violations:
    compact.append({
        "id": v["id"],
        "impact": v.get("impact"),
        "help": v.get("help"),
        "helpUrl": v.get("helpUrl"),
        "tags": v.get("tags",[])[:5],
        "nodes": [
            {"html": n.get("html","")[:300], "target": n.get("target",[])}
            for n in v.get("nodes", [])[:3]  # máx 3 samples por regla
        ],
        "total_nodes": len(v.get("nodes", [])),
    })

# 3. Llamar a Claude API con prompt-caching
prompt_template = Path("/Users/emilioranucoli/Desktop/ADA-AUDITS/templates/PROMPT-GENERAR-AUDITORIA.md").read_text()
m = re.search(r"## PROMPT\s+```(.*?)```", prompt_template, re.DOTALL)
system_prompt = m.group(1).strip() if m else prompt_template

print(f"→ enviando a Claude API ({len(violations)} violaciones, {sum(len(v['nodes']) for v in compact)} elementos)…")

import urllib.error
import urllib.request

req = urllib.request.Request(
    "https://api.anthropic.com/v1/messages",
    method="POST",
    headers={
        "x-api-key": api_key,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json",
    },
    data=json.dumps({
        "model": "claude-sonnet-4-5-20250929",
        "max_tokens": 8000,
        "system": [
            {"type":"text","text": system_prompt, "cache_control":{"type":"ephemeral"}}
        ],
        "messages": [{
            "role":"user",
            "content": f"Cliente: {domain}\nURL: {url}\nFecha: {date.today().isoformat()}\n\nHallazgos de axe-core (JSON):\n\n```json\n{json.dumps(compact, ensure_ascii=False, indent=2)[:60000]}\n```\n\nGenerá la auditoría completa en Markdown siguiendo la plantilla. Usá español argentino. No agregues disclaimers extra."
        }]
    }).encode()
)

try:
    with urllib.request.urlopen(req, timeout=300) as resp:
        result = json.load(resp)
except urllib.error.HTTPError as e:
    print(f"❌ API error {e.code}: {e.read().decode()[:500]}")
    sys.exit(1)

md = "".join(b["text"] for b in result.get("content",[]) if b.get("type")=="text")
usage = result.get("usage",{})
print(f"  tokens: in={usage.get('input_tokens')} cached_read={usage.get('cache_read_input_tokens',0)} out={usage.get('output_tokens')}")

# Guardar Markdown
report_file = out_dir / "reporte.md"
report_file.write_text(md)
print(f"✅ reporte guardado: {report_file}")

# --- NUEVA LÓGICA DE PDF ---
print("→ generando PDF de auditoría...")
pdf_path = out_dir / "reporte.pdf"

# Configuración para ranukita_report.py
spec = {
    "title": f"Auditoría de Accesibilidad - {domain}",
    "content": md,
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

# Ejecutar la skill
try:
    sp.run([
        "python3", "/Users/emilioranucoli/Apps/ranukita-bridge/scripts/ranukita_report.py",
        "--spec", json.dumps(spec),
        "--output", str(pdf_path)
    ], check=True)
    print(f"✅ PDF generado con éxito: {pdf_path}")
except Exception as e:
    print(f"❌ Error al generar PDF: {e}")
    sys.exit(1)
