#!/usr/bin/env python3
"""Batch audit for remaining leads — [ranukita:87d6fb]"""
import subprocess, sys
from pathlib import Path

LEADS = [
    ("https://rk.com", "RK Netmedia Inc."),
    ("https://easterneffects.com", "Eastern Effects"),
    ("https://fortluft.com", "Fortluft"),
    ("https://genius.com", "Genius"),
    ("https://wearesignsny.com", "We Are Signs & Awnings"),
    ("https://thedentalspany.com", "The Dental Spa of New York"),
    ("https://instantrealtyinc.com", "Instant Realty, Inc."),
    ("https://crmjewelers.com", "CRM Jewelers"),
    ("https://whitestonediamonds.com", "Whitestone Diamonds"),
    ("https://heyrowan.com", "Rowan"),
    ("https://puntoottico.it", "Punto Ottico"),
    ("https://locations.tgifridays.com", "TGI Fridays"),
    ("https://lelandbrooklyn.com", "Leland"),
    ("https://onelovevet.com", "One Love Animal Hospital"),
    ("https://smalldoorvet.com", "Small Door Vet"),
    ("https://thegardenvet.com", "Carroll Gardens Veterinary Group"),
]

BASE = Path(__file__).resolve().parent.parent
PIPELINE = BASE / "scripts" / "audit-pipeline.py"

ok, fail = [], []
for url, company in LEADS:
    print(f"\n=== {url} -> {company} ===", flush=True)
    r = subprocess.run(
        [sys.executable, str(PIPELINE), url, "--company", company],
        cwd=BASE, capture_output=False, timeout=120
    )
    if r.returncode == 0:
        ok.append(url)
    else:
        fail.append(url)

print(f"\n=== DONE === OK: {len(ok)} | FAIL: {len(fail)}")
if fail:
    for f in fail:
        print(f"  FAIL: {f}")