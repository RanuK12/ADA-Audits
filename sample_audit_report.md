# Auditoría de Accesibilidad WCAG: TiendaOnline Demo
**Fecha:** 2026-10-04
**Estado:** Finalizado

## Resumen Ejecutivo
Auditoría de accesibilidad WCAG 2.1 AA — se detectaron barreras que afectan la experiencia de usuarios con discapacidad y exponen a la empresa a riesgos legales.

## Hallazgos Detallados
| Hallazgo | Severidad | Impacto económico | Riesgo legal |
| --- | --- | --- | --- |
| Contraste bajo en botón de compra | High | $150–$300 | Deserción de usuarios |
| Imágenes de producto sin alt text | Medium | $200–$500 | Posible demanda por inaccesibilidad |
| Menú de navegación no operable por teclado | Critical | $500–$1000 | Demanda por falta de accesibilidad teclado |

### Contraste bajo en botón de compra
**Impacto en el negocio:** –12% conversión mobile / demanda ADA Title III
**Antes → Después**
**Antes:** `<button style="background: #FFA500; color: #FFFFFF;">Comprar</button>` (contraste 2.1:1)
**Después:** `<button style="background: #D2691E; color: #FFFFFF;">Comprar</button>` (contraste 4.5:1)
💡 **Impacto estimado:** $150–$300 | **Riesgo:** Deserción de usuarios
👉 Contrate el fix para este issue: https://ada-audits.example.com/quote?issue=low_contrast

### Imágenes de producto sin alt text
**Impacto en el negocio:** Lectores de pantalla no pueden describir los productos → pérdida de ventas y riesgo de demanda
**Antes → Después**
**Antes:** `<img src="producto.jpg">`
**Después:** `<img src="producto.jpg" alt="Zapatillas running azul">`
💡 **Impacto estimado:** $200–$500 | **Riesgo:** Posible demanda por inaccesibilidad
👉 Contrate el fix para este issue: https://ada-audits.example.com/quote?issue=missing_alt

### Menú de navegación no operable por teclado
**Impacto en el negocio:** Usuarios sin mouse no pueden navegar → abandono del sitio y posible demanda ADA
**Antes → Después**
**Antes:** `<div class="menu" onclick="toggleMenu()">` (sin `tabindex` ni `role`)
**Después:** `<nav aria-label="Principal"><ul role="menubar">…</ul></nav>` con manejo de teclado
💡 **Impacto estimado:** $500–$1000 | **Riesgo:** Demanda por falta de accesibilidad teclado
👉 Contrate el fix para este issue: https://ada-audits.example.com/quote?issue=keyboard_trap

## Recomendaciones
- Corregir contraste de color en botones y elementos interactivos para cumplir WCAG 2.1 AA (mínimo 4.5:1).
- Agregar texto alternativo descriptivo a todas las imágenes de producto.
- Hacer el menú de navegación operable por teclado usando roles ARIA y gestión de foco.

💡 Arreglamos esto por vos — [contratá el fix](mailto:emilio@ranuk.dev)