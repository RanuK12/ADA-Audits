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
**⚖️ Impacto económico / riesgo legal:** Multas ADA hasta $4,000 + pérdida de conversiones por mala legibilidad
**🎨 Ejemplo visual de la corrección:**
Botón con colores ajustados para contraste mínimo 4.5:1 (ej: naranja oscuro sobre blanco)
**Antes → Después**
**Antes:** `<button style="background: #FFA500; color: #FFFFFF;">Comprar</button>` (contraste 2.1:1)
**Después:** `<button style="background: #D2691E; color: #FFFFFF;">Comprar</button>` (contraste 4.5:1)
**💡 Próximo paso:** Ajustar colores en CSS/SCSS. Tiempo estimado: 10-15 minutos.

### Imágenes de producto sin alt text
**Impacto en el negocio:** Lectores de pantalla no pueden describir los productos → pérdida de ventas y riesgo de demanda
**⚖️ Impacto económico / riesgo legal:** Riesgo de demanda por inaccessibilidad + pérdida de tráfico SEO y ventas
**🎨 Ejemplo visual de la corrección:**
Imagen con atributo alt descriptivo: alt='Zapatillas running azul'
**Antes → Después**
**Antes:** `<img src="producto.jpg">`
**Después:** `<img src="producto.jpg" alt="Zapatillas running azul">`
**💡 Próximo paso:** Agregar texto alternativo descriptivo a todas las imágenes. Tiempo estimado: 5-10 minutos por imagen.

### Menú de navegación no operable por teclado
**Impacto en el negocio:** Usuarios sin mouse no pueden navegar → abandono del sitio y posible demanda ADA
**⚖️ Impacto económico / riesgo legal:** Exclusión de usuarios con discapacidad motriz → abandono y posibles acciones legales
**🎨 Ejemplo visual de la corrección:**
Menú con roles ARIA y tabindex para navegación completa por teclado
**Antes → Después**
**Antes:** `<div class="menu" onclick="toggleMenu()">` (sin `tabindex` ni `role`)
**Después:** `<nav aria-label="Principal"><ul role="menubar">…</ul></nav>` con manejo de teclado
**💡 Próximo paso:** Implementar navegación por teclado con ARIA. Tiempo estimado: 20-30 minutos.

## Recomendaciones
- Corregir contraste de color en botones y elementos interactivos para cumplir WCAG 2.1 AA (mínimo 4.5:1).
- Agregar texto alternativo descriptivo a todas las imágenes de producto.
- Hacer el menú de navegación operable por teclado usando roles ARIA y gestión de foco.

💡 **¿Listo para hacer tu sitio accesible y evitar demandas?**
Arreglamos estos problemas por vos. Presupuesto estimado: Consultá nuestro presupuesto personalizado (ej: arreglos básicos desde $800, auditoría completa + fix desde $1500).
👉 [Contratá el servicio de fix ahora](mailto:emilio@ranuk.dev?subject=Auditoría%20y%20Fix%20de%20Accesibilidad)