# Auditoría de Accesibilidad WCAG: TiendaOnline Demo
**Fecha:** 2026-10-04
**Estado:** Finalizado

## Resumen Ejecutivo
Auditoría de accesibilidad WCAG 2.1 AA — se detectaron barreras que afectan la experiencia de usuarios con discapacidad y exponen a la empresa a riesgos legales.

## Hallazgos Detallados
| Hallazgo | Severidad | Impacto |
| --- | --- | --- |
| Contraste bajo en botón de compra | High | Riesgo legal: $150–$300 sanción (ley 26.653) |
| Imágenes de producto sin alt text | Medium | Riesgo legal: $200–$500 sanción (ley 26.653) |
| Menú de navegación no operable por teclado | Critical | Riesgo legal: $500–$1000 sanción (ley 26.653) |

### Contraste bajo en botón de compra
**Impacto en el negocio:** –12% conversión mobile / demanda ADA Title III
**Antes → Después**
**Antes:** `<button style="background: #FFA500; color: #FFFFFF;">Comprar</button>` (contraste 2.1:1)
**Después:** `<button style="background: #D2691E; color: #FFFFFF;">Comprar</button>` (contraste 4.5:1)
Contratar fix: [Contacto](mailto:ada@ejemplo.com)
![Antes/Después](placeholder.png)

### Imágenes de producto sin alt text
**Impacto en el negocio:** Lectores de pantalla no pueden describir los productos → pérdida de ventas y riesgo de demanda
**Antes → Después**
**Antes:** `<img src="producto.jpg">`
**Después:** `<img src="producto.jpg" alt="Zapatillas running azul">`
Contratar fix: [Contacto](mailto:ada@ejemplo.com)
![Antes/Después](placeholder.png)

### Menú de navegación no operable por teclado
**Impacto en el negocio:** Usuarios sin mouse no pueden navegar → abandono del sitio y posible demanda ADA
**Antes → Después**
**Antes:** `<div class="menu" onclick="toggleMenu()">` (sin `tabindex` ni `role`)
**Después:** `<nav aria-label="Principal"><ul role="menubar">…</ul></nav>` con manejo de teclado
Contratar fix: [Contacto](mailto:ada@ejemplo.com)
![Antes/Después](placeholder.png)

## Recomendaciones
- Corregir contraste de color en botones y elementos interactivos para cumplir WCAG 2.1 AA (mínimo 4.5:1).
- Agregar texto alternativo descriptivo a todas las imágenes de producto.
- Hacer el menú de navegación operable por teclado usando roles ARIA y gestión de foco.

💡 Arreglamos esto por vos — [contratá el fix](mailto:emilio@ranuk.dev)