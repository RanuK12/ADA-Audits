#!/usr/bin/env python3
# © 2026 Ranuk IT Solutions — ranuk.dev
"""scrape_batch2_30.py — Scraper multi-país de 30 prospectos frescos y reales.
Objetivo:
- ES (España): 12 SMBs reales con web activa y MX verificado.
- US (Estados Unidos): 12 SMBs reales con web activa y MX verificado.
- IT (Italia): 6 SMBs reales con web activa y MX verificado.
- 0 duplicados contra cache_gmail_sent.json, campaign_multicountry_30.json y leads.csv.
"""
import html as _h
import json
import os
import re
import subprocess
import sys
import time
import urllib.parse
import urllib.request
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LOGDIR = Path.home() / ".ranukita" / "ada_outreach"
LOGDIR.mkdir(parents=True, exist_ok=True)

# 1. Cargar exclusiones
cache_sent = set()
cache_f = LOGDIR / "cache_gmail_sent.json"
if cache_f.exists():
    try:
        cache_sent = {x.lower().strip() for x in json.loads(cache_f.read_text())}
    except Exception:
        pass

c30_f = ROOT / "prospectos" / "outbox" / "campaign_multicountry_30.json"
campaign_30 = set()
if c30_f.exists():
    try:
        for it in json.loads(c30_f.read_text()):
            campaign_30.add(it["to"].lower().strip())
            campaign_30.add(it["domain"].lower().strip())
    except Exception:
        pass

leads_csv_f = ROOT / "prospectos" / "leads.csv"
leads_csv_set = set()
if leads_csv_f.exists():
    for line in leads_csv_f.read_text(errors="ignore").splitlines():
        for p in line.split(","):
            val = p.strip().strip("\"'").lower()
            if "@" in val or "." in val:
                leads_csv_set.add(val)

EXCLUDE = cache_sent | campaign_30 | leads_csv_set
print(f"Total exclusiones (ya enviados o encolados): {len(EXCLUDE)}")

BLACKLIST_DOMAINS = {
    "google.com", "apple.com", "microsoft.com", "ey.com", "pwc.com", "deloitte.com",
    "kpmg.com", "bain.com", "bain.it", "fsitaliane.it", "rfi.it", "cbre.es",
    "compass.com", "kia.es", "kia.com", "amaris.com", "tecnocasa.es", "alquilerseguro.es",
    "msearchadvisory.com", "facebook.com", "instagram.com", "linkedin.com", "twitter.com"
}

OVERPASS_SERVERS = [
    "https://overpass.openstreetmap.fr/api/interpreter",
    "https://overpass.kumi.systems/api/interpreter",
    "https://overpass-api.de/api/interpreter",
]

TARGETS = [
    # España
    {"country": "ES", "city": "Barcelona", "bbox": (41.36, 2.12, 41.44, 2.22), "lang": "es", "tags": ['"amenity"="dentist"', '"amenity"="clinic"', '"amenity"="pharmacy"', '"shop"="optician"', '"office"="architect"', '"office"="lawyer"']},
    {"country": "ES", "city": "Valencia", "bbox": (39.44, -0.41, 39.51, -0.33), "lang": "es", "tags": ['"amenity"="dentist"', '"amenity"="veterinary"', '"shop"="travel_agency"', '"office"="consulting"', '"office"="advertising_agency"']},
    {"country": "ES", "city": "Sevilla", "bbox": (37.36, -6.01, 37.42, -5.95), "lang": "es", "tags": ['"amenity"="dentist"', '"amenity"="clinic"', '"shop"="optician"', '"office"="lawyer"']},
    {"country": "ES", "city": "Málaga", "bbox": (36.70, -4.46, 36.75, -4.40), "lang": "es", "tags": ['"amenity"="dentist"', '"tourism"="hotel"', '"office"="estate_agent"']},

    # Estados Unidos
    {"country": "US", "city": "Austin", "bbox": (30.22, -97.78, 30.34, -97.70), "lang": "en", "tags": ['"amenity"="dentist"', '"amenity"="clinic"', '"amenity"="veterinary"', '"office"="lawyer"', '"office"="advertising_agency"']},
    {"country": "US", "city": "Denver", "bbox": (39.70, -105.02, 39.78, -104.92), "lang": "en", "tags": ['"amenity"="dentist"', '"amenity"="clinic"', '"leisure"="fitness_centre"', '"office"="architect"']},
    {"country": "US", "city": "San Diego", "bbox": (32.70, -117.20, 32.78, -117.12), "lang": "en", "tags": ['"amenity"="dentist"', '"amenity"="clinic"', '"tourism"="hotel"', '"office"="lawyer"']},
    {"country": "US", "city": "Chicago", "bbox": (41.85, -87.68, 41.93, -87.61), "lang": "en", "tags": ['"amenity"="dentist"', '"office"="consulting"', '"office"="lawyer"', '"office"="financial"']},

    # Italia
    {"country": "IT", "city": "Milano", "bbox": (45.44, 9.15, 45.50, 9.23), "lang": "it", "tags": ['"office"="lawyer"', '"office"="architect"', '"amenity"="dentist"', '"office"="graphic_design"', '"office"="consulting"']},
    {"country": "IT", "city": "Torino", "bbox": (45.04, 7.64, 45.10, 7.72), "lang": "it", "tags": ['"office"="lawyer"', '"amenity"="clinic"', '"amenity"="dentist"', '"tourism"="hotel"']},
    {"country": "IT", "city": "Bologna", "bbox": (44.48, 11.31, 44.52, 11.37), "lang": "it", "tags": ['"office"="lawyer"', '"office"="consulting"', '"amenity"="dentist"', '"office"="it"']},
]

