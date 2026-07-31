#!/usr/bin/env python3
import os, pathlib
BASE = pathlib.Path(os.path.expanduser('~/Desktop/Oficina_Ranuk/ADA-Audits'))

domain = "brooklynfamilydentalcare.com"
print(f"Testing domain: {domain}")

folder1 = BASE / 'entregables' / f"{domain.replace('.','_')}_com"
folder2 = BASE / 'entregables' / domain
folder3 = BASE / 'entregables' / domain.replace('.','_')

print(f"Folder 1: {folder1}")
print(f"Folder 1 exists: {folder1.is_dir()}")
print(f"Folder 2: {folder2}")
print(f"Folder 2 exists: {folder2.is_dir()}")
print(f"Folder 3: {folder3}")
print(f"Folder 3 exists: {folder3.is_dir()}")

if folder1.is_dir():
    resumen_path = folder1 / 'resumen-scan.json'
    axe_path = folder1 / 'axe-raw.json'
    print(f"Resumen: {resumen_path}")
    print(f"Resumen exists: {resumen_path.is_file()}")
    print(f"Axe: {axe_path}")
    print(f"Axe exists: {axe_path.is_file()}")