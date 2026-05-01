# INFORME DE INCIDENTE — GARYCIO BOT
**Fecha del incidente:** 23 de abril de 2026, 18:27–19:36 hora Argentina (21:27–22:36 UTC)
**Fecha del informe:** 23 de abril de 2026
**Estado actual del bot:** APAGADO Y ELIMINADO DE PM2. Watchdog inerte. Sin auto-restart.

---

## 1. RESUMEN EJECUTIVO

Durante ~70 minutos el bot recibió mensajes reales de ~175 donantes y les respondió o intentó responderles, cuando debía estar en TEST_MODE respondiendo SÓLO a los dos admins. El problema tuvo tres capas:

1. **Bug de whitelist (causa raíz):** la función `isWhitelisted()` tenía una ruta lógica que dejaba pasar a todos cuando había "capacidad disponible", ignorando que TEST_MODE estaba activo.
2. **Inestabilidad operativa:** 8 reinicios manuales (SIGINT) en 70 minutos mientras se intentaba diagnosticar. Cada reinicio reprocesaba webhooks en cola.
3. **Amplificadores:** reintentos automáticos 3x por envío fallido, enums de DB desalineados con la IA, permisos postgres faltantes, notificaciones admin sin throttle.

**Impacto real:**
- 372 mensajes de donantes clasificados por la IA
- 175 donantes recibieron mensaje del bot (status "sent")
- 128 escaladas marcadas "needsHuman" (operador humano nunca se enteró a tiempo)
- 1945 fallos de envío a WhatsApp (1773 por ventana de 24h cerrada, 53 por rate limit)
- 47 reclamos no se guardaron en DB (enum inválido)
- Rate limit WhatsApp quemado contra el admin (Emilio + Stefano)

---

## 2. CAUSAS RAÍZ DETALLADAS

### 2.1 Whitelist rota (código)
Archivo: `src/services/bot-control.ts:153`
La versión anterior hacía: si TEST_MODE y no admin → caía en "capacidad first-come-first-served" y activaba a la donante. El fix ya está aplicado (corte duro en `false`), pero se aplicó DESPUÉS del incidente.

### 2.2 Los 8 reinicios NO fueron crashes
Todos los reinicios del bot en la ventana del desastre fueron por SIGINT manual (señal de apagado enviada por consola). No hubo OOM, no hubo excepciones no capturadas. Fue intervención humana mientras se debuggeaba. Cada reinicio:
- Reprocesaba webhooks que 360/Meta tenía en reintento
- Generaba nuevos sendMessage → nuevos retries → más 131047/131056

### 2.3 Retry logic descontrolada
Cada envío fallido dispara 3 reintentos (ver logs "retry:1, retry:2, retry:3"). Un solo reclamo puede gastar 4 intentos contra WhatsApp. Si el primer intento falla con 131047 (ventana 24h), reintentar NO puede funcionar — es fallo permanente. Hay que detectar esos códigos y NO reintentar.

### 2.4 Error 131047 "Re-engagement message"
WhatsApp Business API exige que, si pasaron >24h desde el último mensaje del cliente, sólo puedas enviar "template messages" pre-aprobados. El bot intentaba respuestas libres → 1773 fallos en 1 hora. Esto NO es un problema de nuestro código — es política de Meta. Solución: plantillas pre-aprobadas para re-engagement o, mejor, no intentar responder fuera de la ventana.

### 2.5 Error 131056 "Business/Consumer pair rate limit"
Se disparó cuando el bot intentó notificar al admin (Stefano 5491126330388) múltiples veces por segundo (una por cada escalación). Meta limita la frecuencia de mensajes business→consumer. **Hay que agrupar notificaciones admin en un solo mensaje con ventana de 10–30s.**

### 2.6 Enum `tipo_reclamo` desalineado
La IA genera clasificaciones como `no_pasaron`, `pelela`, `multiple_issues` que no existían en el ENUM postgres → 47 reclamos no se guardaron. La IA anterior agregó algunos enums pero queda la causa raíz: **no hay validación entre lo que la IA genera y lo que la DB acepta.**

### 2.7 Permiso `ia_training_examples`
10 errores "permission denied for table ia_training_examples". El clasificador siguió funcionando pero sin ejemplos de entrenamiento → calidad de clasificación degradada.

---

## 3. EJEMPLOS DE CONVERSACIONES

### 3.1 BIEN MANEJADO — Consulta simple respondida y leída
**Teléfono:** 5491164225454 · 21:29
- Donante: "Que día pasan esta semana gracias"
- IA: `consulta` / `calm` / `confidence:high` ✅
- Bot envió respuesta → `delivered` → `read` ✅
- La donante volvió 14 min después con otra consulta más → también leyó la respuesta.

