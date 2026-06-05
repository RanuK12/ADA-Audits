#!/usr/bin/env python3
"""ADA-AUDITS Outreach Email Generator."""
import argparse, csv, json, os, sys
from datetime import datetime
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
TEMPLATES_DIR = SCRIPT_DIR / "templates"
OUTPUT_DIR = SCRIPT_DIR / "emails"

SECTOR_MAP = {
    "ecommerce": "ecommerce", "e-commerce": "ecommerce", "retail": "ecommerce",
    "fintech": "fintech", "finance": "fintech", "legal": "fintech",
    "banking": "fintech", "insurance": "fintech", "law": "fintech",
    "healthtech": "healthtech", "health": "healthtech", "medical": "healthtech",
    "dental": "healthtech", "chiro": "healthtech", "medspa": "healthtech",
    "fitness": "healthtech", "restaurant": "healthtech", "hotel": "healthtech",
    "saas": "saas", "software": "saas", "tech": "saas", "startup": "saas",
    "gaming": "gaming", "game": "gaming", "esports": "gaming", "entertainment": "gaming",
}
DEFAULT_SECTOR = "ecommerce"

def load_templates():
    t = {}
    for f in TEMPLATES_DIR.glob("*.json"):
        with open(f) as fp:
            d = json.load(fp); t[d["sector"]] = d
    return t

def guess_sector(s, domain="", bname=""):
    text = " ".join([s or "", domain, bname]).lower().strip()
    # Health/dental/chiro/medical/fitness first (most common in our leads)
    health_kw = ["dental", "dentist", "chiro", "medical", "health", "derma", "derm",
                  "clinic", "medspa", "spa", "fitness", "gym", "wellness",
                  "restaurant", "hotel", "salon", "plastic", "surgery", "beauty",
                  "eat", "pizza", "food", "cafe", "bistro", "grill", "kitchen"]
    for kw in health_kw:
        if kw in text: return "healthtech"
    # Fintech / legal
    legal_kw = ["law", "legal", "injury", "attorney", "fintech", "finance", "bank", "insurance"]
    for kw in legal_kw:
        if kw in text: return "fintech"
    # E-commerce
    ecom_kw = ["shop", "store", "buy", "commerce", "product", "brand", "boutique", "market"]
    for kw in ecom_kw:
        if kw in text: return "ecommerce"
    # SaaS / tech
    saas_kw = ["saas", "software", "app", "platform", "tech", "cloud", "api"]
    for kw in saas_kw:
        if kw in text: return "saas"
    # Gaming
    gaming_kw = ["game", "gaming", "esport", "studio"]
    for kw in gaming_kw:
        if kw in text: return "gaming"
    return DEFAULT_SECTOR

def parse_scan(sd, dom):
    if not sd or not os.path.isdir(sd): return {}
    p2 = Path(sd)
    for x in [p2/dom/"scan.json", p2/f"{dom}.json", p2/f"{dom}-scan.json"]:
        if x.exists():
            with open(x) as f: return json.load(f)
    return {}

def render(tpl, d):
    vm = {
        "domain": d.get("domain", ""),
        "business_name": d.get("business_name", "your company"),
        "first_name": d.get("first_name", "there"),
        "email": d.get("email", ""),
        "total_issues": str(d.get("total_issues", 20)),
        "top_issue_1": d.get("top_issue_1", "Multiple elements with missing ARIA labels"),
        "top_issue_2": d.get("top_issue_2", "Color contrast below WCAG 4.5:1"),
        "top_issue_3": d.get("top_issue_3", "No semantic landmarks or heading hierarchy"),
    }
    def _replace(t):
        result = t
        for k, v in vm.items():
            result = result.replace("{{" + k + "}}", v)
        return result
    return {
        "to": d.get("email", ""),
        "domain": d.get("domain", ""),
        "business_name": d.get("business_name", ""),
        "sector": tpl["sector"],
        "subject": _replace(tpl["subject"]),
        "body": _replace(tpl["body"]),
    }

