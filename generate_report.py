import sys
sys.path.insert(0, '.')
import json
from datetime import datetime
import os
from utils.economic_impact import estimate_impact, calculate_economic_impact

def format_findings(findings, visitors_per_month=1000):
    """Return list of dicts with impact, before_after, cta for each finding."""
    impact_results = estimate_impact(findings, visitors_per_month)
    formatted = []
    for item in findings:
        code = item.get('code', item['issue'].lower().replace(' ', '_').replace('-', '_'))
        impact_info = next((impact for impact in impact_results if impact['code'] == code), {"economic_impact": "N/D", "legal_risk": "N/D", "impact_explanation": "N/D"})
        formatted.append({
            "economic_impact": impact_info.get('economic_impact', 'N/D'),
            "legal_risk": impact_info.get('legal_risk', 'N/D'),
            "impact_explanation": impact_info.get('impact_explanation', 'N/D'),
            "before_after": item.get('before_after_image', ''),
            "cta": "Contratar fix: [Contacto](mailto:emilio@ranuk.dev)"
        })
    return formatted

def generate_report(data, output_format='markdown', visitors_per_month=1000):
    report = []
    report.append(f"# Auditoría de Accesibilidad WCAG: {data['client_name']}")
    report.append(f"**Fecha:** {data['date']}")
    report.append(f"**Estado:** Finalizado")
    report.append("\n## Resumen Ejecutivo")
    report.append(f"{data['summary']}")
    
    if data['findings']:
        formatted = format_findings(data['findings'], visitors_per_month)
        
        # Calcular impacto económico total
        impact_data = calculate_economic_impact(data['findings'], visitors_per_month)
        total_monthly_loss = impact_data['total']
        
        # ROI: estimar costo de fix vs pérdida mensual
        estimated_fix_cost = len(data['findings']) * 150  # $150 por fix promedio
        monthly_savings = float(total_monthly_loss.replace('$', '').replace(',', ''))
        roi_months = estimated_fix_cost / monthly_savings if monthly_savings > 0 else 0
        annual_savings = monthly_savings * 12
        
        report.append(f"\n## 💰 Impacto Económico Total")
        report.append(f"- **Pérdida estimada mensual:** {total_monthly_loss}")
        report.append(f"- **Ahorro anual potencial:** ${annual_savings:,.2f}")
        report.append(f"- **Inversión estimada en fixes:** ${estimated_fix_cost:,}")
        report.append(f"- **ROI estimado:** {roi_months:.1f} meses para recuperar la inversión")
        report.append(f"- **ROI anual:** {((annual_savings - estimated_fix_cost) / estimated_fix_cost * 100):.0f}%")
        
        # Visual comparison section
        report.append(f"\n## 🎯 Comparativa Visual: Antes vs Después")
        report.append(f"![Antes vs Después - Accesibilidad](assets/images/before_after.png)")
        report.append(f"*La imagen muestra la diferencia visual entre un sitio con barreras de accesibilidad (izquierda) y el mismo sitio corregido según WCAG 2.1 AA (derecha).*")
        
        report.append("\n## Hallazgos Detallados")
        report.append("| Hallazgo | Severidad | Impacto Económico | Riesgo Legal | Explicación |")
        report.append("| --- | --- | --- | --- | --- |")
        
        for idx, item in enumerate(data['findings']):
            report.append(f"| {item['issue']} | {item['severity']} | {formatted[idx]['economic_impact']} | {formatted[idx]['legal_risk']} | {formatted[idx]['impact_explanation']} |")
        
        # Antes → Después sub‑sections with CTA
        for idx, item in enumerate(data['findings']):
            report.append(f"\n### {item['issue']}")
            report.append(f"**Impacto en el negocio:** {item['business_impact']}")
            report.append(f"**Explicación de impacto:** {formatted[idx]['impact_explanation']}")
            report.append("**Antes → Después**")
            report.append(f"**Antes:** {item['before']}")
            report.append(f"**Después:** {item['after']}")
            # CTA por hallazgo
            report.append(formatted[idx]['cta'])
            # Show before/after image reference
            report.append(f"![Antes/Después]({formatted[idx]['before_after']})")
    
    if data['recommendations']:
        report.append("\n## Recomendaciones")
        for rec in data['recommendations']:
            report.append(f"- {rec}")
    
    # CTA fijo al final
    report.append(f"\n💡 Arreglamos esto por vos — [contratá el fix](mailto:emilio@ranuk.dev)")
    
    return "\n".join(report)

def main():
    sample_data = {
        "client_name": "TiendaOnline Demo",
        "date": datetime.now().strftime("%Y-%m-%d"),
        "summary": "Auditoría de accesibilidad WCAG 2.1 AA — se detectaron barreras que afectan la experiencia de usuarios con discapacidad y exponen a la empresa a riesgos legales.",
        "findings": [
            {
                "code": "low_contrast",
                "issue": "Contraste bajo en botón de compra",
                "severity": "High",
                "business_impact": "–12% conversión mobile / demanda ADA Title III",
                "before": "`<button style=\"background: #FFA500; color: #FFFFFF;\">Comprar</button>` (contraste 2.1:1)",
                "after": "`<button style=\"background: #D2691E; color: #FFFFFF;\">Comprar</button>` (contraste 4.5:1)",
                "before_after_image": "before_after_low_contrast.png"
            },
            {
                "code": "missing_alt",
                "issue": "Imágenes de producto sin alt text",
                "severity": "Medium",
                "business_impact": "Lectores de pantalla no pueden describir los productos → pérdida de ventas y riesgo de demanda",
                "before": "`<img src=\"producto.jpg\">`",
                "after": "`<img src=\"producto.jpg\" alt=\"Zapatillas running azul\">`",
                "before_after_image": "before_after_missing_alt.png"
            },
            {
                "code": "keyboard_trap",
                "issue": "Menú de navegación no operable por teclado",
                "severity": "Critical",
                "business_impact": "Usuarios sin mouse no pueden navegar → abandono del sitio y posible demanda ADA",
                "before": "`<div class=\"menu\" onclick=\"toggleMenu()\">` (sin `tabindex` ni `role`)",
                "after": "`<nav aria-label=\"Principal\"><ul role=\"menubar\">…</ul></nav>` con manejo de teclado",
                "before_after_image": "before_after_keyboard_trap.png"
            }
        ],
        "recommendations": [
            "Corregir contraste de color en botones y elementos interactivos para cumplir WCAG 2.1 AA (mínimo 4.5:1).",
            "Agregar texto alternativo descriptivo a todas las imágenes de producto.",
            "Hacer el menú de navegación operable por teclado usando roles ARIA y gestión de foco."
        ]
    }
    
    report_content = generate_report(sample_data)
    with open("sample_audit_report.md", "w") as f:
        f.write(report_content)
    print("Reporte generado en sample_audit_report.md")

if __name__ == "__main__":
    main()