#!/usr/bin/env python3
"""
Flujo diario completo de ADA Audits con SkyMailer.
1. Verifica emails
2. Envía pendientes con SkyMailer
3. Genera nuevos leads si queda espacio

Uso: ada-outreach-daily.py
"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"

def run_script(script_name, args=None):
    """Ejecuta un script del proyecto"""
    script_path = SCRIPTS / script_name
    cmd = ["python3", str(script_path)]
    
    if args:
        cmd.extend(args)
    
    print(f"🔧 Ejecutando: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"❌ Error en {script_name}: {result.stderr}")
        return False
    
    print(f"✅ {script_name} completado")
    return True

def main():
    print("🚀 Iniciando flujo diario de ADA Audits...")
    
    # 1. Verificar emails pendientes
    print("\n1️⃣ Verificando emails...")
    if not run_script("ada-email-verify.py"):
        print("❌ Falló la verificación de emails")
        return
    
    # 2. Enviar emails pendientes con SkyMailer
    print("\n2️⃣ Enviando emails con SkyMailer...")
    if not run_script("ada-daily-send.py"):
        print("⚠️ Falló el envío (probablemente límite diario de Gmail)")
        print("   El script reintentará automáticamente mañana")
        return
    
    # 3. Si hay espacio en el límite diario, generar nuevos leads
    print("\n3️⃣ Generando nuevos leads...")
    if not run_script("daily-auto.py"):
        print("⚠️ Falló la generación de nuevos leads")
        return
    
    print("\n🎉 Flujo diario completado exitosamente!")
    print("✅ Emails enviados, leads verificados, nueva tanda generada")

if __name__ == "__main__":
    main()