import json
from datetime import datetime

def generate_report(data):
    report = []
    report.append(f"# Auditoría de Accesibilidad WCAG: {data['client_name']}")
    report.append(f"**Fecha:** {data['date']}")
    report.append(f"**Estado:** Finalizado")
    report.append("\n## Resumen Ejecutivo")
    report.append(f"{data['summary']}")
    
    if data['findings']:
        report.append("\n## Hallazgos Detallados")
        report.append("| Hallazgo | Severidad | Impacto en el negocio | Impacto financiero estimado |")
        report.append("| --- | --- | --- | --- |")
        
        for item in data['findings']:
            # Estimar impacto financiero basado en severidad y tipo de hallazgo
            impacto_financiero = "No estimado"
            severidad = item.get('severity', '').lower()
            issue_texto = item.get('issue', '').lower()
            # Lógica simple de estimación financiera
            if 'contraste' in issue_texto or 'color' in issue_texto:
                impacto_financiero = "$500 - $2,000 (pérdida de conversiones)"
            elif 'navegación' in issue_texto or 'menu' in issue_texto or 'teclado' in issue_texto:
                impacto_financiero = "$1,000 - $5,000 (abandono de sitio)"
            elif 'formulario' in issue_texto or 'input' in issue_texto or 'alt text' in issue_texto or 'imagen' in issue_texto:
                impacto_financiero = "$1,500 - $3,000 (pérdida de leads/ventas)"
            elif 'encabezado' in issue_texto or 'heading' in issue_texto:
                impacto_financiero = "$400 - $1,800 (usabilidad y retención)"
            elif severidad in ['critical', 'high']:
                impacto_financiero = "$2,000 - $10,000 (riesgo legal y pérdida significativa)"
            elif severidad == 'medium':
                impacto_financiero = "$500 - $3,000 (mejora de experiencia y retención)"
            else:
                impacto_financiero = "$100 - $1,000 (mejora menor)"
            report.append(f"| {item['issue']} | {item['severity']} | {item['business_impact']} | {impacto_financiero} |")
        
        # Antes → Después sub‑sections
        for item in data['findings']:
            report.append(f"\n### {item['issue']}")
            report.append(f"**Impacto en el negocio:** {item['business_impact']}")
            report.append("**Antes → Después**")
            report.append(f"**Antes:** {item['before']}")
            report.append(f"**Después:** {item['after']}")
    
    if data['recommendations']:
        report.append("\n## Recomendaciones")
        for rec in data['recommendations']:
            report.append(f"- {rec}")
    
    # CTA mejorado con estimado de precio y llamado a la acción más directo
    total_estimado = "Consultá nuestro presupuesto personalizado (ej: arreglos básicos desde $800, auditoría completa + fix desde $1500)"
    report.append(f"\n💡 **¿Listo para hacer tu sitio accesible y evitar demandas?**")
    report.append(f"Arreglamos estos problemas por vos. Presupuesto estimado: {total_estimado}.")
    report.append(f"👉 [Contratá el servicio de fix ahora](mailto:emilio@ranuk.dev?subject=Auditoría%20y%20Fix%20de%20Accesibilidad)")
    
    return "\n".join(report)

def main():
    sample_data = {
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
    
    report_content = generate_report(sample_data)
    with open("sample_audit_report.md", "w") as f:
        f.write(report_content)
    print("Reporte generado en sample_audit_report.md")

if __name__ == "__main__":
    main()
