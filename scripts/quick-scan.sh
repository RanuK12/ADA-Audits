#!/usr/bin/env bash
# Escaneo rápido de accesibilidad — 30s por sitio.
# Devuelve JSON con score, hallazgos top, y flag de lead.
#
# Uso:
#   ./quick-scan.sh https://cliente.com
#   ./quick-scan.sh -f urls.txt

set -uo pipefail

scan_one() {
  local URL="$1"
  local DOMAIN
  DOMAIN=$(echo "$URL" | sed -E 's|https?://||' | cut -d/ -f1 | tr -c '[:alnum:].' '_')
  local OUT="/tmp/ada-scan-${DOMAIN}.json"

  (cd /tmp && axe "$URL" --save "ada-scan-${DOMAIN}.json" \
      --tags wcag2a,wcag2aa,wcag21aa,best-practice \
      --timeout 45 >/dev/null 2>&1) || true

  if [[ ! -s "$OUT" ]]; then
    echo "{\"url\":\"$URL\",\"error\":\"scan_failed\",\"qualifies_as_lead\":false}"
    return
  fi

  python3 - "$URL" "$OUT" <<'PY'
import json, sys
url = sys.argv[1]
try:
    with open(sys.argv[2]) as f:
        data = json.load(f)
except Exception as e:
    print(json.dumps({"url": url, "error": str(e), "qualifies_as_lead": False}))
    sys.exit()
if isinstance(data, list):
    data = data[0] if data else {}
violations = data.get("violations", [])
critical = [v for v in violations if v.get("impact") == "critical"]
serious  = [v for v in violations if v.get("impact") == "serious"]
moderate = [v for v in violations if v.get("impact") == "moderate"]
total_nodes = sum(len(v.get("nodes", [])) for v in violations)
score = max(0, 100 - len(critical)*8 - len(serious)*4 - len(moderate)*2 - (len(violations)-len(critical)-len(serious)-len(moderate)))
top3 = sorted(violations, key=lambda v: {"critical":0,"serious":1,"moderate":2,"minor":3}.get(v.get("impact","minor"),4))[:3]

def sample_node(v):
    nodes = v.get("nodes", [])
    if not nodes: return ""
    html = nodes[0].get("html","")[:200]
    return html

out = {
    "url": url,
    "score": score,
    "critical_count": len(critical),
    "serious_count": len(serious),
    "moderate_count": len(moderate),
    "total_violations": len(violations),
    "total_nodes_affected": total_nodes,
    "top_issues": [
        {
            "id": t["id"],
            "impact": t.get("impact"),
            "help": t.get("help"),
            "nodes_affected": len(t.get("nodes",[])),
            "sample_html": sample_node(t),
        }
        for t in top3
    ],
    "qualifies_as_lead": (len(critical) + len(serious)) >= 2 or total_nodes >= 10,
}
print(json.dumps(out, ensure_ascii=False))
PY
}

if [[ "${1:-}" == "-f" ]]; then
  FILE="$2"
  echo "["
  first=1
  while IFS= read -r url; do
    [[ -z "$url" || "$url" =~ ^# ]] && continue
    [[ $first -eq 0 ]] && echo ","
    scan_one "$url"
    first=0
  done < "$FILE"
  echo "]"
else
  scan_one "$1"
fi
