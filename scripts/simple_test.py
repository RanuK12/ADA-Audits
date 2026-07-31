#!/usr/bin/env python3
import os, pathlib

BASE = pathlib.Path(os.path.expanduser('~/Desktop/Oficina_Ranuk/ADA-Audits'))
domain = "brooklynfamilydentalcare.com"

folder = BASE / 'entregables' / domain.replace('.','_')
print(f"Looking for folder: {folder}")
print(f"Folder exists: {folder.is_dir()}")

if folder.is_dir():
    resumen_path = folder / 'resumen-scan.json'
    axe_path = folder / 'axe-raw.json'
    print(f"Resumen exists: {resumen_path.is_file()}")
    print(f"Axe exists: {axe_path.is_file()}")
else:
    print("Folder not found")