**Veredicto:** IA correcta, bot respondió, donante satisfecha.

### 3.2 BIEN MANEJADO — Saludo clasificado como irrelevante pero respondido
**Teléfono:** 5491158064338 · 21:29
- Donante: "Buen día"
- Bot respondió → `delivered` → `read` varias veces ✅

### 3.3 BIEN MANEJADO — Reclamo escalado correctamente
**Teléfono:** 5491161725469 · 21:29
- Donante: "Pasa de mi casa a siete cuadras y acá no pasan"
- IA: `reclamo` / `frustrated` / `needsHuman:true` ✅ (clasificación excelente)
- Bot envió 2 mensajes de escalación → `sent` ✅
- La donante respondió 4 veces más → bot mantuvo modo "escalado" y no interfirió ✅
- Al final ella se autorresolvió.

**Veredicto:** el flujo de escalación funcionó. El problema fue que el operador humano (vos) no recibió la alerta por el rate limit.

---

### 3.4 MAL MANEJADO — Reclamo que nunca recibió respuesta
**Teléfono:** 5491169011520 · 21:29
- Donante: "Porque no vienen a retirar el bidón hace una semana"
- IA: `reclamo` / `frustrated` / `needsHuman:true` ✅ (clasificación bien)
- Bot intentó responder → FALLÓ con 131047
- Donante quedó muda 3 horas. A las 22:33 escribió "1" (seguía esperando algo).

**Veredicto:** IA bien, infraestructura falló. Donante abandonada.

### 3.5 MAL MANEJADO — Consulta simple triplicada y toda fallida
**Teléfono:** 5491128602976 · 21:28
- Donante: "Buen día no solo quería saber cuando empiezan muchas gracias buen fin de semana"
- IA: `consulta` / `calm` / `confidence:high` ✅
- Bot intentó enviar 3 veces → las 3 fallaron (131047)
- A las 22:26 la donante volvió: "Buena noche Miércoles y Sábado así bueno gracias hay regalos"
- IA esta vez: `multiple_issues` / `confidence:low` ❌ (clasificación mala)
- Bot intentó responder 2 veces → las 2 fallaron.

**Veredicto:** doble falla — retry inútil + segunda clasificación equivocada por ambigüedad.

### 3.6 MAL MANEJADO — Donante pide "hablar con alguien" y la IA le pide datos
**Teléfono:** 5491131017192 · 21:45
- Donante: "Nooooooooo" → "No quiero ser donante!!!!!" → "Necesito hablar con alguien POR FAVOR!!!!!!"
- Bot la metió en flujo de formulario pidiendo nombre y dirección: "Paula Domínguez", "Ramón Cabrero 3169. PB Timbre 1. Lanús Este"
- En vez de escalar a humano, la IA ejecutó flujo administrativo → **empeoró el enojo**.

**Veredicto:** FALLA GRAVE de clasificación. El intent `hablar_persona` existe pero no se disparó. Hay que agregar detección directa de frases "hablar con alguien", "no quiero ser donante", "POR FAVOR" → forzar escalación.

### 3.7 MAL MANEJADO — "No me llevaron el orín" ignorado
**Teléfono:** 5491151010622 · 21:29
- Donante: "Hoy ni me llevaron el orin"
- Bot intentó responder → 131047 → nunca más escribió. Abandonada.

### 3.8 MAL MANEJADO — Reclamo por regalo no entregado
**Teléfono:** 5491164045263 · 21:28 a 22:10
- Donante escribió 4 mensajes distintos a lo largo de 40 min, con frustración creciente: "Estoy llamando para aser reclamo p los regalos q no me trajeron" → "Si pasaron medejaron el vidon pero medijo q aga reclamo p el regalo" → "Y no me atiende nadie" → "Save q p mi casa no pasaron..."
- TODOS los intentos de respuesta fallaron con 131047.

**Veredicto:** el caso más doloroso — la donante sintió literalmente que nadie le atendía.

---

## 4. PLAN DE CORRECCIÓN (prioridad ordenada)

