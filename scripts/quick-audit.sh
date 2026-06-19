#!/usr/bin/env bash
# Quick ADA Audit — one-liner: scan + score + branded PDF
# Usage: ./quick-audit.sh <url> [company-name]
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
URL="${1:?Usage: quick-audit.sh <url> [company-name]}"
COMPANY="${2:-}"

echo "=== ADA Quick Audit ==="
echo "URL: $URL"

# 1. Run axe scan
DOMAIN=$(echo "$URL" | sed -E 's|https?://||' | cut -d/ -f1 | tr -c '[:alnum:].' '_')
OUT_DIR="$SCRIPT_DIR/../entregables/$DOMAIN"
mkdir -p "$OUT_DIR"

echo "[1/3] Running axe-core scan..."
axe "$URL" --save "$OUT_DIR/axe-raw.json" \
    --tags wcag2a,wcag2aa,wcag21aa,best-practice \
    --timeout 60 2>/dev/null || true

if [ ! -s "$OUT_DIR/axe-raw.json" ]; then
    echo "ERROR: axe scan failed. Check if URL is reachable."
    exit 1
fi

# 2. Calculate compliance score
echo "[2/3] Calculating compliance score..."
python3 "$SCRIPT_DIR/compliance_score.py" "$OUT_DIR/axe-raw.json" > "$OUT_DIR/score.json"
SCORE=$(python3 -c "import json; d=json.load(open('$OUT_DIR/score.json')); print(d['wcag_compliance_score'])")
RISK=$(python3 -c "import json; d=json.load(open('$OUT_DIR/score.json')); print(d['legal_risk'])")
VIOLATIONS=$(python3 -c "import json; d=json.load(open('$OUT_DIR/score.json')); print(d['total_violations'])")

echo "   Score: $SCORE/100 | Risk: $RISK | Violations: $VIOLATIONS"

# 3. Generate branded PDF
echo "[3/3] Generating branded PDF report..."
EXTRA_ARGS=""
if [ -n "$COMPANY" ]; then
    EXTRA_ARGS="--company \"$COMPANY\""
fi
python3 "$SCRIPT_DIR/audit-pipeline.py" "$URL" $EXTRA_ARGS

echo ""
echo "=== Done ==="
echo "Results in: $OUT_DIR/"
ls -la "$OUT_DIR/"*.pdf 2>/dev/null || echo "(PDF generation may have failed)"