def fmt(e, n):
    sep = "=" * 60
    line = "-" * 60
    bn = e["business_name"]
    sc = e["sector"].upper()
    to = e["to"]
    subj = e["subject"]
    bd = e["body"]
    dom = e["domain"]
    sc_l = e["sector"]
    today = datetime.now().strftime("%Y-%m-%d")
    parts = [
        "EMAIL #%d -- %s [%s]" % (n, bn, sc), sep, "",
        "TO:       %s" % to,
        "SUBJECT:  %s" % subj, "", line,
        "BODY (copy from line below)", line, "",
        bd, "", line,
        "STATUS:   pending",
        "DOMAIN:   %s" % dom,
        "SECTOR:   %s" % sc_l,
        "CREATED:  %s" % today, "",
    ]
    return "\n".join(parts)

def process(csv_path, tpls, scan_dir=None, quick=False, sector_ov=None):
    res, n = [], 0
    with open(csv_path, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            dom = r.get("domain", "").strip()
            em = r.get("owner_email", "").strip()
            if not dom or not em or r.get("status", "").strip() == "closed":
                continue
            sec = sector_ov or guess_sector(r.get("industry", ""), dom, r.get("business_name", ""))
            tpl = tpls.get(sec, tpls.get(DEFAULT_SECTOR))
            d = {"domain": dom, "business_name": r.get("business_name", dom),
                 "first_name": r.get("owner_name", "there"), "email": em}
            if not quick and scan_dir:
                sc = parse_scan(scan_dir, dom)
                if sc:
                    d["total_issues"] = sc.get("total_issues", 25)
                    iss = sc.get("issues", [])
                    for i in range(min(3, len(iss))):
                        d["top_issue_%d" % (i+1)] = iss[i]
                else:
                    d["top_issue_1"] = r.get("top_issue_1", "") or "Multiple WCAG 2.1 AA violations"
                    d["top_issue_2"] = r.get("top_issue_2", "") or "Color contrast failures"
                    d["top_issue_3"] = r.get("top_issue_3", "") or "Missing semantic landmarks"
            n += 1
            fn = "%02d-%s.txt" % (n, dom.replace(".", "-"))
            res.append((fn, render(tpl, d)))
    return res

def main():
    ap = argparse.ArgumentParser(description="Generador emails outreach ADA-AUDITS")
    ap.add_argument("--prospects")
    ap.add_argument("--scan-dir")
    ap.add_argument("--quick", action="store_true")
    ap.add_argument("--sector")
    ap.add_argument("--list-sectors", action="store_true")
    ap.add_argument("--output")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--domain")
    ap.add_argument("--business-name")
    ap.add_argument("--email")
    ap.add_argument("--first-name")
    a = ap.parse_args()
    tpls = load_templates()
    if a.list_sectors:
        print("Sectores:")
        for s, t in tpls.items():
            print("  %-12s -- %s" % (s, t.get("label", s)))
        return
    out = Path(a.output) if a.output else OUTPUT_DIR
    out.mkdir(parents=True, exist_ok=True)
    if a.domain and a.email:
        sec = a.sector or DEFAULT_SECTOR
        tpl = tpls.get(sec, tpls.get(DEFAULT_SECTOR))
        d = {"domain": a.domain, "business_name": a.business_name or a.domain,
             "first_name": a.first_name or "there", "email": a.email}
        e = render(tpl, d)
        if a.dry_run:
            print(fmt(e, 1))
        else:
            fname = "01-" + a.domain.replace(".", "-") + ".txt"
            (out / fname).write_text(fmt(e, 1), encoding="utf-8")
            print("OK: %s" % (out / fname))
        return
    if not a.prospects:
        print("Error: --prospects o --domain/--email requerido")
        sys.exit(1)
    results = process(a.prospects, tpls, a.scan_dir, a.quick, a.sector)
    if not results:
        print("Sin leads para generar.")
        return
    print("Generando %d emails..." % len(results))
    for fn, e in results:
        if a.dry_run:
            print(fmt(e, int(fn[:2])))
        else:
            (out / fn).write_text(fmt(e, int(fn[:2])), encoding="utf-8")
            print("  %s" % fn)
    if not a.dry_run:
        print("\n%d emails en %s/" % (len(results), out))
        print("Revisar, personalizar nombre real, enviar con SkyMailer.")

if __name__ == "__main__":
    main()
