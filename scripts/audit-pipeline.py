#!/usr/bin/env python3
"""ADA Audit Pipeline: URL -> Scan -> Score -> Branded PDF.

[ranukita:ccbce0]

Dependencies:
    - axe-core CLI (npm install -g @axe-core/cli)
    - weasyprint (pip install weasyprint)
    - jinja2    (pip install jinja2)

Usage:
    python audit-pipeline.py https://example.com --company "Acme Inc"
"""
import argparse
import json
import re
import subprocess
from datetime import date
from pathlib import Path

from jinja2 import Template

BASE = Path(__file__).resolve().parent.parent
TEMPLATE_HTML = BASE / "templates/pdf-template.html"
TEMPLATE_CSS = BASE / "templates/pdf-style.css"
ENTREGABLES = BASE / "entregables"

def run_axe(url, out_dir):
    axe_json = out_dir / "axe-raw.json"
    subprocess.run(["axe", url, "--save", "axe-raw.json",
        "--tags", "wcag2a,wcag2aa,wcag21aa,best-practice", "--timeout", "60"],
        cwd=out_dir, check=False, capture_output=True)
    if not axe_json.exists() or axe_json.stat().st_size < 50:
        return {"violations": [], "error": "scan_failed"}
    data = json.loads(axe_json.read_text())
    return data[0] if isinstance(data, list) and data else (data if isinstance(data, dict) else {})

def classify(violations):
    b = {"critical": [], "serious": [], "moderate": [], "minor": []}
    for v in violations:
        b.get(v.get("impact", "minor"), b["minor"]).append(v)
    return b

def calc_score(b):
    return max(0, min(100, 100 - len(b["critical"])*8 - len(b["serious"])*4 - len(b["moderate"])*2 - len(b["minor"])))

def score_class(s):
    if s < 30: return "sc-crit"
    if s < 60: return "sc-serious"
    if s < 80: return "sc-mod"
    return "sc-good"

def risk_info(score, crit):
    if crit >= 5 or score < 20:
        return ("CRITICO", "El sitio presenta barreras que bloquean el acceso y expone a litigios federales ADA Title III. +5.000 demandas en 2025, 69% contra PyMEs.")
    if crit >= 2 or score < 50:
        return ("ALTO", "Multiples no-conformidades serias que incrementan el riesgo de demanda.")
    if score < 75:
        return ("MEDIO", "Mejoras necesarias para cumplimiento WCAG 2.1 AA completo.")
    return ("BAJO", "Ajustes menores recomendados.")

def build_findings(buckets):
    result = {}
    labels = {"critical": "Criticos", "serious": "Altos", "moderate": "Medios", "minor": "Bajos"}
    idx = {"critical": "C", "serious": "A", "moderate": "M", "minor": "B"}
    for sev, label in labels.items():
        items = []
        for i, v in enumerate(buckets[sev], 1):
            tags = v.get("tags", [])
            wcag = next((t for t in tags if t.startswith("wcag") and "best" not in t), v.get("id",""))
            items.append({"id": f"{idx[sev]}-{i:02d}", "wcag_criterion": wcag,
                "description": v.get("help", "")[:120],
                "nodes_affected": v.get("total_nodes", len(v.get("nodes",[]))),
                "effort": "30-60 min" if sev in ("critical","serious") else "15 min"})
        if items:
            result[label] = items
    return result

def build_top3(buckets):
    top3 = []
    rm = {"critical":"critical","serious":"high","moderate":"medium"}
    for sev in ["critical","serious","moderate"]:
        if buckets[sev]:
            v = buckets[sev][0]
            tags = v.get("tags",[])
            wcag = next((t for t in tags if t.startswith("wcag") and "best" not in t), v.get("id",""))
            top3.append({"title": v.get("help","")[:80], "description": v.get("description","")[:200],
                "wcag_criterion": wcag, "effort": "1-2h" if sev=="critical" else "30-60 min",
                "risk_class": rm.get(sev,"medium")})
    return top3[:3]

