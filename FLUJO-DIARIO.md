# Flujo Diario — 2 horas/día para cerrar 1 cliente/semana

## Setup inicial (una sola vez, ~30 min)

```bash
# Instalar herramientas de escaneo
npm i -g @axe-core/cli puppeteer lighthouse

# Verificar
axe --version
lighthouse --version
```

## Rutina diaria (lunes a viernes, 2 h)

### 🌅 Mañana — 45 min — Generar leads
1. Elegir vertical del día (ej. lunes = dentistas NY, martes = hoteles boutique FL).
2. Google Maps → copiar 20 resultados con web.
3. Pegar URLs en `prospectos/urls-del-dia.txt`.
4. Correr `./scripts/quick-scan.sh -f prospectos/urls-del-dia.txt > /tmp/scan.json`
5. Filtrar los que `qualifies_as_lead == true` → cargar en `leads.csv` con los 3 top issues.
6. Para cada uno, 60 segundos en LinkedIn/About page → obtener nombre del owner + email (usar hunter.io trial o apollo.io).

### ☀️ Tarde — 45 min — Enviar 15 emails personalizados
1. Abrir `EMAIL-TEMPLATES.md` → Template 1.
2. Copy-paste, rellenar `{{...}}` con los 3 issues reales del scan.
3. Mandar desde Gmail (no tool automatizado: entregabilidad alta en volumen bajo).
4. Marcar `email_sent_date` en `leads.csv`.

### 🌙 Noche — 30 min — Follow-ups + atención
1. Leads con `email_sent_date` de hace 3 días y `replied = false` → Template 2.
2. Leads con 7 días sin respuesta → Template 3 (último).
3. Responder cualquier reply del día con Template 4 o 5.

## Cuando cierra el primer cliente

1. Cobrar 50% upfront (Stripe / Wise / transferencia).
2. Correr `./scripts/fetch-site.sh https://cliente.com entregables/cliente-01/`
3. Pegar el prompt de `templates/PROMPT-GENERAR-AUDITORIA.md` en Claude + adjuntar HTMLs.
4. Revisar output, guardar en `entregables/cliente-01/reporte.md`.
5. Convertir a PDF: `pandoc reporte.md -o reporte.pdf --pdf-engine=xelatex`
   (o usar `npx md-to-pdf` si pandoc da problemas).
6. Enviar PDF al cliente junto con el plan de remediación y factura del 50% inicial.
7. Ejecutar remediación con Claude Code sobre el repo/tema del cliente.
8. Cobrar 50% final a la entrega.

## Métricas objetivo (primer mes)

| Semana | Emails | Respuestas | Cierres | Revenue |
|--------|--------|------------|---------|---------|
| 1      | 75     | 4–7        | 1       | $800–1.200 |
| 2      | 75     | 6–10       | 1–2     | $1.600–2.400 |
| 3      | 75     | 8–12       | 2       | $2.400 |
| 4      | 75     | 8–12       | 2       | $2.400 |
| **Total** | **300** | **26–41** | **6–7** | **~$7k–9k** |

Mac recuperado en semana 2–3. Mes 2 pasamos a Fase 3 (Micro-SaaS).

## Qué NO hacer

- No mandar más de 20 emails/día desde Gmail (spam flag).
- No automatizar con Mailchimp o herramientas similares (entregabilidad cae 70% en cold).
- No bajar el precio por debajo de USD 800. El techo cognitivo del cliente es "lo barato es caro" — precios bajos generan desconfianza en servicios legales/compliance.
- No prometer "garantía de no demanda". No sos abogado. WCAG 2.1 AA = reducción drástica de riesgo, no inmunidad.
