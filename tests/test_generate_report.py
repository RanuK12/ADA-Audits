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
            {"issue": "Hallazgo 1", "severity": "High", "impact": "Impacto 1"},
            {"issue": "Hallazgo 2", "severity": "Medium", "impact": "Impacto 2"}
        ],
        "recommendations": [
            "Recomendación 1",
            "Recomendación 2"
        ]
    }
    
    report = generate_report(sample_data)
    
    # Verificar títulos
    assert "# Auditoría de Seguridad: Test Client" in report
    assert "## Resumen Ejecutivo" in report
    assert "## Hallazgos Detallados" in report
    assert "## Recomendaciones" in report
    
    # Verificar tabla de hallazgos
    assert "| Hallazgo | Severidad | Impacto |" in report
    assert "| --- | --- | --- |" in report
    assert "| Hallazgo 1 | High | Impacto 1 |" in report
    assert "| Hallazgo 2 | Medium | Impacto 2 |" in report
    
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
    assert "| Hallazgo | Severidad | Impacto |" not in report
    
    # Verificar que la sección de recomendaciones SÍ esté presente
    assert "## Recomendaciones" in report
    assert "- Recomendación 1" in report


def test_generate_report_empty_recommendations():
    """Verifica que el reporte no incluya la sección de recomendaciones si no hay recomendaciones."""
    sample_data = {
        "client_name": "Test Client",
        "date": "2026-07-12",
        "summary": "Resumen de prueba.",
        "findings": [{"issue": "Hallazgo 1", "severity": "High", "impact": "Impacto 1"}],
        "recommendations": []
    }
    
    report = generate_report(sample_data)
    
    # Verificar que la sección de recomendaciones NO esté presente
    assert "## Recomendaciones" not in report
    
    # Verificar que la sección de hallazgos SÍ esté presente
    assert "## Hallazgos Detallados" in report
    assert "| Hallazgo 1 | High | Impacto 1 |" in report


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