# EVALUACIÓN TÉCNICA INTEGRAL — GARYCIO BOT
**Perspectiva:** Senior Full-Stack Engineer · 20+ años
**Fecha:** 23 de abril de 2026
**Servidor:** 204.168.183.96 (Ubuntu 24.04, 4GB RAM, 75GB disk, Node 22, PG16)
**Estado del bot:** ✅ APAGADO — sin proceso, sin PM2, sin riesgo de reencendido

---

## 1. VEREDICTO GENERAL

El sistema tiene una base decente (stack moderno, Drizzle ORM, pino logs, separación bot/services) pero **está ensamblado como un prototipo corriendo en producción**, no como un sistema crítico que maneja comunicación con 6000+ donantes. El incidente del 23/4 no fue un accidente aislado — fue el resultado predecible de 15 decisiones arquitectónicas frágiles que se alinearon al mismo tiempo.

**Problema filosófico central:** el bot fue diseñado para *responder por defecto* a cualquier mensaje que llega. Para un servicio crítico de soporte a donantes debería ser al revés: *no responder por defecto*, y sólo actuar cuando hay alta confianza de que la respuesta es correcta y autorizada.

---

## 2. INVENTARIO DE COMPONENTES

| Capa | Tecnología | Estado |
|---|---|---|
| VPS | Ubuntu 24.04, 4GB RAM, 2GB swap, 75G disk (8% usado) | ✅ OK |
| Firewall | UFW (22, 80, 443) | ✅ OK |
| Reverse proxy | Nginx 1.24 (solo `garycio` site) | ⚠️ Sin rate-limit, sin WAF |
| Runtime | Node 22.22.2, TypeScript 5.7 | ✅ OK |
| Proceso | PM2 cluster_mode (1 instancia) | ⚠️ Sin redundancia |
| DB | PostgreSQL 16, Drizzle ORM, 33 tablas | ⚠️ Ownership mixto |
| LLM | OpenAI GPT-4o vía `fetch` directo | ⚠️ Sin SDK, sin retries propios |
| WhatsApp | 360dialog Cloud API v2 | ⚠️ Sin templates para re-engagement |
| Observabilidad | Pino logs + watchdog cron | ❌ Sin métricas, sin dashboards |
| Testing | Jest configurado pero `--passWithNoTests` | ❌ Cero tests reales |
| CI/CD | Ninguno (git push manual al server) | ❌ |
| Staging | No existe | ❌ |

---

## 3. HALLAZGOS CRÍTICOS (ordenados por severidad)

### 🔴 CRÍTICO — Filosofía de "responder por defecto"
En `webhook.ts` todo mensaje que pasa whitelist va directo a `processIncomingMessage` → clasificador IA → respuesta. No hay:
- Cola intermedia persistente
- Check de horario
- Check de "esta conversación ya está escalada a humano, no responder"
- Check de "el usuario escribió hace 2s, espera y agrupa"

### 🔴 CRÍTICO — Whitelist con capacity mode (first-come-first-served)
`bot-control.ts:153` tiene múltiples rutas lógicas. El bug ya se corrigió pero la *arquitectura* sigue siendo peligrosa: bastó una condición mal evaluada para que pasaran TODAS las donantes. Debería ser **lista blanca explícita SIN fallbacks**, con test unitario que corre en CI.

### 🔴 CRÍTICO — `isPermanent` existe pero no se respeta en retries
En `client.ts` el error tiene `get isPermanent()` que incluye 131047 y 131056. **Sin embargo los logs muestran retry:1, retry:2, retry:3 para 131056**. Significa que la lógica de retry (probablemente en `handler.ts` o `queue.ts`) no consulta este flag antes de reintentar. Cada reintento de un error permanente quema rate limit extra.

### 🔴 CRÍTICO — Sin pre-check de ventana 24h de WhatsApp
1773 errores 131047 en 70 minutos. La política de Meta es conocida: fuera de 24h necesitás template message aprobado. El código **no consulta** `last_customer_message_at` antes de enviar → siempre tira respuesta libre → falla si pasaron 24h.

