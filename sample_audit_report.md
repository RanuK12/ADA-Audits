# Auditoría de Accesibilidad WCAG: TiendaOnline Demo
**Fecha:** 2026-09-27
**Estado:** Finalizado

## Resumen Ejecutivo
Auditoría de accesibilidad WCAG 2.1 AA — se detectaron barreras que afectan la experiencia de usuarios con discapacidad y exponen a la empresa a riesgos legales.

## Hallazgos Detallados
| Hallazgo | Severidad | Impacto | Antes/Después | CTA |
| --- | --- | --- | --- | --- |
| Contraste bajo en botón de compra | High | –12% conversión mobile / demanda ADA Title III | <div style="display:flex;gap:12px;"><img src="assets/before_1.png" alt="Antes" style="max-width:180px;border:1px solid #ddd;border-radius:4px;"><img src="assets/after_1.png" alt="Después" style="max-width:180px;border:1px solid #ddd;border-radius:4px;"></div> | [Contratar fix](mailto:emilio@ranuk.dev) |
| Imágenes de producto sin alt text | Medium | Lectores de pantalla no pueden describir los productos → pérdida de ventas y riesgo de demanda | <div style="display:flex;gap:12px;"><img src="assets/before_2.png" alt="Antes" style="max-width:180px;border:1px solid #ddd;border-radius:4px;"><img src="assets/after_2.png" alt="Después" style="max-width:180px;border:1px solid #ddd;border-radius:4px;"></div> | [Contratar fix](mailto:emilio@ranuk.dev) |
| Menú de navegación no operable por teclado | Critical | Usuarios sin mouse no pueden navegar → abandono del sitio y posible demanda ADA | <div style="display:flex;gap:12px;"><img src="assets/before_3.png" alt="Antes" style="max-width:180px;border:1px solid #ddd;border-radius:4px;"><img src="assets/after_3.png" alt="Después" style="max-width:180px;border:1px solid #ddd;border-radius:4px;"></div> | [Contratar fix](mailto:emilio@ranuk.dev) |

## Recomendaciones
- Corregir contraste de color en botones y elementos interactivos para cumplir WCAG 2.1 AA (mínimo 4.5:1).
- Agregar texto alternativo descriptivo a todas las imágenes de producto.
- Hacer el menú de navegación operable por teclado usando roles ARIA y gestión de foco.

💡 Arreglamos esto por vos — [contratá el fix](mailto:emilio@ranuk.dev)