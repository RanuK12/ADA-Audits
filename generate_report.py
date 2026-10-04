import sys
sys.path.insert(0, '.')
import json
from datetime import datetime
from impact import IMPACT_MAP

def generate_report(data):
    report = []
    report.append(f"# Auditoría de Accesibilidad WCAG: {data['client_name']}")
    report.append(f"**Fecha:** {data['date']}")
    report.append(f"**Estado:** Finalizado")
    report.append("\n## Resumen Ejecutivo")
    report.append(f"{data['summary']}")
    
    if data['findings']:
        report.append("\n## Hallazgos Detallados")
        report.append("| Hallazgo | Severidad | Impacto económico | Riesgo legal |")
        report.append("| --- | --- | --- | --- |")
        
        for item in data['findings']:
            # Derive a code from the issue string if not provided
            code = item.get('code', item['issue'].lower().replace(' ', '_').replace('-', '_'))
            impact = IMPACT_MAP.get(code, {"cost": "N/D", "risk": "N/D"})
            report.append(f"| {item['issue']} | {item['severity']} | {impact['cost']} | {impact['risk']} |")
        
        # Antes → Después sub‑sections
        for item in data['findings']:
            report.append(f"\n### {item['issue']}")
            report.append(f"**Impacto en el negocio:** {item['business_impact']}")
            report.append("**Antes → Después**")
            report.append(f"**Antes:** {item['before']}")
            report.append(f"**Después:** {item['after']}")
            # CTA por hallazgo
            code = item.get('code', item['issue'].lower().replace(' ', '_').replace('-', '_'))
            impact = IMPACT_MAP.get(code, {"cost": "N/D", "risk": "N/D"})
            report.append(f"💡 **Impacto estimado:** {impact['cost']} | **Riesgo:** {impact['risk']}")
            report.append(f"👉 Contrate el fix para este issue: https://ada-audits.example.com/quote?issue={code}")
    
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
                "after": "`<button style=\"background: #D2691E; color: #FFFFFF;\">Comprar</button>` (contraste 4.5:1)"
            },
            {
                "code": "missing_alt",
                "issue": "Imágenes de producto sin alt text",
                "severity": "Medium",
                "business_impact": "Lectores de pantalla no pueden describir los productos → pérdida de ventas y riesgo de demanda",
                "before": "`<img src=\"producto.jpg\">`",
                "after": "`<img src=\"producto.jpg\" alt=\"Zapatillas running azul\">`"
            },
            {
                "code": "keyboard_trap",
                "issue": "Menú de navegación no operable por teclado",
                "severity": "Critical",
                "business_impact": "Usuarios sin mouse no pueden navegar → abandono del sitio y posible demanda ADA",
                "before": "`<div class=\"menu\" onclick=\"toggleMenu()\">` (sin `tabindex` ni `role`)",
                "after": "`<nav aria-label=\"Principal\"><ul role=\"menubar\">…</ul></nav>` con manejo de teclado"
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