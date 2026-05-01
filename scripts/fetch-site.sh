#!/usr/bin/env bash
# Descarga HTML renderizado de una URL + 3 páginas más enlazadas para auditar.
# Uso: ./fetch-site.sh https://cliente.com output-folder

set -euo pipefail

URL="${1:-}"
OUT="${2:-./out}"

if [[ -z "$URL" ]]; then
  echo "Uso: $0 <url> [carpeta-salida]"
  exit 1
fi

mkdir -p "$OUT"
UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 13_0) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15"

echo "→ Descargando home: $URL"
curl -sL -A "$UA" "$URL" -o "$OUT/00-home.html"

echo "→ Ejecutando axe-core (requiere: npm i -g @axe-core/cli)"
if command -v axe >/dev/null 2>&1; then
  axe "$URL" --save "$OUT/axe-report.json" --tags wcag2a,wcag2aa,wcag21aa || true
else
  echo "  ⚠ axe no instalado. Instalar: npm i -g @axe-core/cli puppeteer"
fi

echo "→ Lighthouse (requiere: npm i -g lighthouse)"
if command -v lighthouse >/dev/null 2>&1; then
  lighthouse "$URL" --only-categories=accessibility --output=json --output-path="$OUT/lighthouse.json" --quiet --chrome-flags="--headless" || true
fi

echo "→ Extrayendo links internos de home"
grep -oE 'href="[^"]+"' "$OUT/00-home.html" \
  | sed -E 's/href="([^"]+)"/\1/' \
  | grep -iE "^(/|${URL})" \
  | sort -u \
  | head -5 > "$OUT/links.txt"

i=1
while IFS= read -r link; do
  [[ "$link" =~ ^/ ]] && link="${URL%/}$link"
  echo "→ Descargando $link"
  curl -sL -A "$UA" "$link" -o "$OUT/0${i}-page.html" || true
  i=$((i+1))
done < "$OUT/links.txt"

echo "✅ Listo en $OUT/"
ls -la "$OUT/"
