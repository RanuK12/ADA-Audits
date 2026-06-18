#!/usr/bin/env python3
"""Generate a professional Markdown audit report from a dictionary of audit data."""

from typing import Dict, List, Any

def generate_report(data: Dict[str, Any]) -> str:
    """
    Generate a Markdown report string from the given audit data dictionary.

    Expected keys:
        - client_name (str)
        - date (str)
        - findings (list of dicts) each with keys:
            - issue (str)
            - severity (str) e.g., Critical, High, Medium, Low
            - impact (str)
        - recommendations (list of str)

    Returns:
        str: The formatted Markdown report.
    """
    client_name = data.get("client_name", "Unknown Client")
    date = data.get("date", "Unknown Date")
    findings: List[Dict[str, str]] = data.get("findings", [])
    recommendations: List[str] = data.get("recommendations", [])

    lines: List[str] = []

    # Header
    lines.append(f"# Auditoría de Accesibilidad Web – {client_name}")
    lines.append("")
    lines.append(f"**Fecha:** {date}")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Summary
    lines.append("## Resumen")
    lines.append("")
    total_findings = len(findings)
    critical = sum(1 for f in findings if f.get("severity", "").lower() == "critical")
    high = sum(1 for f in findings if f.get("severity", "").lower() == "high")
    medium = sum(1 for f in findings if f.get("severity", "").lower() == "medium")
    low = sum(1 for f in findings if f.get("severity", "").lower() == "low")
    lines.append(
        f"Se identificaron **{total_findings}** hallazgos: "
        f"{critical} críticos, {high} altos, {medium} medios, {low} bajos."
    )
    lines.append("")

    # Detailed Findings table
    lines.append("## Hallazgos Detallados")
    lines.append("")
    lines.append("| # | Problema | Severidad | Impacto |")
    lines.append("|---|----------|-----------|---------|")
    for idx, finding in enumerate(findings, start=1):
        issue = finding.get("issue", "")
        severity = finding.get("severity", "")
        impact = finding.get("impact", "")
        # Escape pipe characters in fields
        issue = issue.replace("|", "\\|")
        severity = severity.replace("|", "\\|")
        impact = impact.replace("|", "\\|")
        lines.append(f"| {idx} | {issue} | {severity} | {impact} |")
    lines.append("")

    # Recommendations
    lines.append("## Recomendaciones")
    lines.append("")
    if recommendations:
        for rec in recommendations:
            # Escape leading dash if any
            rec = rec.replace("|", "\\|")
            lines.append(f"- {rec}")
    else:
        lines.append("*No se proporcionaron recomendaciones.*")
    lines.append("")

    # Footer
    lines.append("---")
    lines.append("")
    lines.append("*Reporte generado automáticamente.*")

    return "\n".join(lines)


def main() -> None:
    """Demonstrate usage of generate_report with sample data."""
    sample_data: Dict[str, Any] = {
        "client_name": "Ejemplo S.A.",
        "date": "2026-06-18",
        "findings": [
            {
                "issue": "Contraste insuficiente en botones",
                "severity": "High",
                "impact": "Usuarios con baja visión no pueden leer el texto."
            },
            {
                "issue": "Falta de etiquetas ARIA en formularios",
                "severity": "Critical",
                "impact": "Lectores de pantalla no identifican campos."
            },
            {
                "issue": "Imágenes sin texto alternativo",
                "severity": "Medium",
                "impact": "Información visual no accesible."
            }
        ],
        "recommendations": [
            "Aumentar el contraste de color a una relación de al menos 4.5:1.",
            "Agregar atributos aria-label a todos los campos de formulario.",
            "Incluir texto alternativo descriptivo en todas las imágenes relevantes."
        ]
    }

    report = generate_report(sample_data)
    print(report)


if __name__ == "__main__":
    main()
