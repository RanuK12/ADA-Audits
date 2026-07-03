#!/usr/bin/env python3
"""Daily automation: busca URLs nuevas, escanea, pitchea, encuentra emails y manda todo al Telegram.

Se ejecuta 1x/día vía launchd. Rotación automática de verticales+ciudades.

Lógica:
 1. Si hay follow-ups pendientes hoy → los manda al Telegram.
 2. Si hay leads escaneados sin pitch → genera pitches y los manda.
 3. Si no → elige vertical+ciudad del día, busca URLs, escanea, pitchea, manda.
"""
import csv
import json
import re
import subprocess
from datetime import date, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"
PROSPECTOS = ROOT / "prospectos"
LEADS = PROSPECTOS / "leads.csv"
SCAN = PROSPECTOS / "scan-results.json"
URLS = PROSPECTOS / "urls-del-dia.txt"
STATE = PROSPECTOS / ".rotation-state.json"
LOG = ROOT / "logs" / "daily-auto.log"
LOG.parent.mkdir(exist_ok=True)

# Rotación: cada día un combo distinto
ROTATIONS = [
    ("dentist", "Brooklyn NY"),
    ("chiropractor", "Miami FL"),
    ("boutique hotel", "Manhattan NY"),
    ("personal injury lawyer", "Philadelphia PA"),
    ("restaurant", "Austin TX"),
    ("dentist", "Queens NY"),
    ("plastic surgeon", "Los Angeles CA"),
    ("dermatologist", "Miami FL"),
    ("pediatric dentist", "San Diego CA"),
    ("family law attorney", "Chicago IL"),
    ("veterinarian", "Denver CO"),
    ("med spa", "Scottsdale AZ"),
    ("orthodontist", "Dallas TX"),
    ("physical therapy", "Boston MA"),
]


def run(cmd, timeout=1800, capture=True):
    return subprocess.run(cmd, capture_output=capture, text=True, timeout=timeout)


def log(msg):
    with open(LOG, "a") as f:
        f.write(f"{datetime.now().isoformat()} {msg}\n")


