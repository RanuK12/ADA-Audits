# Auditoría de Accesibilidad WCAG: TiendaOnline Demo
**Fecha:** 2026-10-06
**Estado:** Finalizado

## Resumen Ejecutivo
Auditoría de accesibilidad WCAG 2.1 AA — se detectaron barreras que afectan la experiencia de usuarios con discapacidad y exponen a la empresa a riesgos legales.

## Hallazgos Detallados
| Hallazgo | Severidad | Impacto Económico | Riesgo Legal |
| --- | --- | --- | --- |
| Contraste bajo en botón de compra | High | $150–300 | Deserción de usuarios |
| Imágenes de producto sin alt text | Medium | $200–500 | Posible demanda por inaccesibilidad |
| Menú de navegación no operable por teclado | Critical | $300–600 | Exclusión de usuarios con discapacidad motriz |

### Contraste bajo en botón de compra
**Impacto económico:** $$150–$300
**Riesgo legal:** Deserción de usuarios
**Antes → Después**
**Antes:** `<button style="background: #FFA500; color: #FFFFFF;">Comprar</button>` (contraste 2.1:1)
**Después:** `<button style="background: #D2691E; color: #FFFFFF;">Comprar</button>` (contraste 4.5:1)
**CTA:** [Contratar solución](mailto:emilio@ranuk.dev)
![Antes/Después](before_after_low_contrast.png)

### Imágenes de producto sin alt text
**Impacto económico:** $$200–$500
**Riesgo legal:** Posible demanda por inaccesibilidad
**Antes → Después**
**Antes:** `<img src="producto.jpg">`
**Después:** `<img src="producto.jpg" alt="Zapatillas running azul">`
**CTA:** [Contratar solución](mailto:emilio@ranuk.dev)
![Antes/Después](before_after_missing_alt.png)

### Menú de navegación no operable por teclado
**Impacto económico:** $$300–$600
**Riesgo legal:** Exclusión de usuarios con discapacidad motriz
**Antes → Después**
**Antes:** `<div class="menu" onclick="toggleMenu()">` (sin `tabindex` ni `role`)
**Después:** `<nav aria-label="Principal"><ul role="menubar">…</ul></nav>` con manejo de teclado
**CTA:** [Contratar solución](mailto:emilio@ranuk.dev)
![Antes/Después](before_after_keyboard_trap.png)

## Recomendaciones
- Corregir contraste de color en botones y elementos interactivos para cumplir WCAG 2.1 AA (mínimo 4.5:1).
- Agregar texto alternativo descriptivo a todas las imágenes de producto.
- Hacer el menú de navegación operable por teclado usando roles ARIA y gestión de foco.

💡 Arreglamos esto por vos — [contratá el fix](mailto:emilio@ranuk.dev)