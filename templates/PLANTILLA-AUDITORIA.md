# Auditoría de Accesibilidad Digital — ADA / WCAG 2.1 AA

**Cliente:** `{{NOMBRE_EMPRESA}}`
**Sitio auditado:** `{{URL}}`
**Fecha:** `{{FECHA}}`
**Auditor:** Emilio Ranúcoli — Consultoría de Accesibilidad Digital
**Normativa de referencia:** Americans with Disabilities Act (ADA Title III) + WCAG 2.1 Nivel AA

---

## 1. Resumen Ejecutivo

Este reporte documenta `{{N_HALLAZGOS}}` hallazgos de no-conformidad con los estándares WCAG 2.1 AA, de los cuales `{{N_CRITICOS}}` presentan **riesgo legal alto** bajo ADA Title III. En 2025 se registraron más de 5.000 demandas federales por accesibilidad web en EE.UU., el **69% dirigidas a empresas con facturación menor a USD 25M** — el perfil de `{{NOMBRE_EMPRESA}}`.

**Nivel de riesgo actual:** `{{CRITICO / ALTO / MEDIO / BAJO}}`
**Tiempo estimado de remediación:** `{{HORAS}}` horas
**Costo estimado de remediación (paquete propuesto):** USD `{{PRECIO}}`

### Top 3 riesgos urgentes
1. `{{RIESGO_1}}`
2. `{{RIESGO_2}}`
3. `{{RIESGO_3}}`

---

## 2. Metodología

Auditoría híbrida: escaneo automatizado (axe-core, Lighthouse, WAVE) + revisión semántica asistida con modelo de lenguaje avanzado (Claude Sonnet 4) sobre árbol DOM, roles ARIA, orden de tabulación y contraste. Cobertura:

- Home + 3 páginas de mayor tráfico
- 1 flujo transaccional completo (ej. checkout, contacto, reserva)
- Formularios públicos
- Media (imágenes, video, PDFs enlazados)

---

## 3. Hallazgos por Severidad

> Cada hallazgo incluye: criterio WCAG violado, ubicación, evidencia, impacto en usuario, y remediación con código.

### 🔴 CRÍTICOS (bloqueo total + riesgo legal directo)

#### C-01 — `{{TITULO}}`
- **Criterio WCAG:** `{{EJ: 1.1.1 Non-text Content (A)}}`
- **Ubicación:** `{{URL / selector CSS}}`
- **Evidencia:**
  ```html
  <!-- ACTUAL -->
  <img src="/hero.jpg">
  ```
- **Impacto:** Usuarios de lector de pantalla no perciben el contenido visual; bloquea comprensión.
- **Base legal:** Caso *Robles v. Domino's* (SCOTUS 2019) establece aplicabilidad de ADA a sitios comerciales.
- **Remediación:**
  ```html
  <img src="/hero.jpg" alt="{{DESCRIPCIÓN_CONTEXTUAL}}">
  ```
- **Esfuerzo:** `{{N}}` min

*(Repetir bloque para cada hallazgo crítico)*

---

### 🟠 ALTOS (fricción severa, riesgo legal indirecto)

#### A-01 — Contraste de color insuficiente en CTAs
- **Criterio WCAG:** 1.4.3 Contrast (Minimum) (AA)
- **Evidencia:** Botón "Comprar" usa `#9ca3af` sobre `#ffffff` → ratio 2.8:1 (requiere ≥4.5:1)
- **Impacto:** 8% de hombres y 0.5% de mujeres con déficit de visión al color no pueden leer el botón.
- **Remediación:** Cambiar a `#4b5563` → ratio 7.6:1 ✅
- **Esfuerzo:** 5 min

*(Repetir)*

---

### 🟡 MEDIOS (mejora de experiencia)

*(Repetir)*

---

### 🔵 BAJOS (best practices)

*(Repetir)*

---

## 4. Resumen Cuantitativo

| Severidad | Cantidad | Criterios WCAG violados |
|-----------|----------|-------------------------|
| 🔴 Crítico | `{{N}}` | `{{LISTA}}` |
| 🟠 Alto    | `{{N}}` | `{{LISTA}}` |
| 🟡 Medio   | `{{N}}` | `{{LISTA}}` |
| 🔵 Bajo    | `{{N}}` | `{{LISTA}}` |
| **Total**  | **`{{N}}`** | |

---

## 5. Plan de Remediación Propuesto

### Fase 1 — Críticos (Semana 1)
- `{{TAREAS}}`
- **Entrega:** sitio libre de los hallazgos rojos, declaración de accesibilidad publicada.

### Fase 2 — Altos (Semana 2)
- `{{TAREAS}}`

### Fase 3 — Medios y Bajos (Semana 3, opcional)
- `{{TAREAS}}`

**Incluye además:**
- Archivo `accessibility-statement.html` publicado en `/accesibilidad`
- Testing manual con NVDA + VoiceOver
- Certificado de cumplimiento WCAG 2.1 AA post-remediación
- 30 días de soporte para regresiones

**Inversión:** USD `{{PRECIO}}` — pago 50% inicio / 50% entrega.

---

## 6. Qué ocurre si no se remedia

- **Demandas "drive-by":** litigios masivos por firmas especializadas, costo típico de arreglo extrajudicial USD 10.000–75.000.
- **Pérdida de mercado:** 26% de adultos en EE.UU. reporta alguna discapacidad (CDC). Sitio inaccesible = exclusión directa de ingresos.
- **SEO:** Google penaliza sitios con mala semántica y bajo contraste desde Core Web Vitals 2024.

---

## 7. Anexos

- **A1.** Reporte completo axe-core (JSON adjunto)
- **A2.** Capturas de pantalla de cada hallazgo crítico
- **A3.** Declaración de accesibilidad modelo (borrador editable)
- **A4.** Checklist WCAG 2.1 AA completa con estado por criterio

---

**Contacto para ejecutar la remediación:**
Emilio Ranúcoli
ranucoliemilio@gmail.com
`{{TELEFONO_O_CALENDLY}}`

*Este reporte es confidencial. No constituye asesoramiento legal; para defensa ante litigios en curso, consulte a un abogado especializado en ADA.*
