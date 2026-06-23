#!/usr/bin/env python3
"""Busca URLs de negocios en una ciudad+vertical usando DuckDuckGo HTML (gratis, sin API key).

Uso: find-urls.py "<vertical>" "<city-state>"
Ejemplo: find-urls.py "dentist" "Brooklyn NY"

Output: una URL por línea, a stdout.
"""
import re
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

vertical = sys.argv[1] if len(sys.argv) > 1 else "dentist"
location = sys.argv[2] if len(sys.argv) > 2 else "Brooklyn NY"

# Dominios a descartar (directorios y agregadores)
BLACKLIST = {
    "yelp.com", "zocdoc.com", "healthgrades.com", "yellowpages.com",
    "facebook.com", "instagram.com", "linkedin.com", "twitter.com", "x.com",
    "google.com", "maps.google.com", "bing.com", "duckduckgo.com",
    "indeed.com", "bbb.org", "nextdoor.com", "angi.com", "homeadvisor.com",
    "manta.com", "superpages.com", "citysearch.com", "wikipedia.org",
    "yahoo.com", "chamber.co", "thumbtack.com", "reddit.com", "youtube.com",
    "pinterest.com", "tiktok.com", "apple.com", "amazon.com", "opendi.us",
    "mapquest.com", "tripadvisor.com", "doctor.com", "wellness.com",
    "vitals.com", "ratemds.com", "sharecare.com", "doctorsnetwork.com",
    "webmd.com", "mayoclinic.org", "healthline.com",
}

def ddg_search(query, max_results=25):
    """Scrapea resultados de DuckDuckGo HTML (no requiere API key)."""
    url = "https://html.duckduckgo.com/html/?q=" + urllib.parse.quote(query)
    req = urllib.request.Request(url, headers={
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_0) AppleWebKit/605.1.15",
        "Accept-Language": "en-US,en;q=0.9",
    })
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            html = r.read().decode("utf-8", errors="ignore")
    except Exception as e:
        print(f"# ddg error: {e}", file=sys.stderr)
        return []

    # DDG HTML: <a class="result__a" href="//duckduckgo.com/l/?uddg=ENCODED_URL&...">
    results = []
    for m in re.finditer(r'href="[^"]*uddg=([^&"]+)', html):
        try:
            u = urllib.parse.unquote(m.group(1))
            if u.startswith("http"):
                results.append(u)
        except Exception:
            pass
    # Fallback: direct links
    for m in re.finditer(r'class="result__a"[^>]*href="(https?://[^"]+)"', html):
        results.append(m.group(1))
    return results[:max_results]


def clean_domain(url):
    try:
        p = urllib.parse.urlparse(url)
        host = p.netloc.lower().replace("www.", "")
        return host
    except Exception:
        return ""


def is_business_site(url):
    host = clean_domain(url)
    if not host:
        return False
    if any(host.endswith(b) or b in host for b in BLACKLIST):
        return False
    # Preferir dominios que sugieran negocio propio
    return True


def root_url(url):
    p = urllib.parse.urlparse(url)
    return f"{p.scheme}://{p.netloc}/"


# Consultas múltiples para diversificar
queries = [
    f'"{vertical}" "{location}" -site:yelp.com -site:zocdoc.com',
    f'{vertical} {location} office website',
    f'best {vertical} {location}',
]

seen = set()
output = []
for q in queries:
    results = ddg_search(q, max_results=15)
    for u in results:
        if is_business_site(u):
            root = root_url(u)
            host = clean_domain(root)
            if host and host not in seen:
                seen.add(host)
                output.append(root)
    time.sleep(1.5)  # cortesía
    if len(output) >= 20:
        break

# Filtrar contra leads ya existentes
leads_csv = Path("/Users/emilioranucoli/Desktop/ADA-AUDITS/prospectos/leads.csv")
already = set()
if leads_csv.exists():
    import csv
    for row in csv.DictReader(open(leads_csv)):
        if row.get("domain"):
            already.add(row["domain"].lower().replace("www.",""))

fresh = [u for u in output if clean_domain(u) not in already]

for u in fresh[:15]:
    print(u)

print(f"# {len(fresh)} URLs nuevas encontradas para '{vertical} {location}'", file=sys.stderr)
