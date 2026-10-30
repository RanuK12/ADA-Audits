"""Utility functions to estimate monetary impact and legal risk based on WCAG findings."""

from typing import Dict, List
import json

# Tabla de referencia para estimar impacto económico y riesgo legal
IMPACT_FACTORS = {
    # Problemas de percepción
    "low_contrast": {"cost_per_user": 0.05, "legal_risk": "bajo", "description": "Pérdida de conversión por falta de contraste adecuado"},
    "missing_alt": {"cost_per_user": 0.10, "legal_risk": "medio", "description": "Pérdida de ventas y riesgo de demanda por imágenes sin texto alternativo"},
    "color_only_info": {"cost_per_user": 0.07, "legal_risk": "bajo", "description": "Usuarios daltónicos pierden información"},
    
    # Problemas de operación
    "keyboard_trap": {"cost_per_user": 0.20, "legal_risk": "alto", "description": "Usuarios sin mouse no pueden navegar, riesgo de demanda ADA"},
    "focus_visible_missing": {"cost_per_user": 0.09, "legal_risk": "medio", "description": "Usuarios no ven dónde está el foco"},
    "keyboard_navigation_inconsistent": {"cost_per_user": 0.11, "legal_risk": "medio", "description": "Navegación por teclado incoherente"},
    
    # Problemas de comprensión
    "heading_order": {"cost_per_user": 0.06, "legal_risk": "bajo", "description": "Estructura confusa para lectores de pantalla"},
    "form_label_missing": {"cost_per_user": 0.15, "legal_risk": "medio", "description": "Usuarios no saben qué ingresar en campos"},
    "table_headers_missing": {"cost_per_user": 0.12, "legal_risk": "medio", "description": "Datos tabulares ininteligibles para asistentes de tecnología"},
    "language_missing": {"cost_per_user": 0.08, "legal_risk": "bajo", "description": "No se define el idioma principal del documento"},
    
    # Problemas de robustez
    "video_no_captions": {"cost_per_user": 0.30, "legal_risk": "alto", "description": "Exclusión de sordos y riesgo legal"},
    "audio_no_transcript": {"cost_per_user": 0.25, "legal_risk": "alto", "description": "Exclusión de sordos y riesgo legal"},
    "time_limits_missing": {"cost_per_user": 0.14, "legal_risk": "medio", "description": "Usuarios con discapacidad cognitiva no pueden completar tareas"},
    
    # Problemas críticos
    "aria_label_missing": {"cost_per_user": 0.18, "legal_risk": "alto", "description": "Usuarios de lectores de pantalla pierden acceso al contenido"},
    "link_ambiguous": {"cost_per_user": 0.13, "legal_risk": "medio", "description": "Enlaces genéricos como 'click aquí' confunden usuarios"},
    "skip_navigation_missing": {"cost_per_user": 0.16, "legal_risk": "medio", "description": "Usuarios no pueden saltar contenido repetitivo"},
}


def calculate_economic_impact(findings: List[Dict], visitors_per_month: int = 1000) -> Dict[str, float]:
    """
    Calculate the estimated economic impact of findings.
    Args:
        findings: List of findings with 'code' key.
        visitors_per_month: Number of visitors per month to the site.
    Returns:
        Dict with total economic impact and breakdown by finding.
    """
    total_impact = 0.0
    impact_by_finding = {}
    
    for finding in findings:
        finding_code = finding.get('code', '').lower()
        if finding_code in IMPACT_FACTORS:
            factor = IMPACT_FACTORS[finding_code]
            monthly_loss = visitors_per_month * factor["cost_per_user"]
            total_impact += monthly_loss
            impact_by_finding[finding_code] = {
                "cost": f"${monthly_loss:,.2f}",
                "risk": factor["legal_risk"],
                "description": factor["description"]
            }
        else:
            impact_by_finding[finding_code] = {
                "cost": "$N/D",
                "risk": "N/D",
                "description": "No data available"
            }
    
    return {
        "total": f"${total_impact:,.2f}",
        "breakdown": impact_by_finding
    }


def calculate_legal_risk(findings: List[Dict]) -> Dict[str, str]:
    """
    Calculate the legal risk level for each finding.
    Args:
        findings: List of findings with 'code' key.
    Returns:
        Dict with legal risk breakdown by finding.
    """
    legal_risk_by_finding = {}
    
    for finding in findings:
        finding_code = finding.get('code', '').lower()
        if finding_code in IMPACT_FACTORS:
            factor = IMPACT_FACTORS[finding_code]
            legal_risk_by_finding[finding_code] = factor["legal_risk"]
        else:
            legal_risk_by_finding[finding_code] = "N/D"
    
    return legal_risk_by_finding


def generate_impact_explanation(finding_code: str, visitors_per_month: int = 1000) -> str:
    """
    Generate a one-line explanation of economic impact and legal risk for a finding.
    Args:
        finding_code: The code of the finding.
        visitors_per_month: Number of visitors per month to the site.
    Returns:
        One-line explanation string.
    """
    finding_code = finding_code.lower()
    if finding_code in IMPACT_FACTORS:
        factor = IMPACT_FACTORS[finding_code]
        monthly_loss = visitors_per_month * factor["cost_per_user"]
        risk_text = {
            "bajo": "riesgo legal bajo",
            "medio": "riesgo legal medio", 
            "alto": "riesgo legal alto"
        }.get(factor["legal_risk"], factor["legal_risk"])
        
        return f"Costo estimado: ${monthly_loss:,.2f}/mes, {risk_text} - {factor['description']}"
    else:
        return f"Sin datos de impacto para: {finding_code}"


def estimate_impact(findings: List[Dict], visitors_per_month: int = 1000) -> List[Dict]:
    """
    Estimate the economic impact and legal risk for each finding.
    Args:
        findings: List of findings with 'code' key.
        visitors_per_month: Number of visitors per month to the site.
    Returns:
        List of dicts with impact and risk info for each finding.
    """
    economic_impact = calculate_economic_impact(findings, visitors_per_month)
    legal_risk = calculate_legal_risk(findings)
    
    result = []
    for finding in findings:
        finding_code = finding.get('code', '').lower()
        result.append({
            "code": finding_code,
            "economic_impact": economic_impact['breakdown'].get(finding_code, {"cost": "$N/D"})["cost"],
            "legal_risk": legal_risk.get(finding_code, "N/D"),
            "description": economic_impact['breakdown'].get(finding_code, {"description": "No data available"})["description"],
            "impact_explanation": generate_impact_explanation(finding_code, visitors_per_month)
        })
    
    return result