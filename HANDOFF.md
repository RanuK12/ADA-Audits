# HANDOFF — ADA Audits

## Propósito del proyecto

Sistema de outbound manual + semi-automatizado para vender auditorías de accesibilidad digital (ADA / WCAG 2.1 AA) a negocios en EE.UU. Fase 1 de un plan de monetización de 3 fases.

## Estado actual

**En desarrollo / activo.** El sistema de escaneo y las plantillas están listos. Se han realizado escaneos de prueba. La fase de outbound manual está en curso.

## Stack y dependencias clave

- axe-core CLI (`npm i -g @axe-core/cli`)
- Puppeteer
- Lighthouse
- Python 3 (scripts de automatización)
- Bash
- Claude Sonnet 4 (generación de reportes finales)

**No requiere deploy ni servidor.** Todo es local.

## Qué funciona / qué está roto

| Estado | Item |
|--------|------|
| ✅ | `quick-scan.sh` — escaneo rápido + scoring + flag de lead |
| ✅ | `fetch-site.sh` — descarga de sitio + axe + lighthouse |
| ✅ | Plantilla de auditoría (`PLANTILLA-AUDITORIA.md`) |
| ✅ | Plantillas de email cold + follow-up (`EMAIL-TEMPLATES.md`) |
| ✅ | Pipeline de leads (`prospectos/leads.csv`) |
| ⚠️ | Outbound 100% manual (no hay automatización de envío en Fase 1) |
| ❓ | Aún sin primer cliente cerrado (objetivo: 1/semana) |

## Próximos pasos claros

1. **Hoy:** elegir 1 vertical + 1 ciudad US, buscar 10 URLs, correr `quick-scan.sh`.
2. **Esta semana:** enviar 5 emails personalizados con evidencia de scan.
3. **Cierre #1:** cobrar 50% upfront, correr `fetch-site.sh`, generar reporte con Claude, entregar PDF.
4. **Post-cierre #3:** evaluar pasar a Fase 2 (Gumroad pasivo) y Fase 3 (Micro-SaaS).

## Notas para retomar el proyecto después de X tiempo

- **Leer primero:** `FLUJO-DIARIO.md` (rutina de 2h/día).
- **Elegir vertical:** dentistas, hoteles boutique, chiropractors, etc. (ver `CRITERIOS-TARGETING.md`).
- **Recordar:** no bajar de USD 800. No automatizar envío en Fase 1. Solo sitios US.
- **Si se olvidó el comando de escaneo:** `./scripts/quick-scan.sh -f prospectos/urls-del-dia.txt`
- **Si se olvidó el pipeline:** abrir `prospectos/leads.csv` y actualizar `email_sent_date` a mano.