### PRIORIDAD 1 — Bloquear antes de volver a encender (BLOQUEANTES)
1. **Reforzar TEST_MODE con double-check en múltiples capas.** Además del check en webhook, agregar check en `sendMessage()` que rechace envíos si el teléfono no está en `ADMIN_PHONES`+`TEST_PHONES` y `TEST_MODE=true`. Defensa en profundidad.
2. **Agregar test unitario** de `isWhitelisted()` con TEST_MODE=true, verificando que toda otra donante retorna `false`. Correr este test en CI antes de cada deploy.
3. **Deshabilitar retries para códigos permanentes de WhatsApp:** 131047, 131026, 131049, 131051. Agregar a `client.ts` una lista de "non-retriable errors".
4. **Throttle/coalescing de notificaciones admin:** acumular escalaciones por 20s y enviar un solo mensaje agrupado al admin. Esto elimina el rate limit 131056.
5. **Normalización IA → DB enum:** antes de `guardarReclamo()`, mappear la salida de la IA a valores válidos del enum. Mantener un mapa declarativo y, ante valor desconocido, usar `otro` + loguear warning.
6. **Permisos postgres** a `ia_training_examples`: `GRANT SELECT, INSERT ON ia_training_examples TO garycio_user`.

### PRIORIDAD 2 — Calidad de clasificación
7. **Frases gatillo de escalación forzada:** lista negra de patterns que pasan DIRECTO a humano sin consultar IA: "hablar con alguien", "no quiero ser", "POR FAVOR", ≥3 signos de exclamación seguidos, mayúsculas sostenidas >10 caracteres.
8. **Fallback de baja confianza:** si `confidence:low` → no ejecutar flujo, escalar a humano. Nunca improvisar con baja confianza.
9. **Detección de contexto previo:** si la donante ya escribió en últimos 10 min, no clasificar desde cero — seguir el hilo del reclamo abierto.

### PRIORIDAD 3 — Política WhatsApp
10. **Pre-check de ventana 24h antes de enviar.** Antes de llamar a `sendMessage`, verificar en DB si esta conversación está dentro de la ventana. Si no → usar template message o dejar sin responder (no intentar).
11. **Templates pre-aprobados** para re-engagement ("Hola, vi tu mensaje, te respondo ahora"). Esto abre la ventana sin error.

### PRIORIDAD 4 — Infraestructura
12. **Systemd o PM2 con `min_uptime: 60s` y `max_restarts: 3`** para evitar restart loops.
13. **Prohibir SIGINT manual en producción.** Cualquier reinicio debe pasar por un script que vacíe la cola primero (drain).
14. **Dashboard de monitoreo en vivo:** tasa de errores 131047/131056 por minuto, alerta si >5.
15. **Watchdog solo notifica, nunca reinicia automáticamente.** Ya está así, pero hay que revisar que los ADMIN_PHONES del script coincidan con el `.env` (hoy el script tiene 5 números, el `.env` solo 2).

### PRIORIDAD 5 — Plan de re-encendido seguro
16. **Fase 1:** TEST_MODE=true, solo admins. Probar por 48h cada flujo manualmente.
17. **Fase 2:** whitelist controlada de 5 donantes voluntarias conocidas. Probar por 72h.
18. **Fase 3:** ampliar de a 20 por día con monitoreo activo.
19. **Fase 4:** apertura general solo con dashboard en vivo + operador humano de guardia.

---

## 5. VERIFICACIÓN DE ESTADO ACTUAL

- `pm2 list` → vacío ✅
- `pgrep node` → no hay proceso del bot ✅
- `ss -tlnp` → no hay puerto del bot escuchando ✅
- Watchdog en cron → sigue activo pero en modo "Bot no esta corriendo. Nada que monitorear" ✅
- Webhook endpoint → nginx activo pero si llega un POST, no hay nada que lo procese. 360/Meta seguirán reintentando hasta timeout de su lado. **Recomendación: apagar nginx del dominio del webhook también**, o responder 503 con nginx, para no dejar webhooks en cola del lado de Meta.

---

## 6. ANTES DE VOLVER A ENCENDER — CHECKLIST
- [ ] P1.1 Double-check TEST_MODE en sendMessage
- [ ] P1.2 Test unitario de isWhitelisted
- [ ] P1.3 Non-retriable error codes
- [ ] P1.4 Throttle notificaciones admin
- [ ] P1.5 Mapper IA→enum DB
- [ ] P1.6 GRANT permisos ia_training_examples
- [ ] P2.7 Frases gatillo escalación
- [ ] P2.8 Fallback confidence:low
- [ ] P3.10 Pre-check ventana 24h
- [ ] P3.11 Templates aprobados por Meta
- [ ] P4.12 PM2 con min_uptime y max_restarts
- [ ] P4.15 Alinear ADMIN_PHONES en watchdog y .env
- [ ] Plan de comunicación con donantes afectadas listo
- [ ] Conversación con 360dialog cerrada

---

**Firma:** Informe generado por Claude tras análisis de `/opt/garycio/logs/out-0.log` y `/opt/garycio/src/` el 23/04/2026.