### 🔴 CRÍTICO — OpenAI GPT-4o sin SDK ni resiliencia
`clasificador-ia.ts` usa `fetch` directo a `api.openai.com`. Problemas:
- Sin retry con backoff exponencial
- Sin circuit breaker (si OpenAI cae, cada mensaje es 15s de timeout)
- Sin cache de clasificaciones repetidas
- Sin fallback a reglas heurísticas cuando la IA falla
- Modelo hardcoded `gpt-4o` → sin A/B, sin bajada a `gpt-4o-mini` para mensajes simples (costo)
- El prompt de sistema está bien estructurado pero **no hay validación** de que la respuesta JSON matchee el schema esperado (zod) antes de usarla

### 🔴 CRÍTICO — Notificaciones admin sin throttle
Cada escalación humana dispara `sendMessage` al admin. Con 128 escalaciones en 1 hora → rate limit 131056 sobre admin. Debe haber **cola de notificaciones con debounce de 20s** que agrupe en un solo mensaje.

### 🔴 CRÍTICO — Ownership de tablas PostgreSQL mixto
2 tablas (`ia_training_examples`, `audio_mensajes`) son propiedad del user `postgres`, el resto de `garycio`. Por eso "permission denied" en logs. Se arregla con `ALTER TABLE ... OWNER TO garycio` o con `GRANT`.

### 🟠 ALTO — Sin cola persistente
Todo es in-memory y async. Si el proceso cae:
- Se pierden mensajes en procesamiento
- Meta reintenta el webhook → reprocessing doble
- Los 8 reinicios manuales del 23/4 causaron exactamente esto

Una cola real (Redis con BullMQ, o incluso `pg-boss` si no se quiere agregar Redis) elimina el problema.

### 🟠 ALTO — Enums DB desalineados con output IA
La IA genera `tipo_reclamo: "no_pasaron"`, `"pelela"`, `"multiple_issues"` — ninguno en el enum original. 47 reclamos perdidos. Falta **capa de mapeo/validación** entre IA y persistencia. Ante valor desconocido → guardar como `otro` + loguear + alertar.

### 🟠 ALTO — Cero tests
`package.json`: `"test": "jest --passWithNoTests"`. Y efectivamente no hay tests. Para un sistema que maneja dinero y datos de personas esto es inaceptable. Mínimo: `isWhitelisted`, mapeo IA→enum, parser de webhook, clasificador con mocks.

### 🟠 ALTO — Secretos en .env plano con permisos amplios
`.env` tiene `OPENAI_API_KEY`, `WHATSAPP_TOKEN`, `ADMIN_API_KEY`, DB password. El servidor tiene password SSH `Fletero91!` (mismo que DB). Si alguien consigue ese password tiene acceso total a todo. Recomendación: (1) mover secretos a vault o systemd credentials, (2) SSH solo por key, password OFF, (3) DB password distinto, (4) rotar TODOS los tokens ahora.

### 🟠 ALTO — Watchdog con `ADMIN_PHONES` desincronizado
`scripts/watchdog.sh` tiene hardcoded 5 teléfonos, `.env` tiene 2. Si el watchdog dispara, notifica a teléfonos que NO son admins en runtime. Fuente única de verdad en `.env`.

### 🟠 ALTO — 737 líneas en `conversation-manager.ts`
Archivo monstruo, difícil de razonar. Mezclado: enrutamiento, lógica de negocio, IO DB, llamadas IA. Necesita split por dominio (reclamos, avisos, consultas, saludos).

### 🟡 MEDIO — Un solo VPS, sin failover
4GB RAM, 1 proceso cluster_mode (que igual es 1 sola instancia por el mode). Si este VPS se cae, el servicio muere. Para un sistema crítico mínimamente: snapshots automáticos diarios + segundo VPS dormido listo para levantar en <1h.

### 🟡 MEDIO — Sin CI/CD
Deploy = `git pull && npm run build && pm2 restart`. No hay validación previa, no hay test suite que corra, no hay rollback automático. Cualquier commit puede romper producción sin red de seguridad.

### 🟡 MEDIO — Sin rate limit ni WAF en Nginx
Un script malicioso puede inundar `/webhook` y saturar el bot. Debe haber `limit_req_zone` de Nginx al menos.

### 🟡 MEDIO — Logs sin rotación visible
`out-0.log` = 6.1MB en 2 días. Crece indefinidamente. PM2 logrotate existe pero no se ve configurado.

