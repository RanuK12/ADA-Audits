#!/bin/bash
# Batch audit for remaining leads — [ranukita:87d6fb]
cd /Users/emilioranucoli/Desktop/Oficina_Ranuk/ADA-AUDITS

declare -A LEADS
LEADS=(
  ["https://rk.com"]="RK Netmedia Inc."
  ["https://easterneffects.com"]="Eastern Effects"
  ["https://fortluft.com"]="Fortluft"
  ["https://genius.com"]="Genius"
  ["https://wearesignsny.com"]="We Are Signs & Awnings"
  ["https://thedentalspany.com"]="The Dental Spa of New York"
  ["https://instantrealtyinc.com"]="Instant Realty, Inc."
  ["https://crmjewelers.com"]="CRM Jewelers"
  ["https://whitestonediamonds.com"]="Whitestone Diamonds"
  ["https://heyrowan.com"]="Rowan"
  ["https://puntoottico.it"]="Punto Ottico"
  ["https://locations.tgifridays.com"]="TGI Fridays"
  ["https://lelandbrooklyn.com"]="Leland"
  ["https://onelovevet.com"]="One Love Animal Hospital"
  ["https://smalldoorvet.com"]="Small Door Vet"
  ["https://thegardenvet.com"]="Carroll Gardens Veterinary Group"
)

for url in "${!LEADS[@]}"; do
  company="${LEADS[$url]}"
  echo "=== $url -> $company ==="
  python3 scripts/audit-pipeline.py "$url" --company "$company" 2>&1
  echo "---"
done

echo "BATCH DONE"