def has_mx(domain):
    try:
        r = subprocess.run(["dig", "+short", "MX", domain], capture_output=True, text=True, timeout=6)
        if r.stdout.strip():
            return True
        r_a = subprocess.run(["dig", "+short", "A", domain], capture_output=True, text=True, timeout=6)
        return bool(r_a.stdout.strip())
    except Exception:
        return False

def query_overpass(bbox, tag, limit=15):
    s, w, n, e = bbox
    q = f'[out:json][timeout:20];node[{tag}]["website"]({s},{w},{n},{e});out {limit};'
    for srv in OVERPASS_SERVERS:
        try:
            req = urllib.request.Request(
                srv,
                data=urllib.parse.urlencode({"data": q}).encode(),
                headers={"User-Agent": "RanukADA/2.0"}
            )
            with urllib.request.urlopen(req, timeout=20) as resp:
                data = json.loads(resp.read())
                elems = data.get("elements", [])
                out = []
                for el in elems:
                    t = el.get("tags", {})
                    name = t.get("name")
                    web = t.get("website") or t.get("contact:website", "")
                    osm_email = t.get("email") or t.get("contact:email", "")
                    if name and web:
                        out.append({"name": name, "website": web, "osm_email": osm_email})
                if out:
                    return out
        except Exception:
            continue
    return []

EMAIL_RE = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")

def scrape_email_from_web(url):
    if not url.startswith("http"):
        url = "https://" + url
    parsed = urllib.parse.urlparse(url)
    dom = parsed.netloc.replace("www.", "").lower()
    
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"}
    emails_found = []
    
    # 1. Probar Home
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=8) as r:
            html = r.read().decode("utf-8", errors="ignore")
            # mails en mailto
            for m in re.findall(r'mailto:([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})', html):
                emails_found.append(m.lower())
            for m in EMAIL_RE.findall(html):
                emails_found.append(m.lower())
    except Exception:
        pass
    
    # 2. Probar /contact o /contacto
    if not emails_found:
        for path in ["/contact", "/contacto", "/contatti", "/about"]:
            try:
                c_url = f"{parsed.scheme}://{parsed.netloc}{path}"
                req = urllib.request.Request(c_url, headers=headers)
                with urllib.request.urlopen(req, timeout=6) as r:
                    html = r.read().decode("utf-8", errors="ignore")
                    for m in re.findall(r'mailto:([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})', html):
                        emails_found.append(m.lower())
                    for m in EMAIL_RE.findall(html):
                        emails_found.append(m.lower())
                if emails_found:
                    break
            except Exception:
                pass
    
    # Filtrar emails de imágenes (.png, .jpg) o proveedores comunes de plugins (sentry, gravatar, wix, wordpress)
    junk = ("sentry", "gravatar", "w3.org", "schema.org", "wixpress", "example", "domain.com", ".png", ".jpg", ".webp")
    clean = []
    for em in emails_found:
        if any(j in em for j in junk):
            continue
        # Preferir mails del mismo dominio
        if dom in em:
            return em, "real" if not em.startswith(("info@", "contact@", "contacto@", "hola@")) else "role"
        clean.append(em)
    
    if clean:
        return clean[0], "role"
    return None, None

def main():
    results = {"ES": [], "US": [], "IT": []}
    targets_needed = {"ES": 12, "US": 12, "IT": 6}
    seen_domains = set()

    print("Iniciando escaneo multi-país de prospectos...")

    for tgt in TARGETS:
        country = tgt["country"]
        if len(results[country]) >= targets_needed[country]:
            continue
        
        city = tgt["city"]
        bbox = tgt["bbox"]
        lang = tgt["lang"]
        
        print(f"\n--- Explorando {city} ({country}) ---")
        for tag in tgt["tags"]:
            if len(results[country]) >= targets_needed[country]:
                break
            
            elements = query_overpass(bbox, tag, limit=12)
            for el in elements:
                if len(results[country]) >= targets_needed[country]:
                    break
                
                raw_web = el["website"].strip()
                dom = urllib.parse.urlparse(raw_web if raw_web.startswith("http") else "http://" + raw_web).netloc.replace("www.", "").lower()
                
                if not dom or "." not in dom or dom in seen_domains or dom in EXCLUDE or dom in BLACKLIST_DOMAINS:
                    continue
                
                # Check MX primero
                if not has_mx(dom):
                    continue
                
                email = el.get("osm_email", "").strip().lower()
                quality = "osm" if email else None
                
                if not email:
                    email, quality = scrape_email_from_web(raw_web)
                
                if not email or "@" not in email:
                    continue
                
                email = email.split(";")[0].split(",")[0].strip()
                if email in EXCLUDE:
                    continue
                
                seen_domains.add(dom)
                lead = {
                    "name": el["name"],
                    "domain": dom,
                    "website": raw_web,
                    "email": email,
                    "country": country,
                    "city": city,
                    "lang": lang,
                    "quality": quality or "real"
                }
                results[country].append(lead)
                print(f"  ✓ [{country}] {el['name'][:24]:24} | {dom:24} | {email} ({quality})")
                time.sleep(0.5)

    print("\n================== RESUMEN SCRAPING ==================")
    total = sum(len(v) for v in results.values())
    for c, items in results.items():
        print(f"[{c}] Obtenidos: {len(items)} / {targets_needed[c]}")
    
    out_file = LOGDIR / "fresh_scraped_batch2_30.json"
    flat_list = []
    for c in ["ES", "US", "IT"]:
        flat_list.extend(results[c][:targets_needed[c]])
    
    out_file.write_text(json.dumps(flat_list, indent=2, ensure_ascii=False))
    print(f"Guardados {len(flat_list)} prospectos en: {out_file}")

if __name__ == "__main__":
    main()
