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
            "description": economic_impact['breakdown'].get(finding_code, {"description": "No data available"})["description"]
        })
    
    return result