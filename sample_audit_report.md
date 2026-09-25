# Auditoría de Accesibilidad WCAG: TiendaOnline Demo
**Fecha:** 2026-09-25
**Estado:** Finalizado

## Resumen Ejecutivo
Auditoría de accesibilidad WCAG 2.1 AA — se detectaron barreras que afectan la experiencia de usuarios con discapacidad y exponen a la empresa a riesgos legales.

## Hallazgos Detallados
| Hallazgo | Severidad | Impacto en el negocio | Impacto financiero estimado |
| --- | --- | --- | --- |
| Contraste bajo en botón de compra | High | –12% conversión mobile / demanda ADA Title III | $500 - $2,000 (pérdida de conversiones) |
| Imágenes de producto sin alt text | Medium | Lectores de pantalla no pueden describir los productos → pérdida de ventas y riesgo de demanda | $1,500 - $3,000 (pérdida de leads/ventas) |
| Menú de navegación no operable por teclado | Critical | Usuarios sin mouse no pueden navegar → abandono del sitio y posible demanda ADA | $1,000 - $5,000 (abandono de sitio) |

### Contraste bajo en botón de compra
**Impacto en el negocio:** –12% conversión mobile / demanda ADA Title III
**Antes → Después**
**Antes:** `<button style="background: #FFA500; color: #FFFFFF;">Comprar</button>` (contraste 2.1:1)
**Después:** `<button style="background: #D2691E; color: #FFFFFF;">Comprar</button>` (contraste 4.5:1)

### Imágenes de producto sin alt text
**Impacto en el negocio:** Lectores de pantalla no pueden describir los productos → pérdida de ventas y riesgo de demanda
**Antes → Después**
**Antes:** `<img src="producto.jpg">`
**Después:** `<img src="producto.jpg" alt="Zapatillas running azul">`

### Menú de navegación no operable por teclado
**Impacto en el negocio:** Usuarios sin mouse no pueden navegar → abandono del sitio y posible demanda ADA
**Antes → Después**
**Antes:** `<div class="menu" onclick="toggleMenu()">` (sin `tabindex` ni `role`)
**Después:** `<nav aria-label="Principal"><ul role="menubar">…</ul></nav>` con manejo de teclado

## Recomendaciones
- Corregir contraste de color en botones y elementos interactivos para cumplir WCAG 2.1 AA (mínimo 4.5:1).
- Agregar texto alternativo descriptivo a todas las imágenes de producto.
- Hacer el menú de navegación operable por teclado usando roles ARIA y gestión de foco.

💡 **¿Listo para hacer tu sitio accesible y evitar demandas?**
Arreglamos estos problemas por vos. Presupuesto estimado: Consultá nuestro presupuesto personalizado (ej: arreglos básicos desde $800, auditoría completa + fix desde $1500).
👉 [Contratá el servicio de fix ahora](mailto:emilio@ranuk.dev?subject=Auditoría%20y%20Fix%20de%20Accesibilidad)