#!/usr/bin/env python3
"""Renderiza el template HTML de auditoría con datos reales y genera PDF vía WeasyPrint.

Uso: render_html_report.py <data.json> <output.pdf>
El JSON debe tener la estructura del reporte (company, url, score, findings, etc).
"""
import json
import sys
from pathlib import Path

from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML

# Resolver rutas base
PROJECT_ROOT = Path(__file__).resolve().parent.parent  # ada-audits/scripts -> ada-audits
TEMPLATES_DIR = PROJECT_ROOT / "templates"


def render(data: dict, output_pdf: str) -> None:
    env = Environment(loader=FileSystemLoader(str(TEMPLATES_DIR)))
    template = env.get_template("pdf-template.html")

    # Calcular clases de score
    score = data.get("score", 0)
    if score < 50:
        data["score_class"] = "sc-crit"
        data["risk_level"] = "ALTO"
        data["score_desc"] = "Riesgo legal significativo"
    elif score < 70:
        data["score_class"] = "sc-serious"
        data["risk_level"] = "MEDIO"
        data["score_desc"] = "Varias áreas requieren remediación"
    elif score < 90:
        data["score_class"] = "sc-mod"
        data["risk_level"] = "MODERADO"
        data["score_desc"] = "Cumplimiento parcial con gaps puntuales"
    else:
        data["score_class"] = "sc-good"
        data["risk_level"] = "BAJO"
        data["score_desc"] = "Buen nivel de accesibilidad"

    # Contar findings por severidad
    findings = data.get("findings", {})
    data["critical_count"] = len(findings.get("Crítico", []))
    data["serious_count"] = len(findings.get("Alto", []))
    data["moderate_count"] = sum(len(v) for v in findings.values()) - data["critical_count"] - data["serious_count"]
    data["total_count"] = data["critical_count"] + data["serious_count"] + data["moderate_count"]

    # CSS path relativo (WeasyPrint resuelve file://)
    data["css_path"] = str(TEMPLATES_DIR / "pdf-style.css")

    html_out = template.render(**data)

    # Guardar HTML intermedio (skip si output es /dev/null)
    if output_pdf != "/dev/null":
        html_path = Path(output_pdf).with_suffix(".html")
        html_path.write_text(html_out)
        print(f"   HTML intermedio: {html_path}")

    # Generar PDF
    HTML(string=html_out, base_url=str(TEMPLATES_DIR)).write_pdf(output_pdf)
    print(f"✅ PDF generado: {output_pdf}")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(f"Uso: {sys.argv[0]} <data.json> <output.pdf>")
        sys.exit(1)

    with open(sys.argv[1]) as f:
        data = json.load(f)
    render(data, sys.argv[2])