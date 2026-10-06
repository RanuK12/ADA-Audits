"""Utility functions to estimate monetary impact and legal risk based on WCAG findings."""

from typing import Dict, List
import json

# Tabla de referencia para estimar impacto económico y riesgo legal
IMPACT_FACTORS = {
    "low_contrast": {"cost_per_user": 0.05, "legal_risk": "bajo", "description": "Pérdida de conversión por falta de contraste adecuado"},
    "missing_alt": {"cost_per_user": 0.10, "legal_risk": "medio", "description": "Pérdida de ventas y riesgo de demanda por imágenes sin texto alternativo"},
    "keyboard_trap": {"cost_per_user": 0.20, "legal_risk": "alto", "description": "Usuarios sin mouse no pueden navegar, riesgo de demanda ADA"},
    "aria_label_missing": {"cost_per_user": 0.08, "legal_risk": "bajo", "description": "Usuarios de lectores de pantalla pierden contexto"},
    "color_only_info": {"cost_per_user": 0.07, "legal_risk": "bajo", "description": "Usuarios daltónicos pierden información"},
    "focus_visible_missing": {"cost_per_user": 0.09, "legal_risk": "medio", "description": "Usuarios no ven dónde está el foco"},
    "heading_order": {"cost_per_user": 0.06, "legal_risk": "bajo", "description": "Estructura confusa para lectores de pantalla"},
    "form_label_missing": {"cost_per_user": 0.15, "legal_risk": "medio", "description": "Usuarios no saben qué ingresar en campos"},
    "table_headers_missing": {"cost_per_user": 0.12, "legal_risk": "medio", "description": "Datos tabulares ininteligibles para asistentes de tecnología"},
    "video_no_captions": {"cost_per_user": 0.30, "legal_risk": "alto", "description": "Exclusión de sordos y riesgo legal"},
}


def calculate_economic_impact(finding_code: str, visitors_per_month: int = 1000) -> float:
    """
    Calculate the estimated economic impact of a finding.
    Args:
        finding_code: The code of the finding (e.g., 'missing_alt').
        visitors_per_month: Number of visitors per month to the site.
    Returns:
        Estimated monthly economic impact in USD.
    """
    if finding_code in IMPACT_FACTORS:
        factor = IMPACT_FACTORS[finding_code]
        monthly_loss = visitors_per_month * factor["cost_per_user"]
        return int(round(monthly_loss))  # Convertir a entero y redondear
    else:
        return 0  # Valor por defecto si no hay datos


def calculate_legal_risk(finding_code: str, severity: str) -> str:
    """
    Calculate the legal risk level for a finding based on its severity.
    Args:
        finding_code: The code of the finding (e.g., 'missing_alt').
        severity: The severity level (e.g., 'high', 'medium', 'low').
    Returns:
        Legal risk level as a string (e.g., 'alto', 'moderado', 'bajo').
    """
    if severity.lower() == "critical":
        return "alto"
    elif severity.lower() == "high":
        return "moderado"
    elif severity.lower() == "medium":
        return "medio"
    else:
        return "bajo"


def estimate_cost(finding_code: str, severity: str, visitors_per_month: int = 1000) -> float:
    """
    Estimate the economic impact for a finding.
    Args:
        finding_code: The code of the finding (e.g., 'missing_alt').
        severity: The severity level (not used in calculation, but kept for consistency).
        visitors_per_month: Number of visitors per month to the site.
    Returns:
        Estimated monthly economic impact in USD.
    """
    return calculate_economic_impact(finding_code, visitors_per_month)