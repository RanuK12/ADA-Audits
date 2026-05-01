# Cheatsheet — Disparadores ADA desde Ranuk Bot (Telegram)

Todo lo que podés tipear al bot:

| Comando Telegram | Qué hace | Tiempo |
|-----------------|----------|--------|
| `ada` | Muestra ayuda | 1s |
| `ada next` / `próxima acción` | Dice qué hacer ahora según el pipeline | 1s |
| `ada status` / `pipeline` | Resumen del pipeline (leads, revenue, etc.) | 1s |
| `ada scan <url>` | Escanea 1 sitio, devuelve score + top 3 issues | 30-60s |
| `ada scan-batch` | Escanea todas las URLs de `urls-del-dia.txt` | 5-20 min |
| `ada pitch <url>` | Genera email cold personalizado (requiere scan previo) | 2s |
| `ada report <url>` | Genera auditoría completa con Claude API + envía MD al chat | 30-120s |
| `ada add-lead <url> <email>` | Marca lead como "enviado" | 1s |

## Desde terminal (sin bot)

Mismos comandos pero tipeando `ada` directo en Terminal. El CLI está en `/opt/homebrew/bin/ada` (global).

## Flujo típico de un día (2h)

**Por Telegram, donde sea:**

```
próxima acción
```

El bot te contesta qué hacer. Seguí lo que diga.

**Cuando te dice "agregá URLs nuevas":**

1. Desde Telegram pedís al bot: `abrí urls-del-dia.txt`
2. Pegás 10-15 URLs nuevas (buscás en Google Maps: `dentist Brooklyn NY`, `chiropractor Miami FL`, etc.).
3. Volvés al bot:
   ```
   ada scan-batch
   ```
4. Esperás 5-15 min. El bot te devuelve los leads.

**Cuando te muestra leads:**

Para cada top lead:
```
ada pitch https://sitioejemplo.com/
```

El bot te devuelve el email LISTO para mandar. Solo tenés que:
- Buscar nombre del owner (2 min en LinkedIn)
- Buscar email (hunter.io / apollo.io)
- Reemplazar `{{first_name}}`
- Copiar → pegar en Gmail → enviar

Después avisás al bot:
```
ada add-lead https://sitioejemplo.com/ juan@clinica.com
```

**Cuando responden:**

```
ada report https://sitioejemplo.com/
```

El bot corre axe-core + Claude API y te manda el reporte MD completo al chat. Lo convertís a PDF (`pandoc` o `md-to-pdf`) y se lo enviás al cliente con Template 4 de `EMAIL-TEMPLATES.md`.

## Fuentes de URLs para prospectar

| Día | Vertical | Ciudad | Búsqueda |
|-----|----------|--------|----------|
| Lun | Dentistas | Brooklyn NY | `dentist brooklyn ny` |
| Mar | Quirop. / Chiro | Miami FL | `chiropractor miami fl` |
| Mié | Hoteles boutique | NYC | `boutique hotel manhattan` |
| Jue | Law firms chicos | Philadelphia | `personal injury lawyer philly` |
| Vie | Restaurantes con online ordering | LA | `restaurant online ordering los angeles` |

Copiá los primeros 10-15 resultados de Google Maps que tengan web propio (no Yelp/OpenTable).

## Archivos clave

```
~/Desktop/ADA-AUDITS/
├── CHEATSHEET-BOT.md              ← este archivo
├── FLUJO-DIARIO.md                ← rutina completa
├── README.md
├── prospectos/
│   ├── urls-del-dia.txt           ← ACÁ PEGÁS URLs NUEVAS
│   ├── scan-results.json          ← output de scan-batch
│   ├── leads.csv                  ← pipeline
│   ├── pitches/                   ← emails generados
│   ├── CRITERIOS-TARGETING.md
│   ├── EMAIL-TEMPLATES.md         ← follow-ups y respuestas a objeciones
│   └── emails-listos-2026-04-17.md ← primeros 3 leads personalizados
├── templates/
│   ├── PLANTILLA-AUDITORIA.md
│   └── PROMPT-GENERAR-AUDITORIA.md
├── entregables/
│   └── EJEMPLO-auditoria-dentista-palermo.md  ← muestra
└── scripts/
    ├── ada                        ← CLI principal
    ├── quick-scan.sh              ← motor axe-core
    ├── generate-pitch.py          ← motor emails
    ├── generate-report.py         ← motor auditoría Claude API
    └── next-action.py             ← motor "qué sigue"
```

## Ya tenés cargado hoy

3 emails listos en `prospectos/emails-listos-2026-04-17.md` para:

1. 🔴 Brooklyn Family Dental Care (30 issues — el mejor lead)
2. 🟠 Brooklyn Heights Dental (25 issues)
3. 🔴 Quentin Smile Dental (1 crítico + 22 landmarks)

**Siguiente paso:** mandá esos 3 emails. Objetivo: cerrar el primero en 1-2 semanas → Mac pagado.

## Si algo falla

- Bot no responde a comandos `ada`: reiniciar con `PATH=/opt/homebrew/Cellar/node/25.9.0_2/bin:$PATH pm2 restart ranuk-asistente --update-env`
- `ada scan` falla en un sitio: ese sitio bloquea headless Chrome. Pasá al siguiente.
- `ada report` pide API key: verificar `ANTHROPIC_API_KEY` en `~/ranuk-agent/bot/.env`
