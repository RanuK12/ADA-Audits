#!/usr/bin/env python3
"""Generate ADA Audits landing page."""
import os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "index.html")

def w(s):
    with open(OUT, 'a') as f:
        f.write(s)

# Clear file
with open(OUT, 'w') as f:
    f.write('')

CSS = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'styles.css')).read()

HTML = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'body.html')).read()

w('<!DOCTYPE html>\n<html lang="en">\n<head>\n')
w('<meta charset="UTF-8">\n')
w('<meta name="viewport" content="width=device-width, initial-scale=1.0">\n')
w('<title>ADA Audits - WCAG 2.1 AA Accessibility Compliance</title>\n')
w('<meta name="description" content="Full WCAG 2.1 AA accessibility audit. Fix legal risks, expand audience, boost SEO.">\n')
w('<style>\n' + CSS + '\n</style>\n')
w('</head>\n<body>\n')
w(HTML)
w('\n<script>\n')
JS = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'script.js')).read()
w(JS)
w('\n</script>\n</body>\n</html>\n')
print(f"Done: {OUT} ({os.path.getsize(OUT)} bytes)")
