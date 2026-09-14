import json
import os
import sys
from datetime import datetime

# Commercial impact mapping (rule_id -> (amount, risk))
IMPACT = {
    "contraste_bajo_en_boton_de_compra": ("$5 k", "Posible demanda por accesibilidad"),
    "imagenes_de_producto_sin_alt_text": ("$3 k", "Pérdida de ventas y riesgo de demanda"),
    "menu_de_navegacion_no_opercable_por_teclado": ("$8 k", "Abandono del sitio y posible demanda ADA"),
}

def impact_text(rule_id):
    """Return (amount, risk) for a given rule_id, or default."""
    return IMPACT.get(rule_id, ("N/D", "Riesgo legal desconocido"))

def generate_report(data):
    report = []
    report.append(f"# Auditoría de Accesibilidad WCAG: {data['client_name']}")
    report.append(f"**Fecha:** {data['date']}")
    report.append(f"**Estado:** Finalizado")
    report.append("\n## Resumen Ejecutivo")
    report.append(f"{data['summary']}")
    
    if data['findings']:
        report.append("\n## Hallazgos Detallados")
        report.append("| Hallazgo | Severidad | Impacto en el negocio |")
        report.append("| --- | --- | --- |")
        
        for item in data['findings']:
            report.append(f"| {item['issue']} | {item['severity']} | {item['business_impact']} |")
        
        # Antes → Después sub‑sections
        for item in data['findings']:
            report.append(f"\n### {item['issue']}")
            report.append(f"**Impacto en el negocio:** {item['business_impact']}")
            # Commercial impact line
            rule_id = item.get('rule', item['issue'].lower().replace(' ', '_'))
            amount, risk = impact_text(rule_id)
            report.append(f"**Impacto comercial:** {amount} – {risk}")
            report.append("**Antes → Después**")
            report.append(f"**Antes:** {item['before']}")
            report.append(f"**Después:** {item['after']}")
            # CTA per finding
            report.append(f"[Contratar solución](https://ada.com/quote?rule={rule_id})")
    
    if data['recommendations']:
        report.append("\n## Recomendaciones")
        for rec in data['recommendations']:
            report.append(f"- {rec}")
    
    # CTA fijo al final
    report.append("\n💡 Arreglamos esto por vos — [contratá el fix](mailto:emilio@ranuk.dev)")
    
    return "\n".join(report)

def main():
    # If arguments provided: input JSON and output file
    if len(sys.argv) >= 3:
        input_path = sys.argv[1]
        output_path = sys.argv[2]
        with open(input_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    else:
        # Default sample data for backward compatibility
        data = {
            "client_name": "TiendaOnline Demo",
            "date": datetime.now().strftime("%Y-%m-%d"),
            "summary": "Auditoría de accesibilidad WCAG 2.1 AA — se detectaron barreras que afectan la experiencia de usuarios con discapacidad y exponen a la empresa a riesgos legales.",
            "findings": [
                {
                    "issue": "Contraste bajo en botón de compra",
                    "severity": "High",
                    "business_impact": "–12% conversión mobile / demanda ADA Title III",
                    "before": "`<button style=\"background: #FFA500; color: #FFFFFF;\">Comprar</button>` (contraste 2.1:1)",
                    "after": "`<button style=\"background: #D2691E; color: #FFFFFF;\">Comprar</button>` (contraste 4.5:1)"
                },
                {
                    "issue": "Imágenes de producto sin alt text",
                    "severity": "Medium",
                    "business_impact": "Lectores de pantalla no pueden describir los productos → pérdida de ventas y riesgo de demanda",
                    "before": "`<img src=\"producto.jpg\">`",
                    "after": "`<img src=\"producto.jpg\" alt=\"Zapatillas running azul\">`"
                },
                {
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
        # Ensure rule field
        for item in data['findings']:
            if 'rule' not in item:
                item['rule'] = item['issue'].lower().replace(' ', '_')
    
    report_content = generate_report(data)
    with open(output_path if len(sys.argv) >= 3 else "sample_audit_report.md", 'w', encoding='utf-8') as f:
        f.write(report_content)
    if len(sys.argv) >= 3:
        print(f"Reporte generado en {output_path}")
    else:
        print("Reporte generado en sample_audit_report.md")

if __name__ == "__main__":
    main()