import json, subprocess, sys
from playwright.sync_api import sync_playwright

URL = "https://wsyasociados.com.ar/"
AXE = "https://cdnjs.cloudflare.com/ajax/libs/axe-core/4.10.2/axe.min.js"

with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome")
    pg = b.new_page(viewport={"width":1280,"height":900})
    pg.goto(URL, wait_until="load", timeout=90000)
    pg.wait_for_timeout(4000)
    pg.add_script_tag(url=AXE)
    res = pg.evaluate("async () => await axe.run(document, {runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21a','wcag21aa','best-practice']}})")
    json.dump(res, open("axe_raw.json","w"), ensure_ascii=False, indent=1)
    pg.screenshot(path="home.png", full_page=False)
    b.close()
print("violations:", len(res["violations"]))
for v in res["violations"]:
    print(f"- {v['id']} [{v['impact']}] x{len(v['nodes'])} :: {v['help']}")