def tg(msg):
    p = subprocess.Popen([str(SCRIPTS / "tg-send.py")],
                         stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    p.communicate(msg.encode())


def next_rotation():
    if STATE.exists():
        try:
            s = json.load(open(STATE))
            idx = (s.get("idx", -1) + 1) % len(ROTATIONS)
        except Exception:
            idx = 0
    else:
        idx = 0
    json.dump({"idx": idx, "date": date.today().isoformat()}, open(STATE, "w"))
    return ROTATIONS[idx]


def check_followups():
    """Leads que necesitan follow-up hoy (día +3 o día +7 desde envío)."""
    if not LEADS.exists():
        return [], []
    today = date.today()
    d3, d7 = [], []
    for r in csv.DictReader(open(LEADS)):
        sent = r.get("email_sent_date", "")
        if not sent or r.get("replied", "").lower() == "true" or r.get("closed", "").lower() == "true":
            continue
        try:
            sent_date = datetime.strptime(sent, "%Y-%m-%d").date()
            days = (today - sent_date).days
            if days == 3:
                d3.append(r)
            elif days == 7:
                d7.append(r)
        except Exception:
            pass
    return d3, d7


def pending_pitches():
    """Leads escaneados sin pitch enviado."""
    if not SCAN.exists() or not LEADS.exists():
        return []
    scans = json.load(open(SCAN))
    sent_domains = set()
    for r in csv.DictReader(open(LEADS)):
        if r.get("domain"):
            sent_domains.add(r["domain"].lower().replace("www.", ""))
    pending = []
    for r in scans:
        if not r.get("qualifies_as_lead"):
            continue
        url = r.get("url", "")
        host = url.replace("https://", "").replace("http://", "").replace("www.", "").rstrip("/").split("/")[0]
        if host and host not in sent_domains:
            pending.append(r)
    return pending


def find_email(url):
    try:
        out = run([str(SCRIPTS / "find-emails.py"), url], timeout=30)
        if out.returncode == 0:
            return json.loads(out.stdout)
    except Exception as e:
        log(f"find-email err {url}: {e}")
    return {}


def generate_pitch(url):
    try:
        out = run([str(SCRIPTS / "ada"), "pitch", url], timeout=30)
        return out.stdout
    except Exception as e:
        return f"❌ pitch error: {e}"


# ============ MAIN FLOW ============

def main():
    log("=== daily-auto start ===")
    parts = [f"🌅 *Daily Brief ADA Audits* — {date.today().isoformat()}"]
    parts.append("")

    # 1. Follow-ups primero
    d3, d7 = check_followups()
    if d3:
        parts.append(f"📨 *Follow-up día +3* ({len(d3)} leads):")
        for r in d3[:5]:
            parts.append(f"  • {r.get('domain','?')} ({r.get('owner_email','')})")
        parts.append("  → usar Template 2 de EMAIL-TEMPLATES.md\n")
    if d7:
        parts.append(f"📨 *Último follow-up día +7* ({len(d7)} leads):")
        for r in d7[:5]:
            parts.append(f"  • {r.get('domain','?')}")
        parts.append("  → usar Template 3 (cierre)\n")

    # 2. Pitches pendientes de scans previos → agregarlos al OUTBOX automáticamente
    pend = pending_pitches()
    if pend:
        added_now = []
        for lead in pend[:5]:  # top 5 leads nuevos por batch
            url = lead["url"]
            email_info = find_email(url)
            to_email = email_info.get("best_email")
            first_name = email_info.get("first_name") or "there"

            # Si no se encontró email, usar genérico basado en el dominio
            if not to_email:
                host = re.sub(r"^https?://(www\.)?", "", url).rstrip("/").split("/")[0]
                to_email = f"info@{host}"

            # Ubicar el scan file correcto
            scan_file = SCAN  # default
            # buscar también en batches/
            for candidate in (PROSPECTOS / "batches").glob("*-scan.json") if (PROSPECTOS / "batches").exists() else []:
                try:
                    data = json.load(open(candidate))
                    if any(r.get("url", "").rstrip("/") == url.rstrip("/") for r in data):
                        scan_file = candidate
                        break
                except Exception:
                    pass

            # Agregar al outbox
            r = run([str(SCRIPTS / "outbox.py"), "add", url, to_email, first_name, str(scan_file)], timeout=30)
            if r.returncode == 0 and "añadido" in (r.stdout or ""):
                added_now.append({"url": url, "to": to_email, "first": first_name})
                log(f"outbox+ {url} → {to_email}")

        if added_now:
            parts.append(f"🎯 *{len(added_now)} nuevo(s) email(s) listos en tu outbox*\n")
            for a in added_now:
                host = re.sub(r"^https?://(www\.)?", "", a["url"]).rstrip("/").split("/")[0]
                parts.append(f"  • {host}  →  {a['to']}")
            parts.append("")
            parts.append("📋 Para ver y mandar desde Telegram:")
            parts.append("  `outbox`         → lista completa con números")
            parts.append("  `email <n>`      → te paso el email #N listo para copiar")
            parts.append("  `sent <n>`       → lo marco como enviado cuando lo mandes")
            parts.append("")

    # 3. Si no hay pendientes, buscar nuevos
    if not pend and not d3 and not d7:
        vertical, city = next_rotation()
        parts.append(f"🔍 *Buscando leads nuevos*: {vertical} en {city}")
        log(f"searching {vertical} / {city}")

        r = run([str(SCRIPTS / "find-urls.py"), vertical, city], timeout=60)
        urls = [l for l in r.stdout.strip().split("\n") if l.strip().startswith("http")]
        parts.append(f"  → {len(urls)} URLs encontradas\n")

        if urls:
            URLS.write_text("\n".join(urls) + "\n")
            parts.append("🔎 *Escaneando...* (esto puede tardar 5-15 min, el scan corre en background)")
            # Correr scan en background
            subprocess.Popen(
                [str(SCRIPTS / "ada"), "scan-batch"],
                stdout=open(ROOT / "logs" / "scan.log", "a"),
                stderr=subprocess.STDOUT,
            )
            parts.append("  → Cuando termine, mañana vas a tener los pitches listos acá.")
            parts.append("  → O pedile al bot: `próxima acción`")
        else:
            parts.append("⚠️ No hubo resultados. Mañana probamos otro combo.")

    if len(parts) == 2:  # solo el header
        parts.append("✅ Día limpio. Todo bajo control.")
        parts.append("Pipeline: usá `pipeline` en el bot para ver métricas.")

    msg = "\n".join(parts)
    tg(msg)
    log(f"sent {len(msg)} chars")
    log("=== daily-auto end ===")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        log(f"FATAL: {e}")
        tg(f"❌ daily-auto crasheó: {e}")
        raise
