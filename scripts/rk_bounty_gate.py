#!/usr/bin/env python3
import json
import sys
import os

def validate_context(ctx):
    """Valida el contexto contra los 7 criterios del portón"""
    errors = []
    
    # 1. Código sin ejecutar (validamos que el comando se ejecutó)
    if 'validation' not in ctx or not ctx['validation']['exit_code'] == 0:
        errors.append("❌ El código no se ejecutó correctamente")
    else:
        print("✅ Código ejecutado correctamente")
    
    # 2. Archivos de nuestras herramientas
    tool_files = ['rk_aider.py', 'rk_bounty_gate.py', 'rk_git_sync.py']
    for tool_file in tool_files:
        if os.path.exists(tool_file):
            errors.append(f"❌ Archivo de herramienta encontrado: {tool_file}")
    if not errors:
        print("✅ No hay archivos de herramientas")
    
    # 3. Repo desactualizado
    if ctx.get('repo_updated') != True:
        errors.append("❌ Repo no actualizado")
    else:
        print("✅ Repo actualizado")
    
    # 4. Duplicado
    if ctx.get('duplicate') != False:
        errors.append("❌ Cambio duplicado")
    else:
        print("✅ Cambio no duplicado")
    
    # 5. Cambio que nadie pidió
    if ctx.get('requested') != False:
        errors.append("❌ Cambio no solicitado")
    else:
        print("✅ Cambio solicitado")
    
    # 6. Proceso del repo
    if ctx.get('process_followed') != True:
        errors.append("❌ Proceso no seguido")
    else:
        print("✅ Proceso seguido")
    
    # 7. Tamaño
    if ctx.get('size') not in ['small', 'medium']:
        errors.append("❌ Tamaño incorrecto")
    else:
        print("✅ Tamaño correcto")
    
    if errors:
        print("\n🚫 Portón bloqueado:")
        for error in errors:
            print(f"  {error}")
        return False
    
    print("\n✅ Portón pasado")
    return True

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python3 rk_bounty_gate.py <ctx.json>")
        sys.exit(1)
    
    ctx_file = sys.argv[1]
    with open(ctx_file, 'r') as f:
        ctx = json.load(f)
    
    success = validate_context(ctx)
    sys.exit(0 if success else 1)