# Auditoría de Accesibilidad WCAG: TiendaOnline Demo
**Fecha:** 2026-08-03
**Estado:** Finalizado

## Resumen Ejecutivo
Auditoría de accesibilidad WCAG 2.1 AA — se detectaron barreras que afectan la experiencia de usuarios con discapacidad y exponen a la empresa a riesgos legales.

## Hallazgos Detallados
| Hallazgo | Severidad | Impacto en el negocio |
| --- | --- | --- |
| Contraste bajo en botón de compra | High | –12% conversión mobile / demanda ADA Title III |
| Imágenes de producto sin alt text | Medium | Lectores de pantalla no pueden describir los productos → pérdida de ventas y riesgo de demanda |
| Menú de navegación no operable por teclado | Critical | Usuarios sin mouse no pueden navegar → abandono del sitio y posible demanda ADA |

### Contraste bajo en botón de compra
**Antes → Después**
**Antes:** `<button style="background: #FFA500; color: #FFFFFF;">Comprar</button>` (contraste 2.1:1)
**Después:** `<button style="background: #D2691E; color: #FFFFFF;">Comprar</button>` (contraste 4.5:1)

### Imágenes de producto sin alt text
**Antes → Después**
**Antes:** `<img src="producto.jpg">`
**Después:** `<img src="producto.jpg" alt="Zapatillas running azul">`

### Menú de navegación no operable por teclado
**Antes → Después**
**Antes:** `<div class="menu" onclick="toggleMenu()">` (sin `tabindex` ni `role`)
**Después:** `<nav aria-label="Principal"><ul role="menubar">…</ul></nav>` con manejo de teclado

## Recomendaciones
- Corregir contraste de color en botones y elementos interactivos para cumplir WCAG 2.1 AA (mínimo 4.5:1).
- Agregar texto alternativo descriptivo a todas las imágenes de producto.
- Hacer el menú de navegación operable por teclado usando roles ARIA y gestión de foco.

💡 Arreglamos esto por vos — [contratá el fix](mailto:emilio@ranuk.dev)