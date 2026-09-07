#!/usr/bin/env python3
"""ADA Audit Report Generator — WCAG accessibility audits for PyMEs.

Usage:
    python3 generate_report.py                          # sample demo
    python3 generate_report.py --input findings.json    # custom JSON
    python3 generate_report.py --input findings.json --pdf  # + PDF
"""

import argparse
import json
import os
import subprocess
import sys
import tempfile
from datetime import datetime
from urllib.parse import quote


def estimate_impact(item):
    """Estimate monetary impact or legal risk for a finding."""
    if item.get('business_impact'):
        return item['business_impact']
    
    severity = item.get('severity', '').lower()
    issue = item.get('issue', '').lower()
    
    if severity == 'critical':
        return "Riesgo legal alto: posible demanda ADA Title III, multas hasta $75,000 por primera infracción"
    elif severity == 'high':
        return "Pérdida estimada de 10-15% conversión + riesgo demanda"
    elif severity == 'medium':
        return "Pérdida estimada de 5-10% usuarios con discapacidad + riesgo legal moderado"
    elif severity == 'low':
        return "Mejora UX y cumplimiento preventivo"
    return "Impacto no estimado - revisar manualmente"


def generate_diagram(item):
    """Generate a simple text diagram showing before/after."""
    before = item.get('before', '').strip()
    after = item.get('after', '').strip()
    
    if not before and not after:
        return ""
    
    lines = ["```text", "┌─ ANTES ──────────────────────────────────────────────┐"]
    if before:
        for line in before.split('\n'):
            lines.append(f"│ {line[:60]:<60} │")
    else:
        lines.append(f"│ {'(sin código antes)':<60} │")
    lines.append("├──────────────────────────────────────────────────────┤")
    lines.append("│ DESPUÉS                                              │")
    if after:
        for line in after.split('\n'):
            lines.append(f"│ {line[:60]:<60} │")
    else:
        lines.append(f"│ {'(sin código después)':<60} │")
    lines.append("└──────────────────────────────────────────────────────┘")
    lines.append("```")
    return "\n".join(lines)


def generate_report(data):
    """Generate a Markdown audit report from structured data."""
    report = []
    report.append(f"# Auditoría de Accesibilidad WCAG: {data['client_name']}")
    report.append(f"**Fecha:** {data['date']}")
    report.append(f"**Estado:** Finalizado")
    report.append("\n## Resumen Ejecutivo")
    report.append(f"{data['summary']}")

    if data.get('findings'):
        report.append("\n## 💰 Impacto Financiero y Riesgo Legal")
        for item in data['findings']:
            report.append(f"- **{item['issue']}** → {item.get('business_impact', '')}")

        report.append("\n## Hallazgos Detallados")
        report.append("| Hallazgo | Severidad | Impacto en el negocio |")
        report.append("| --- | --- | --- |")

        for item in data['findings']:
            report.append(f"| {item['issue']} | {item['severity']} | {item.get('business_impact', '')} |")

        for item in data['findings']:
            report.append(f"\n### {item['issue']}")
            
            # Impact line (estimated or provided)
            impact_text = estimate_impact(item)
            report.append(f"**Impacto estimado:** {impact_text}")
            
            # Visual representation (diagram)
            diagram = generate_diagram(item)
            if diagram:
                report.append("**Representación visual (antes/después):**")
                report.append(diagram)
            
            # CTA per finding
            issue_encoded = quote(item['issue'])
            cta_url = f"mailto:emilio@ranuk.dev?subject=Correcci%C3%B3n+de+{issue_encoded}"
            report.append(f"**¿Querés corregir este issue?** [Contratarnos]({cta_url})")
            
            # Original before/after code blocks
            report.append("**Antes → Después**")
            before_code = item.get('before', '')
            after_code = item.get('after', '')
            if before_code:
                report.append("**Antes:**")
                report.append("```html")
                report.append(before_code)
                report.append("```")
            if after_code:
                report.append("**Después:**")
                report.append("```html")
                report.append(after_code)
                report.append("```")

    if data.get('recommendations'):
        report.append("\n## Recomendaciones")
        for rec in data['recommendations']:
            report.append(f"- {rec}")

    report.append("")
    report.append("> **💡 ¿Querés que arreglemos esto?**")
    report.append(">")
    report.append("> Respondé este informe o escribinos a **emilio@ranuk.dev** para coordinar las correcciones.")
    report.append(">")
    report.append("> **Ranuk IT Solutions** — [ranuk.dev](https://ranuk.dev)")

    return "\n".join(report)


