#!/usr/bin/env python3
# © 2026 Ranuk IT Solutions — ranuk.dev
"""ADA Audits Campaign Dispatcher: Sends queued outreach emails via SkyMailer.

Features:
- Full visual HTML standard support with embedded CID logo.
- Idempotent and resumable (skips already sent emails).
- Anti-spam pacing (default 45s interval).
- Comprehensive audit logging in logs/campaign_send.log.
- Support for --dry-run and --limit.
"""
import argparse
import json
import os
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_MASTER_JSON = ROOT / "prospectos" / "outbox" / "campaign_visual_master.json"
LOG_FILE = ROOT / "logs" / "campaign_send.log"
LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

BANNER_LOGO = Path.home() / "Apps" / "ranukita-bridge" / "assets" / "ranuk-email-header-640.png"
SKYMAILER_SEND = Path("/Users/emilioranucoli/Apps/ranukita-bridge/scripts/rk-skymailer-send")

def log(msg):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line, flush=True)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(line + "\n")

def send_one(entry, dry_run=False):
    to_email = entry["to"]
    subject = entry["subject"]
    html_path = entry.get("html_path")
    
    if dry_run:
        mode = f"HTML ({html_path})" if html_path else "PLAIN"
        log(f"[DRY-RUN] Would send to {to_email} | Mode: {mode} | Subject: '{subject}'")
        return True, "dry_run"

    cmd = [
        str(SKYMAILER_SEND),
        "--to", to_email,
        "--subject", subject,
    ]

    if html_path and os.path.exists(html_path):
        cmd.extend(["--html-file", str(html_path)])
        if BANNER_LOGO.exists():
            cmd.extend(["--inline", f"ranuklogo={str(BANNER_LOGO)}"])
    else:
        body = entry.get("body", "")
        cmd.extend(["--body", body, "--plain"])

    try:
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=35)
        if res.returncode == 0:
            log(f"[SENT] To: {to_email} | {res.stdout.strip()}")
            return True, res.stdout.strip()
        else:
            err = res.stderr.strip() or res.stdout.strip()
            log(f"[ERROR] To: {to_email} | Code {res.returncode}: {err}")
            return False, err
    except Exception as e:
        log(f"[EXCEPTION] To: {to_email} | {e}")
        return False, str(e)

def main():
    parser = argparse.ArgumentParser(description="ADA Audits 50 Campaign Sender")
    parser.add_argument("--master", type=str, default=str(DEFAULT_MASTER_JSON), help="Path to master campaign json")
    parser.add_argument("--dry-run", action="store_true", help="Simulate sends without dispatching")
    parser.add_argument("--limit", type=int, default=0, help="Limit number of emails to send (0 = all)")
    parser.add_argument("--interval", type=int, default=45, help="Seconds to sleep between sends (default: 45)")
    args = parser.parse_args()

    master_path = Path(args.master)
    if not master_path.exists():
        log(f"Error: Master file not found at {master_path}")
        sys.exit(1)

    with open(master_path, "r", encoding="utf-8") as f:
        entries = json.load(f)

    pending = [e for e in entries if e.get("status") != "sent"]
    log(f"Iniciando dispatcher: {len(pending)} pendientes de {len(entries)} totales. (Intervalo: {args.interval}s)")

    if args.limit > 0:
        pending = pending[:args.limit]
        log(f"Limitando envío a los primeros {len(pending)} correos.")

    sent_count = 0
    fail_count = 0

    for idx, item in enumerate(pending, 1):
        dom = item["domain"]
        to_email = item["to"]
        log(f"[{idx}/{len(pending)}] Enviando #{item['index']:02d} ({dom} -> {to_email})...")

        ok, output = send_one(item, dry_run=args.dry_run)
        if ok and not args.dry_run:
            item["status"] = "sent"
            item["sent_at"] = datetime.now().isoformat()
            item["sent_output"] = output
            sent_count += 1
            # Actualizar master tras cada envío para persistencia
            with open(master_path, "w", encoding="utf-8") as f:
                json.dump(entries, f, indent=2, ensure_ascii=False)

            # Registrar en cache_gmail_sent.json para evitar recontacto futuro
            cache_file = Path.home() / ".ranukita" / "ada_outreach" / "cache_gmail_sent.json"
            if cache_file.exists():
                try:
                    c_data = json.loads(cache_file.read_text())
                    if to_email.lower() not in c_data:
                        c_data.append(to_email.lower())
                        cache_file.write_text(json.dumps(c_data, indent=2))
                except Exception:
                    pass

            # Registrar en leads.csv
            leads_csv = ROOT / "prospectos" / "leads.csv"
            if leads_csv.exists():
                try:
                    with open(leads_csv, "a", encoding="utf-8") as lf:
                        today_str = datetime.now().strftime("%Y-%m-%d")
                        row_vals = [
                            "pending", dom, item.get("business_name", ""),
                            item.get("first_name", "") or "", to_email,
                            "", "", "", str(item.get("score", "")), str(item.get("nodes", "")),
                            "", "", "", today_str, "false", "false", "0", "Campaign visual batch"
                        ]
                        lf.write(",".join(f'"{v}"' if "," in v else v for v in row_vals) + "\n")
                except Exception:
                    pass
        elif not ok and not args.dry_run:
            item["status"] = "failed"
            item["last_error"] = output
            fail_count += 1
            with open(master_path, "w", encoding="utf-8") as f:
                json.dump(entries, f, indent=2, ensure_ascii=False)

        if idx < len(pending) and not args.dry_run:
            log(f"Pausa de seguridad anti-spam: esperando {args.interval}s...")
            time.sleep(args.interval)

    log(f"=== DISPATCH COMPLETADO ===")
    log(f"Enviados con éxito: {sent_count} | Fallidos: {fail_count} | Pendientes restantes: {len(entries) - sent_count}")

if __name__ == "__main__":
    main()
