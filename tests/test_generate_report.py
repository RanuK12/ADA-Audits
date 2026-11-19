# Tests unitarios para generate_report.py
import pytest
from generate_report import generate_report
from datetime import datetime


def test_generate_report_structure():
    """Verifica que el reporte tenga la estructura esperada: títulos, tablas y listas."""
    sample_data = {
        "client_name": "Test Client",
        "date": "2026-07-12",
        "summary": "Resumen de prueba.",
        "findings": [
            {
                "issue": "Hallazgo 1",
                "severity": "High",
                "business_impact": "Impacto 1",
                "before": "antes 1",
                "after": "después 1",
                "economic_impact": "$1.200/mes",
                "legal_risk": "Riesgo ADA Title III",
                "impact_explanation": "Cada hallazgo explica su impacto en plata o riesgo legal en una línea.",
            },
            {
                "issue": "Hallazgo 2",
                "severity": "Medium",
                "business_impact": "Impacto 2",
                "before": "antes 2",
                "after": "después 2",
                "economic_impact": "$400/mes",
                "legal_risk": "Bajo",
                "impact_explanation": "Cada hallazgo explica su impacto en plata o riesgo legal en una línea.",
            }
        ],
        "recommendations": [
            "Recomendación 1",
            "Recomendación 2"
        ]
    }

    report = generate_report(sample_data)

    # Verificar títulos
    assert "# Auditoría de Accesibilidad WCAG: Test Client" in report
    assert "## Resumen Ejecutivo" in report
    assert "## Hallazgos Detallados" in report
    assert "## Recomendaciones" in report

    # Verificar tabla de hallazgos (5 columnas: Hallazgo | Severidad | Impacto Económico | Riesgo Legal | Explicación)
    assert "| Hallazgo | Severidad | Impacto Económico | Riesgo Legal | Explicación |" in report
    assert "| --- | --- | --- | --- | --- |" in report
    assert "| Hallazgo 1 | High | $1.200/mes | Riesgo ADA Title III | Cada hallazgo explica su impacto en plata o riesgo legal en una línea. |" in report
    assert "| Hallazgo 2 | Medium | $400/mes | Bajo | Cada hallazgo explica su impacto en plata o riesgo legal en una línea. |" in report

    # Verificar que cada hallazgo incluye impacto económico, riesgo legal y explicación de impacto
    assert "$1.200/mes" in report
    assert "$400/mes" in report
    assert "Riesgo ADA Title III" in report
    assert "Bajo" in report
    assert "Cada hallazgo explica su impacto en plata o riesgo legal en una línea." in report

    # Verificar recomendaciones
    assert "- Recomendación 1" in report
    assert "- Recomendación 2" in report


def test_generate_report_empty_findings():
    """Verifica que el reporte no incluya la sección de hallazgos si no hay hallazgos."""
    sample_data = {
        "client_name": "Test Client",
        "date": "2026-07-12",
        "summary": "Resumen de prueba.",
        "findings": [],
        "recommendations": ["Recomendación 1"]
    }

    report = generate_report(sample_data)

    # Verificar que la sección de hallazgos NO esté presente
    assert "## Hallazgos Detallados" not in report
    assert "| Hallazgo | Severidad | Impacto Económico | Riesgo Legal | Explicación |" not in report

    # Verificar que la sección de recomendaciones SÍ esté presente
    assert "## Recomendaciones" in report
    assert "- Recomendación 1" in report


def test_generate_report_empty_recommendations():
    """Verifica que el reporte no incluya la sección de recomendaciones si no hay recomendaciones."""
    sample_data = {
        "client_name": "Test Client",
        "date": "2026-07-12",
        "summary": "Resumen de prueba.",
        "findings": [
            {
                "issue": "Hallazgo 1",
                "severity": "High",
                "business_impact": "Impacto 1",
                "before": "antes 1",
                "after": "después 1",
                "economic_impact": "$1.200/mes",
                "legal_risk": "Riesgo ADA Title III",
                "impact_explanation": "Cada hallazgo explica su impacto en plata o riesgo legal en una línea.",
            }
        ],
        "recommendations": []
    }

    report = generate_report(sample_data)

    # Verificar que la sección de recomendaciones NO esté presente
    assert "## Recomendaciones" not in report

    # Verificar que la sección de hallazgos SÍ esté presente
    assert "## Hallazgos Detallados" in report
    assert "| Hallazgo 1 | High | $1.200/mes | Riesgo ADA Title III | Cada hallazgo explica su impacto en plata o riesgo legal en una línea. |" in report


def test_generate_report_date_format():
    """Verifica que la fecha en el reporte coincida con el formato esperado."""
    sample_data = {
        "client_name": "Test Client",
        "date": "2026-07-12",
        "summary": "Resumen de prueba.",
        "findings": [],
        "recommendations": []
    }

    report = generate_report(sample_data)
    assert "**Fecha:** 2026-07-12" in report
