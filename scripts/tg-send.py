#!/usr/bin/env python3
"""Envía un mensaje al chat del dueño por Telegram. Lee token + chat_id de ~/ranuk-agent/bot/.env

Uso:
  echo "hola" | tg-send.py
  tg-send.py "mensaje corto"
  tg-send.py --file /path/to/file.txt
"""

import json
import os
import sys
import urllib.parse
import urllib.request
from pathlib import Path

env = {}
env_path = Path("/Users/emilioranucoli/ranuk-agent/bot/.env")
if env_path.exists():
    for line in env_path.read_text().splitlines():
        if "=" in line and not line.startswith("#"):
            k, v = line.split("=", 1)
            env[k.strip()] = v.strip().strip('"').strip("'")

token = env.get("TELEGRAM_TOKEN") or os.environ.get("TELEGRAM_TOKEN")
allowed = env.get("ALLOWED_USER_IDS") or os.environ.get("ALLOWED_USER_IDS", "")
chat_id = allowed.split(",")[0].strip() if allowed else None

if not token or not chat_id:
    print("❌ falta TELEGRAM_TOKEN o ALLOWED_USER_IDS en .env")
    sys.exit(1)

if len(sys.argv) > 1 and sys.argv[1] == "--file":
    text = Path(sys.argv[2]).read_text()
elif len(sys.argv) > 1:
    text = " ".join(sys.argv[1:])
else:
    text = sys.stdin.read()

text = text.strip()
if not text:
    sys.exit(0)

# Telegram max 4096 chars por msg. Partir si es necesario.
CHUNK = 3800
chunks = [text[i : i + CHUNK] for i in range(0, len(text), CHUNK)] or [text]

for i, chunk in enumerate(chunks):
    data = urllib.parse.urlencode(
        {
            "chat_id": chat_id,
            "text": chunk,
            "disable_web_page_preview": "true",
        }
    ).encode()
    req = urllib.request.Request(
        f"https://api.telegram.org/bot{token}/sendMessage",
        data=data,
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            json.load(r)
    except Exception as e:
        print(f"❌ chunk {i + 1}/{len(chunks)}: {e}", file=sys.stderr)
        sys.exit(1)
print(f"✅ enviado al Telegram ({len(chunks)} chunk{'s' if len(chunks) > 1 else ''})")