def build_remediation(buckets):
    phases = []
    if buckets["critical"]:
        phases.append({"title":"Fase 1 - Criticos (Semana 1)",
            "tasks":[v.get("help","")[:80] for v in buckets["critical"][:10]],
            "deliverable":"Sitio libre de hallazgos rojos + declaracion de accesibilidad",
            "risk_class":"critical"})
    if buckets["serious"]:
        phases.append({"title":"Fase 2 - Altos (Semana 2)",
            "tasks":[v.get("help","")[:80] for v in buckets["serious"][:10]],
            "deliverable":"Cumplimiento WCAG 2.1 AA alcanzado","risk_class":"high"})
    minor_all = buckets["moderate"] + buckets["minor"]
    if minor_all:
        phases.append({"title":"Fase 3 - Medios y Bajos (Semana 3)",
            "tasks":[v.get("help","")[:80] for v in minor_all[:10]],
            "deliverable":"Certificado + 30 dias soporte","risk_class":"medium"})
    return phases

def build_compliance_table(axe_data):
    cmap = {}
    for v in axe_data.get("violations",[]):
        for tag in v.get("tags",[]):
            if tag.startswith("wcag") and "best" not in tag:
                cmap.setdefault(tag,[]).append(v.get("impact","minor"))
    badge = {"critical":"badge-critical","serious":"badge-serious","moderate":"badge-moderate","minor":"badge-minor"}
    status = {"critical":"No cumple","serious":"Riesgo alto","moderate":"Parcial","minor":"OK"}
    rows = []
    for crit in sorted(cmap.keys()):
        impacts = cmap[crit]
        worst = "critical" if "critical" in impacts else "serious" if "serious" in impacts else "moderate" if "moderate" in impacts else "minor"
        rows.append({"criterion": crit, "badge_class": badge.get(worst,"badge-minor"),
            "status": status.get(worst,"OK"), "violations": len(impacts)})
    return rows

def main():
    parser = argparse.ArgumentParser(description="ADA Audit Pipeline")
    parser.add_argument("url", help="URL to audit")
    parser.add_argument("--company", default="", help="Company name")
    args = parser.parse_args()
    url = args.url.rstrip("/")
    domain = re.sub(r"^https?://(www\.)?", "", url).split("/")[0].replace(".", "_")
    company = args.company or domain.replace("_", " ").title()
    out_dir = ENTREGABLES / domain
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"Auditing: {url}")
    print(f"Company: {company}")
    axe_data = run_axe(url, out_dir)
    violations = axe_data.get("violations", [])
    print(f"   Found {len(violations)} violations")

    buckets = classify(violations)
    score = calc_score(buckets)
    rl, rd = risk_info(score, len(buckets["critical"]))
    price = 800 if len(buckets["critical"]) <= 5 else 1200 if len(buckets["critical"]) <= 15 else 1800

    exec_sum = (
        f"Se identificaron {len(violations)} hallazgos de no-conformidad con WCAG 2.1 AA, "
        f"de los cuales {len(buckets['critical'])} presentan riesgo legal directo bajo ADA Title III. "
        f"Score de cumplimiento: {score}/100."
    )
    methodology = (
        "Escaneo automatizado (axe-core, WCAG 2.1 AA tags) + analisis semantico "
        "de roles ARIA, orden de tabulacion, contraste y contenido no-texto."
    )
    consequences = (
        "<ul>"
        "<li><strong>Demandas drive-by:</strong> costo extrajudicial USD 10.000-75.000.</li>"
        "<li><strong>Prdida de mercado:</strong> 26% de adultos en EE.UU. reporta discapacidad (CDC).</li>"
        "<li><strong>SEO:</strong> Google penaliza mala semantica y bajo contraste.</li>"
        "</ul>"
    )
    pricing_note = (
        f"{'Incluye remediacion completa de ' + str(len(buckets['critical'])) + ' hallazgos criticos + ' + str(len(buckets['serious'])) + ' altos. ' if buckets['critical'] or buckets['serious'] else ''}"
        "Testing manual con NVDA + VoiceOver. Declaracion de accesibilidad publicada. "
        "30 dias de soporte post-entrega."
    )

    context = {
        "company": company,
        "url": url,
        "date": date.today().strftime("%d/%m/%Y"),
        "css_path": str(TEMPLATE_CSS),
        "score": score,
        "score_class": score_class(score),
        "score_desc": f"{'Riesgo critico' if score<30 else 'Riesgo alto' if score<60 else 'Riesgo moderado' if score<80 else 'Cumplimiento aceptable'}",
        "critical_count": len(buckets["critical"]),
        "serious_count": len(buckets["serious"]),
        "moderate_count": len(buckets["moderate"]),
        "total_count": len(violations),
        "executive_summary": exec_sum,
        "risk_level": rl,
        "risk_description": rd,
        "methodology": methodology,
        "findings": build_findings(buckets),
        "top3_issues": build_top3(buckets),
        "remediation_phases": build_remediation(buckets),
        "price": str(price),
        "pricing_note": pricing_note,
        "consequences": consequences,
        "compliance_table": build_compliance_table(axe_data),
    }

    html_tmpl = Template(TEMPLATE_HTML.read_text())
    html_out = html_tmpl.render(**context)
    html_path = out_dir / "auditoria.html"
    html_path.write_text(html_out)
    print(f"   HTML generated: {html_path}")

    pdf_path = out_dir / f"auditoria-{domain}.pdf"
    generate_pdf(html_path, TEMPLATE_CSS, pdf_path)
    print(f"   PDF generated: {pdf_path}")

    md_path = out_dir / "resumen-scan.json"
    summary = {
        "url": url, "company": company, "date": date.today().isoformat(),
        "score": score, "risk_level": rl,
        "violations": len(violations),
        "critical": len(buckets["critical"]), "serious": len(buckets["serious"]),
        "moderate": len(buckets["moderate"]), "minor": len(buckets["minor"]),
        "price": price
    }
    md_path.write_text(json.dumps(summary, indent=2, ensure_ascii=False))
    print(f"   Summary: {md_path}")
    print(f"\nDone! PDF ready at: {pdf_path}")
    return pdf_path