def markdown_to_pdf_spec(md_path, pdf_path):
    """Convert a generated markdown report to PDF using the official Ranukita report engine."""
    with open(md_path) as f:
        content = f.read()

    # Parse the markdown into sections for the report spec
    lines = content.split("\n")
    title = ""
    sections = []
    current_heading = ""
    current_body = []
    current_bullets = []

    for line in lines:
        if line.startswith("# ") and not title:
            title = line.lstrip("# ").strip()
        elif line.startswith("## "):
            if current_heading:
                sections.append({
                    "heading": current_heading,
                    "body": "\n".join(current_body).strip(),
                    "bullets": current_bullets
                })
            current_heading = line.lstrip("## ").strip()
            current_body = []
            current_bullets = []
        elif line.startswith("### "):
            if current_heading:
                sections.append({
                    "heading": current_heading,
                    "body": "\n".join(current_body).strip(),
                    "bullets": current_bullets
                })
            current_heading = line.lstrip("### ").strip()
            current_body = []
            current_bullets = []
        elif line.startswith("- "):
            current_bullets.append(line.lstrip("- ").strip())
        elif line.strip():
            current_body.append(line)
        else:
            if current_body:
                current_body.append("")

    if current_heading:
        sections.append({
            "heading": current_heading,
            "body": "\n".join(current_body).strip(),
            "bullets": current_bullets
        })

    spec = {
        "title": title or "Auditoría de Accesibilidad WCAG",
        "subtitle": f"Generado el {datetime.now().strftime('%d/%m/%Y')}",
        "sections": sections
    }

    spec_path = os.path.join(tempfile.gettempdir(), "ada_spec.json")
    with open(spec_path, "w") as f:
        json.dump(spec, f, ensure_ascii=False, indent=2)

    # Call the official report generator
    script = os.path.expanduser("~/Apps/ranukita-bridge/scripts/ranukita_report.py")
    result = subprocess.run(
        ["python3", script, spec_path, pdf_path, "dark"],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print(f"⚠️  PDF generation failed: {result.stderr.strip()}")
        return False

    if os.path.exists(pdf_path):
        print(f"PDF generado: {pdf_path}")
        return True
    return False


def main():
    parser = argparse.ArgumentParser(description="ADA Audit Report Generator")
    parser.add_argument("--input", "-i", help="JSON file with audit findings")
    parser.add_argument("--output", "-o", default="audit_report.md", help="Output markdown file")
    parser.add_argument("--pdf", action="store_true", help="Also generate PDF")
    args = parser.parse_args()

    if args.input:
        if not os.path.exists(args.input):
            print(f"❌ Error: input file '{args.input}' not found", file=sys.stderr)
            sys.exit(1)
        try:
            with open(args.input) as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            print(f"❌ Error: invalid JSON in '{args.input}': {e}", file=sys.stderr)
            sys.exit(1)
    else:
        # Sample demo data
        data = {
            "client_name": "TiendaOnline Demo",
            "date": datetime.now().strftime("%Y-%m-%d"),
            "summary": "Auditoría de accesibilidad WCAG 2.1 AA — se detectaron barreras que afectan la experiencia de usuarios con discapacidad y exponen a la empresa a riesgos legales.",
            "findings": [
                {
                    "issue": "Contraste bajo en botón de compra",
                    "severity": "High",
                    "business_impact": "–12% conversión mobile / demanda ADA Title III",
                    "before": "<button style=\"background: #FFA500; color: #FFFFFF;\">Comprar</button>",
                    "after": "<button style=\"background: #D2691E; color: #FFFFFF;\">Comprar</button>"
                },
                {
                    "issue": "Imágenes de producto sin alt text",
                    "severity": "Medium",
                    "business_impact": "Lectores de pantalla no pueden describir los productos → pérdida de ventas y riesgo de demanda",
                    "before": "<img src=\"producto.jpg\">",
                    "after": "<img src=\"producto.jpg\" alt=\"Zapatillas running azul\">"
                },
                {
                    "issue": "Menú de navegación no operable por teclado",
                    "severity": "Critical",
                    "business_impact": "Usuarios sin mouse no pueden navegar → abandono del sitio y posible demanda ADA",
                    "before": "<div class=\"menu\" onclick=\"toggleMenu()\">",
                    "after": "<nav aria-label=\"Principal\"><ul role=\"menubar\"><li role=\"menuitem\">Inicio</li><li role=\"menuitem\">Productos</li><li role=\"menuitem\">Contacto</li></ul></nav>"                }
            ],
            "recommendations": [
                "Aumentar contraste de botones críticos a 4.5:1 mínimo",
                "Agregar alt text descriptivo a todas las imágenes de producto",
                "Refactorizar navegación con elementos semánticos y roles ARIA"
            ]
        }

    report = generate_report(data)

    with open(args.output, "w") as f:
        f.write(report)
    print(f"✅ Informe generado: {args.output}")

    if args.pdf:
        pdf_path = args.output.replace('.md', '.pdf')
        if markdown_to_pdf_spec(args.output, pdf_path):
            print(f"✅ PDF generado: {pdf_path}")

if __name__ == "__main__":
    main()
