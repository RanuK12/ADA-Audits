#!/usr/bin/env python3
"""CRM Audit para ADA-AUDITS.

Lee ~/.ranukita/ada_outreach/crm.json y genera un reporte de salud de leads:
- Activos: contacto reciente (<= 14 días).
- Estancados: sin contacto en > 14 días.
- Calientes: respondieron / alto score (touches >= 5 o status positivo).
- Sin fecha: leads sin last_touch.

Para cada lead sugiere próximos pasos concretos.
Guarda el reporte en reports/crm_audit_latest.md.
"""

import json
from datetime import datetime, timedelta
from pathlib import Path

CRM_PATH = Path("/Users/emilioranucoli/.ranukita/ada_outreach/crm.json")
REPORTS_DIR = Path(__file__).resolve().parent / "reports"
REPORT_PATH = REPORTS_DIR / "crm_audit_latest.md"

HOY = datetime(2026, 11, 20)
LIMITE_ESTANCADO = HOY - timedelta(days=14)  # 2026-11-06

STATUSES_POSITIVOS = {
    "responded", "interested", "hot", "meeting_booked",
    "proposal_sent", "negotiation",
}


def _parse_fecha(texto):
    if not texto:
        return None
    try:
        dt = datetime.fromisoformat(texto)
        if dt.tzinfo is not None:
            dt = dt.replace(tzinfo=None)
        return dt
    except ValueError:
        return None


def _clasificar(lead):
    email = lead.get("email", "")
    nombre = lead.get("name", "")
    dominio = lead.get("domain", "")
    status = lead.get("status", "")
    touches = int(lead.get("touches", 0) or 0)
    dt = _parse_fecha(lead.get("last_touch", ""))
    dias = (HOY - dt).days if dt else None

    caliente = status in STATUSES_POSITIVOS or touches >= 5
    if caliente:
        grupo = "caliente"
    elif dt and dt < LIMITE_ESTANCADO:
        grupo = "estancado"
    elif dt is None:
        grupo = "sin_fecha"
    else:
        grupo = "activo"

    return {
        "email": email,
        "nombre": nombre,
        "dominio": dominio,
        "status": status,
        "touches": touches,
        "last_touch": lead.get("last_touch", "") or "sin fecha",
        "dias": dias,
        "grupo": grupo,
    }


def _proximo_paso(lead):
    grupo = lead["grupo"]
    status = lead["status"]
    touches = lead["touches"]
    nombre = lead["nombre"]

    if grupo == "caliente":
        if status in ("meeting_booked", "negotiation"):
            return f"Seguir el hilo y cerrar la propuesta con {nombre}."
        if status == "proposal_sent":
            return f"Hacer follow-up de la propuesta enviada a {nombre} esta semana."
        if status in ("responded", "interested", "hot"):
            return f"Responder a {nombre} y agendar una llamada de diagnóstico ADA."
        return f"Priorizar a {nombre}: alto interés, avanzar a propuesta."
    if grupo == "estancado":
        return f"Reactivar a {nombre} con un email de seguimiento (touches={touches})."
    if grupo == "sin_fecha":
        return f"Enviar primer contacto a {nombre} (lead nuevo sin rastro de outreach)."
    return f"Mantener contacto periódico con {nombre} (último toque hace {lead['dias']} días)."


def main():
    with open(CRM_PATH, encoding="utf-8") as f:
        crm = json.load(f)

    leads = [_clasificar(v) for v in crm.values()]

    grupos = {"activo": [], "estancado": [], "caliente": [], "sin_fecha": []}
    for l in leads:
        grupos[l["grupo"]].append(l)

    lineas = []
    lineas.append("# Reporte de salud de leads — CRM ADA-AUDITS")
    lineas.append("")
    lineas.append(f"Fecha de generación: {HOY.strftime('%Y-%m-%d')}")
    lineas.append(f"Total de leads: {len(leads)}")
    lineas.append("")
    lineas.append("## Resumen por grupo")
    lineas.append("")
    lineas.append("| Grupo | Cantidad |")
    lineas.append("|-------|----------|")
    for g in ("caliente", "estancado", "activo", "sin_fecha"):
        lineas.append(f"| {g.title()} | {len(grupos[g])} |")
    lineas.append("")

    for g in ("caliente", "estancado", "sin_fecha", "activo"):
        items = grupos[g]
        if not items:
            continue
        lineas.append(f"## {g.title()} ({len(items)})")
        lineas.append("")
        lineas.append("| Email | Nombre / Dominio | Status | Toques | Último toque | Días | Próximo paso |")
        lineas.append("|-------|------------------|--------|--------|--------------|------|--------------|")
        for l in items:
            nombre_dom = f"{l['nombre']} ({l['dominio']})" if l['nombre'] else l['dominio']
            dias_txt = str(l["dias"]) if l["dias"] is not None else "—"
            paso = _proximo_paso(l)
            lineas.append(
                f"| {l['email']} | {nombre_dom} | {l['status']} | {l['touches']} | "
                f"{l['last_touch']} | {dias_txt} | {paso} |"
            )
        lineas.append("")

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text("\n".join(lineas) + "\n", encoding="utf-8")
    print(f"Reporte guardado en {REPORT_PATH}")
    print(f"Leads: total={len(leads)} caliente={len(grupos['caliente'])} "
          f"estancado={len(grupos['estancado'])} activo={len(grupos['activo'])} "
          f"sin_fecha={len(grupos['sin_fecha'])}")


if __name__ == "__main__":
    main()
