#!/usr/bin/env python3
"""Batch ADA Audit Runner: Audits a list of prospects and monitors progress.

Reads prospects from leads.csv, runs the audit pipeline for each, records
scores, violations, and generated deliverables.
"""
import csv
import json
import os
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LEADS_CSV = ROOT / "prospectos" / "leads.csv"
ENTREGABLES = ROOT / "entregables"
OUTPUT_JSON = ENTREGABLES / "batch_audit_results.json"
PROGRESS_FILE = ENTREGABLES / "batch_progress.json"

def get_prospects(limit=20):
    prospects = []
    with open(LEADS_CSV, "r", encoding="utf-8", errors="ignore") as f:
        r = csv.reader(f)
        try:
            next(r)
        except StopIteration:
            return []
        for row in r:
            if not row:
                continue
            name = row[0].strip()
            email = row[2].strip() if len(row) > 2 else ""
            domain = ""
            if "@" in email:
                domain = email.split("@")[1].strip()
            elif "." in name and " " not in name:
                domain = name.strip()
            if domain and not any(p["domain"] == domain for p in prospects):
                prospects.append({
                    "name": name,
                    "domain": domain,
                    "url": f"https://{domain}",
                    "email": email,
                })
            if len(prospects) >= limit:
                break
    return prospects

def run_single_audit(p):
    url = p["url"]
    name = p["name"]
    domain_slug = p["domain"].replace(".", "_")
    target_dir = ENTREGABLES / domain_slug
    target_dir.mkdir(parents=True, exist_ok=True)
    
    cmd = [
        sys.executable,
        str(ROOT / "scripts" / "audit-pipeline.py"),
        url,
        "--company", name
    ]
    t0 = time.time()
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=90)
        elapsed = round(time.time() - t0, 2)
        resumen_file = target_dir / "resumen-scan.json"
        pdf_file = target_dir / f"auditoria-{domain_slug}.pdf"
        html_file = target_dir / "auditoria.html"
        
        scan_data = {}
        if resumen_file.exists():
            try:
                with open(resumen_file) as rf:
                    scan_data = json.load(rf)
            except Exception:
                pass
                
        status = "success" if pdf_file.exists() else "failed"
        return {
            "name": name,
            "domain": p["domain"],
            "url": url,
            "email": p["email"],
            "status": status,
            "elapsed_seconds": elapsed,
            "score": scan_data.get("score", 0),
            "risk_level": scan_data.get("risk_level", "DESCONOCIDO"),
            "critical_count": scan_data.get("critical_count", 0),
            "serious_count": scan_data.get("serious_count", 0),
            "total_violations": scan_data.get("total_violations", 0),
            "qualifies_as_lead": scan_data.get("score", 100) < 80 or scan_data.get("critical_count", 0) > 0,
            "pdf_path": str(pdf_file) if pdf_file.exists() else None,
            "html_path": str(html_file) if html_file.exists() else None,
            "error": res.stderr[:300] if status == "failed" else None
        }
    except subprocess.TimeoutExpired:
        return {
            "name": name,
            "domain": p["domain"],
            "url": url,
            "email": p["email"],
            "status": "timeout",
            "elapsed_seconds": 90,
            "score": 0,
            "risk_level": "TIMEOUT",
            "error": "Timeout after 90s"
        }
    except Exception as e:
        return {
            "name": name,
            "domain": p["domain"],
            "url": url,
            "email": p["email"],
            "status": "error",
            "elapsed_seconds": round(time.time() - t0, 2),
            "score": 0,
            "risk_level": "ERROR",
            "error": str(e)
        }

def main():
    limit = 20
    if len(sys.argv) > 1 and sys.argv[1].isdigit():
        limit = int(sys.argv[1])
        
    prospects = get_prospects(limit=limit)
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Iniciando auditoría batch de {len(prospects)} prospectos...")
    
    ENTREGABLES.mkdir(parents=True, exist_ok=True)
    results = []
    
    for idx, p in enumerate(prospects, 1):
        print(f"[{datetime.now().strftime('%H:%M:%S')}] [{idx}/{len(prospects)}] Auditando {p['name']} ({p['url']})...", flush=True)
        r = run_single_audit(p)
        results.append(r)
        
        status_sym = "✓" if r["status"] == "success" else "✗"
        print(f"   -> {status_sym} {r['status'].upper()}: Score {r.get('score', 0)}/100 | {r.get('critical_count', 0)} criticos | {r.get('total_violations', 0)} violaciones ({r['elapsed_seconds']}s)", flush=True)
        
        # Guardar progreso parcial
        progress = {
            "timestamp": datetime.now().isoformat(),
            "completed": idx,
            "total": len(prospects),
            "current": p["domain"],
            "results": results
        }
        with open(PROGRESS_FILE, "w") as pf:
            json.dump(progress, pf, indent=2)
            
    # Guardar reporte consolidado final
    summary = {
        "timestamp": datetime.now().isoformat(),
        "total_prospects": len(prospects),
        "audited_successfully": sum(1 for r in results if r["status"] == "success"),
        "qualified_leads": sum(1 for r in results if r.get("qualifies_as_lead")),
        "avg_score": round(sum(r.get("score", 0) for r in results if r["status"] == "success") / max(1, sum(1 for r in results if r["status"] == "success")), 1),
        "results": results
    }
    with open(OUTPUT_JSON, "w") as of:
        json.dump(summary, of, indent=2)
        
    print(f"\n[{datetime.now().strftime('%H:%M:%S')}] === LOTE COMPLETADO ===")
    print(f"Auditados exitosamente: {summary['audited_successfully']}/{summary['total_prospects']}")
    print(f"Leads calificados (Score < 80 o criticos): {summary['qualified_leads']}")
    print(f"Score promedio: {summary['avg_score']}/100")
    print(f"Reporte consolidado guardado en: {OUTPUT_JSON}")

if __name__ == "__main__":
    main()
