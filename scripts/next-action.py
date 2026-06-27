#!/usr/bin/env python3
"""Dice la próxima acción concreta según estado del pipeline."""

import csv
import json
from datetime import date, datetime
from pathlib import Path

ROOT = Path("/Users/emilioranucoli/Desktop/ADA-AUDITS")
LEADS = ROOT / "prospectos" / "leads.csv"
URLS = ROOT / "prospectos" / "urls-del-dia.txt"
SCAN = ROOT / "prospectos" / "scan-results.json"

rows = list(csv.DictReader(open(LEADS))) if LEADS.exists() else []
rows = [r for r in rows if r.get("domain")]

sent_today = [r for r in rows if r.get("email_sent_date") == date.today().isoformat()]
need_followup_3d = []
need_followup_7d = []
today = date.today()
for r in rows:
    sent_str = r.get("email_sent_date", "")
    if (
        not sent_str
        or r.get("replied", "").lower() == "true"
        or r.get("closed", "").lower() == "true"
    ):
        continue
    try:
        sent = datetime.strptime(sent_str, "%Y-%m-%d").date()
        days = (today - sent).days
        if days == 3:
            need_followup_3d.append(r)
        elif days == 7:
            need_followup_7d.append(r)
    except Exception:
        pass

replied_open = [
    r
    for r in rows
    if r.get("replied", "").lower() == "true" and r.get("closed", "").lower() != "true"
]

urls_ready = (
    URLS.exists()
    and len([l for l in URLS.read_text().splitlines() if l.strip() and not l.startswith("#")]) > 0
)
scan_ready = SCAN.exists()

print("🎯 Próxima acción ADA Audits")
print()

if replied_open:
    print(
        f"  ⚡ URGENTE: {len(replied_open)} lead(s) respondieron y esperan tu email con el reporte:"
    )
    for r in replied_open[:3]:
        print(f"   → {r['domain']}")
    print("\n   Acción: ada report <url> → mandá Template 4 de EMAIL-TEMPLATES.md")
    exit()

if need_followup_3d:
    print(f"  📨 Mandar follow-up día +3 a {len(need_followup_3d)} lead(s):")
    for r in need_followup_3d[:5]:
        print(f"   → {r['domain']}  ({r.get('owner_email', '?')})")
    print("\n   Acción: usar Template 2 de EMAIL-TEMPLATES.md")
    exit()

if need_followup_7d:
    print(f"  📨 Último follow-up día +7 a {len(need_followup_7d)} lead(s):")
    for r in need_followup_7d[:5]:
        print(f"   → {r['domain']}")
    print("\n   Acción: usar Template 3 de EMAIL-TEMPLATES.md (cierre)")
    exit()

if len(sent_today) >= 15:
    print(f"  ✅ Ya mandaste {len(sent_today)} emails hoy. Objetivo cumplido.")
    print("   Mañana: agregar 10-15 URLs nuevas a urls-del-dia.txt y correr 'ada scan-batch'")
    exit()

if scan_ready and not urls_ready:
    print("  📝 Tenés scan listo pero no hay URLs nuevas.")
    print("   Acción: agregar 10-15 URLs nuevas en prospectos/urls-del-dia.txt")
    print("       luego: ada scan-batch")
    exit()

if urls_ready and not scan_ready:
    print("  🔍 Tenés URLs sin escanear.")
    print("   Acción: ada scan-batch")
    exit()

if scan_ready:
    scans = json.load(open(SCAN))
    leads_found = [r for r in scans if r.get("qualifies_as_lead")]
    sent_domains = {r.get("domain", "") for r in rows}
    pending = [
        r
        for r in leads_found
        if r.get("url", "")
        .replace("https://", "")
        .replace("http://", "")
        .replace("www.", "")
        .rstrip("/")
        .split("/")[0]
        not in sent_domains
    ]
    if pending:
        print(f"  📨 {len(pending)} lead(s) escaneados sin pitch enviado.")
        print("   Acción: ada pitch <url>  — generá y mandá el email.")
        for p in pending[:3]:
            print(f"     → {p['url']}")
        exit()

print("  🎨 Día limpio. Arrancá la rutina:")
print("   1. Buscar 10-15 dentistas/abogados/restaurantes en una ciudad US nueva")
print("   2. Pegarlos en prospectos/urls-del-dia.txt")
print("   3. ada scan-batch")
print("   4. ada pitch <top-lead>  × 3-5 veces")
print("   5. Mandar los emails desde Gmail (uno cada 5 min)")
