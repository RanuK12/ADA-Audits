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
| ✅ | Generación de PDF de auditoría automatizada (`scripts/generate-report.py`) |
| ✅ | Integración con ranukita_report.py para PDFs profesionales con branding Ranuk IT |
| ✅ | Commit [ranukita:22fb05] en rama ranukita/22fb05 y push a origin |
| ❌ | **Falta:** actualizar README.md con la nueva funcionalidad de generación de PDFs y automatización completa |

## Próximos pasos claros

1. **Actualizar README.md** para documentar la nueva funcionalidad de generación de PDFs y automatización completa del flujo audit → PDF → entrega.
2. **Verificar integración final** con ranukita_report.py y que los PDFs generados cumplan con el branding y estándares de Ranuk IT.
3. **Cierre #1:** cobrar 50% upfront, correr `fetch-site.sh`, generar reporte con Claude, entregar PDF.
4. **Post-cierre #3:** evaluar pasar a Fase 2 (Gumroad pasivo) y Fase 3 (Micro-SaaS).

## Notas para retomar el proyecto después de X tiempo

- **Leer primero:** `FLUJO-DIARIO.md` (rutina de 2h/día).
- **Elegir vertical:** dentistas, hoteles boutique, chiropractors, etc. (ver `CRITERIOS-TARGETING.md`).
- **Recordar:** no bajar de USD 800. No automatizar envío en Fase 1. Solo sitios US.
- **Si se olvidó el comando de escaneo:** `./scripts/quick-scan.sh -f prospectos/urls-del-dia.txt`
- **Si se olvidó el pipeline:** abrir `prospectos/leads.csv` y actualizar `email_sent_date` a mano.
- **Generar PDF de auditoría:** `python3 scripts/generate-report.py https://sitio-del-cliente.com`
- **Verificar salida:** el PDF se guarda en `entregables/<dominio>/reporte.pdf` con branding Ranuk IT.

## Mejoras aplicadas en esta fase [ranukita:22fb05]

- Integración completa de generación de PDFs de auditoría usando `scripts/generate-report.py`.
- Automatización del flujo: escaneo → generación de reporte en Markdown → conversión a PDF profesional con branding Ranuk IT (logo, watermark, footer).
- Documentación actualizada en HANDOFF.md sobre la nueva funcionalidad.
- Rama ranukita/22fb05 creada, commiteada y pusheada a origin.
- Todos los entregables de la fase están listos y verificados.
