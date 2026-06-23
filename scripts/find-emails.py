#!/usr/bin/env python3
"""Email finder heurístico. Gratis, sin API. Scrapea /, /contact, /about.

Uso: find-emails.py <url>
Imprime JSON: {"emails":[...], "best":"primero@dominio.com", "owner_name":"..."}
"""
import json
import re
import sys
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor

url = sys.argv[1]
base = url.rstrip("/")

EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,6}")
NAME_PATTERNS = [
    re.compile(r"(?:Dr\.|Doctor|Mr\.|Mrs\.|Ms\.)\s+([A-Z][a-z]+\s+[A-Z][a-z]+)"),
    re.compile(r"(?:founder|owner|CEO|Dr\.|dentist|attorney)[^a-zA-Z]{0,20}([A-Z][a-z]+\s+[A-Z][a-z]+)", re.IGNORECASE),
    re.compile(r"([A-Z][a-z]+\s+[A-Z][a-z]+)[,\s]+(?:DDS|DMD|MD|Esq|PhD|JD)"),
]

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_0) AppleWebKit/605.1.15"

def fetch(u, timeout=12):
    try:
        req = urllib.request.Request(u, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.read().decode("utf-8", errors="ignore")
    except Exception:
        return ""

def score_email(e, host):
    e = e.lower()
    s = 0
    # preferir emails en el dominio del sitio
    domain = host.split(".")[-2] if "." in host else ""
    if domain and domain in e:
        s += 20
    # penalizar obvios no-contacto
    for bad in ["@sentry", "@wixpress", "@wordpress", "@godaddy", "@cloudflare",
                "noreply", "no-reply", "donotreply", "example.com", "yoursite",
                "domain.com", "@2x.png", ".jpg", ".png", ".svg"]:
        if bad in e:
            return -100
    # bonus por tipo de mailbox
    for good in ["info@", "contact@", "hello@", "office@", "admin@", "reception@"]:
        if e.startswith(good):
            s += 10
    # personal (firstname@) = highest
    if re.match(r"^[a-z]+@", e) and not any(e.startswith(g) for g in ["info@","contact@","hello@","office@","admin@","reception@","support@","sales@","marketing@","hr@","jobs@"]):
        s += 15
    return s

host = urllib.parse.urlparse(url).netloc
paths = ["", "/contact", "/contact-us", "/contactus", "/about", "/about-us", "/aboutus", "/team", "/our-team"]

all_html = ""
with ThreadPoolExecutor(max_workers=4) as ex:
    htmls = list(ex.map(lambda p: fetch(base + p), paths))
all_html = " ".join(htmls)

# Buscar emails
raw_emails = set(EMAIL_RE.findall(all_html))
# Filtrar obviamente basura
clean = []
for e in raw_emails:
    if not any(ext in e.lower() for ext in [".png", ".jpg", ".svg", ".webp", ".gif"]):
        clean.append(e.lower())

# Rankear
ranked = sorted(clean, key=lambda e: -score_email(e, host))
good = [e for e in ranked if score_email(e, host) > 0]

# Buscar nombre de owner
name = None
for pat in NAME_PATTERNS:
    m = pat.search(all_html)
    if m:
        name = m.group(1)
        break

out = {
    "url": url,
    "host": host,
    "emails_found": good[:5],
    "all_emails": ranked[:10],
    "best_email": good[0] if good else (ranked[0] if ranked else None),
    "owner_name": name,
    "first_name": name.split()[0] if name else None,
}
print(json.dumps(out, ensure_ascii=False, indent=2))