import shutil

def inject_css_into_html(html_path, css_path):
    """Inject CSS into HTML as a <style> tag to ensure styles are applied.
    
    Args:
        html_path: Path to the HTML file.
        css_path: Path to the CSS file.
        
    Returns:
        Path to the modified HTML file (temporary).
    """
    html_content = html_path.read_text()
    css_content = css_path.read_text()
    
    # Inject CSS into HTML
    modified_html = html_content.replace(
        '</head>',
        f'<style>{css_content}</style></head>'
    )
    
    # Create a temporary HTML file
    temp_html_path = html_path.with_suffix('.tmp.html')
    temp_html_path.write_text(modified_html)
    
    return temp_html_path

def generate_pdf(html_path, css_path, pdf_path):
    """Render an HTML audit report into a branded PDF using WeasyPrint.
    Falls back to wkhtmltopdf if WeasyPrint is not available.

    Args:
        html_path: Path to the rendered HTML file.
        css_path:  Path to the external stylesheet.
        pdf_path:  Destination path for the output PDF.

    Raises:
        FileNotFoundError: If neither WeasyPrint nor wkhtmltopdf are installed.
    """
    # Inject CSS into HTML
    temp_html_path = inject_css_into_html(html_path, css_path)
    
    # Try WeasyPrint first
    if shutil.which("weasyprint"):
        try:
            subprocess.run(["weasyprint", str(temp_html_path), str(pdf_path)], check=True)
            temp_html_path.unlink()  # Clean up
            return
        except subprocess.CalledProcessError as e:
            print(f"WeasyPrint failed: {e}")
    
    # Fallback to wkhtmltopdf
    if shutil.which("wkhtmltopdf"):
        try:
            subprocess.run([
                "wkhtmltopdf",
                "--enable-local-file-access",
                str(temp_html_path), str(pdf_path)
            ], check=True)
            temp_html_path.unlink()  # Clean up
            return
        except subprocess.CalledProcessError as e:
            print(f"wkhtmltopdf failed: {e}")
    
    # Clean up and raise error
    temp_html_path.unlink()
    raise FileNotFoundError("Neither weasyprint nor wkhtmltopdf are installed.")

if __name__ == "__main__":
    main()