### 🟡 MEDIO — Sin métricas (Prometheus/Grafana)
Para detectar este incidente en vivo hubiera hecho falta: contador de errores 131047/min, contador de retries/min, latencia p95 de OpenAI, tasa de escalaciones. Nada existe.

### 🟡 MEDIO — `SEND_RATE_PER_SECOND=30` demasiado alto
El rate limiter interno permite 30 mensajes/segundo. WhatsApp Business para un par (business, consumer) es mucho más bajo. Debería ser 1/seg por destinatario + 10/seg global, con backoff adaptativo cuando 131056 aparece.

---

## 4. LO QUE SÍ ESTÁ BIEN

- Estructura de carpetas coherente (`bot/`, `services/`, `database/`, `config/`)
- Drizzle ORM es buena elección (type-safe, no magia)
- Pino como logger es decisión senior
- El `system_prompt` del clasificador está bien diseñado ("solo clasificá, no respondas")
- Webhook responde 200 inmediato (no bloquea a Meta) ✅
- Deduplicación por messageId existe (`markAsProcessed`)
- `TEST_MODE` tiene defensa en dos capas (webhook + client)
- Enum `WhatsAppAPIError.isPermanent` existe (aunque no se usa bien)
- Dead letter queue existe como tabla (aunque no verifiqué si se usa)
- UFW firewall activo con política mínima

---

## 5. ROOT CAUSE DEL INCIDENTE — RESUMEN

```
[Bug whitelist] + [sin pre-check 24h] + [retries sobre errores permanentes]
       ↓                    ↓                        ↓
  pasan todas       falla 131047           x3 por cada fallo
       ↓                    ↓                        ↓
  + [sin throttle notif admin] → rate limit admin 131056
       ↓
  + [8 reinicios manuales] → webhooks reprocesados
       ↓
  + [enum desalineado] → reclamos perdidos en DB
       ↓
  + [permisos DB rotos] → clasificador degradado
       ↓
  = 175 donantes tocadas, 128 escaladas perdidas, 1945 fallos de envío
```

---

## 6. PROMPT MAESTRO PARA IA DE IMPLEMENTACIÓN

Usá el prompt del archivo [PROMPT_MAESTRO_GARYCIO.md](PROMPT_MAESTRO_GARYCIO.md) con una IA capaz (Claude 4.7 / GPT-5) para que ejecute las correcciones en orden.

---

## 7. ESTIMACIÓN DE ESFUERZO

| Bloque | Tiempo estimado | Prioridad |
|---|---|---|
| P0 — Hotfixes bloqueantes (whitelist, isPermanent, ownership DB, throttle admin, pre-check 24h) | 2-3 días | Antes de cualquier reencendido |
| P1 — Cola persistente + circuit breaker OpenAI | 3-5 días | Antes de ampliar whitelist |
| P2 — Tests mínimos + CI | 2-3 días | Antes de ampliar whitelist |
| P3 — Refactor conversation-manager | 5-7 días | Mes 1 |
| P4 — Observabilidad (Prometheus + Grafana) | 3-4 días | Mes 1 |
| P5 — Templates Meta aprobados + re-engagement | 1-2 semanas de espera por aprobación de Meta | Paralelo |
| P6 — Staging environment + secretos en vault | 3-5 días | Mes 1-2 |

**Tiempo total razonable hasta sistema confiable:** 4-6 semanas de trabajo enfocado.

---

## 8. RECOMENDACIÓN FINAL

**No prendas el bot** hasta que, como mínimo:
1. Los 6 hotfixes P0 estén hechos, **deployados en staging** y probados con vos + Stefano por 48h.
2. Haya una lista de 5 donantes voluntarias (gente conocida, explicándoles que están en beta) para la fase 2.
3. Hables con 360dialog/Meta para aprobar 2-3 templates de re-engagement y subir tier de rate limit.
4. Haya un dashboard aunque sea básico que muestre errores 131047/131056/131009 en tiempo real.
5. Alguien esté *de guardia humana* las primeras 72h post-reencendido.

Si volvés a prender sin esto, **va a pasar igual o peor**. Las donantes no son recurso renovable — la pérdida de confianza no se recupera con un segundo intento.
