# ADA Audits — Sistema de Monetización Fase 1

**Objetivo:** recuperar Mac + costo Claude en 2–3 semanas cerrando 1 cliente/semana a USD 800–1.200.

## Qué es esto

Sistema de outbound personalizado para vender auditorías de accesibilidad digital (ADA / WCAG 2.1 AA) a negocios en EE.UU. Combina escaneo automatizado, inteligencia de mercado y plantillas de email frías para cerrar clientes de forma predecible.

## Stack / Tecnologías

- **Escaneo:** axe-core CLI, Lighthouse, Puppeteer
- **Scripting:** Bash + Python 3
- **Reportes:** Markdown + pandoc (PDF) o `npx md-to-pdf`
- **Outbound:** Gmail manual (Fase 1) / scripts de apoyo Python
- **LLM:** Claude Sonnet 4 (para generar reportes finales)

## Estructura de carpetas

```
ADA-AUDITS/
├── README.md                       ← este archivo
├── FLUJO-DIARIO.md                 ← rutina de 2h/día. Leer primero.
├── CHEATSHEET-BOT.md               ← comandos rápidos para el bot
├── templates/
│   ├── PLANTILLA-AUDITORIA.md      ← formato del entregable final
│   └── PROMPT-GENERAR-AUDITORIA.md ← prompt maestro para Claude
├── scripts/
│   ├── fetch-site.sh               ← descarga HTML + axe + lighthouse
│   ├── quick-scan.sh               ← escaneo 30s → decide si es lead
│   ├── daily-auto.py               ← automatización diaria
│   ├── generate-pitch.py           ← genera pitch personalizado
│   ├── generate-report.py          ← genera reporte desde scan
│   ├── find-emails.py              ← extracción de emails
│   ├── find-urls.py                ← extracción de URLs
│   ├── next-action.py              ← sugiere siguiente acción
│   ├── outbox.py                   ← gestión de outbox
│   └── tg-send.py                  ← envío vía Telegram
├── prospectos/
│   ├── CRITERIOS-TARGETING.md      ← quién es ICP, quién no
│   ├── EMAIL-TEMPLATES.md          ← 5 plantillas cold + follow-up + objeciones
│   ├── leads.csv                   ← pipeline
│   └── urls-del-dia.txt            ← URLs a escanear hoy
├── entregables/
│   └── EJEMPLO-auditoria-dentista-palermo.md  ← muestra terminada
└── logs/                           ← logs de escaneos y envíos
```

## Cómo correrlo localmente

### Setup inicial (una sola vez)

```bash
# Instalar herramientas de escaneo
npm i -g @axe-core/cli puppeteer lighthouse

# Verificar
axe --version
lighthouse --version
```

### Escaneo rápido (decide si es lead en 30s)

```bash
./scripts/quick-scan.sh https://cliente.com
# o batch
./scripts/quick-scan.sh -f prospectos/urls-del-dia.txt
```

### Auditoría completa (cuando cierra cliente)

```bash
./scripts/fetch-site.sh https://cliente.com entregables/cliente-01/
# Luego usá templates/PROMPT-GENERAR-AUDITORIA.md con Claude
```

### Generar PDF del reporte

```bash
pandoc entregables/cliente-01/reporte.md -o reporte.pdf --pdf-engine=xelatex
# fallback:
npx md-to-pdf entregables/cliente-01/reporte.md
```

## Deploy

No aplica. Todo corre localmente. Los reportes se entregan por email como PDF.

## Estado actual

- ✅ Sistema de escaneo funcional (axe + lighthouse + script propio)
- ✅ Plantillas de email y auditoría listas
- ✅ Pipeline de leads (`leads.csv`) operativo
- ⚠️ Outbound 100% manual en Fase 1 (sin automatización de envío)
- 🔄 Evolución futura: Fase 2 pasiva (Gumroad/Twitter/Reddit) y Fase 3 (Micro-SaaS)

## Reglas que no se negocian

- Precio mínimo USD 800. Nunca menos.
- 50% upfront siempre.
- Sitios solo US (ADA no aplica afuera).
- Evidencia específica en el primer email — genérico = 0% respuesta.
- No automatizar envío de emails en Fase 1. Personalizado 1-a-1.

## Siguiente fase

Mientras este sistema genera cash, Gumroad/Twitter/Reddit corren en background (Fase 2 pasiva). Después del 3er cliente cerrado, arrancar Fase 3 (Micro-SaaS) en paralelo.

## Licencia

MIT — © 2026 Ranuk IT Solutions | ranuk.dev
