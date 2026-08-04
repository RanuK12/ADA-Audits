#!/usr/bin/env python3
"""
Envío diario con SkyMailer para ADA Audits.
Respeta límites de Gmail y adjunta PDFs de auditoría personalizados.
Uso: ada-daily-send.py --max 10 --batch-size 2
"""
import csv
import json
import subprocess
import sys
import time
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"
OUTBOX = ROOT / "prospectos" / "outbox"
INDEX = OUTBOX / "index.json"
LEADS = ROOT / "prospectos" / "verified-leads.csv"
OUTPUT = ROOT / "output"
SENT_DIR = OUTBOX / "sent"

# Configuración para respetar límites de Gmail
MAX_DAILY = 5  # Límite reducido para evitar exceder el límite real
BATCH_SIZE = 1  # Enviar uno a la vez para mejor control
DELAY_BETWEEN_BATCHES = 120  # Segundos entre lotes
DELAY_BETWEEN_EMAILS = 180  # Tiempo más largo entre emails

def load_index():
    """Carga el índice del outbox"""
    if INDEX.exists():
        return json.load(open(INDEX))
    return []

def save_index(data):
    """Guarda el índice del outbox"""
    json.dump(data, open(INDEX, 'w'), indent=2)

def get_pdf_for_domain(domain):
    """Busca PDF de auditoría para el dominio"""
    pdf_pattern = f"ADA_Audit_{domain.replace('.', '_')}.pdf"
    pdf_path = OUTPUT / pdf_pattern
    if pdf_path.exists():
        return str(pdf_path)
    return None

def send_email_with_skymailer(entry):
    """Envía email individual con SkyMailer"""
    # Preparar HTML body
    html_path = Path('/tmp/ada_email_body.html')
    html_content = f"<html><body>{entry['body'].replace('\n','<br>')}</body></html>"
    html_path.write_text(html_content)
    
    # Construir comando
    cmd = [
        str(Path.home() / 'Apps' / 'ranukita-bridge' / 'scripts' / 'rk-skymailer-send'),
        '--to', entry['to'],
        '--subject', entry['subject'],
        '--html-file', str(html_path)
    ]
    
    # Adjuntar PDF si existe
    pdf_path = get_pdf_for_domain(entry['domain'])
    if pdf_path:
        cmd.extend(['--attach', pdf_path])
    
    # Ejecutar
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    # Verificar resultado
    if result.returncode != 0:
        print(f"⚠️ Error enviando a {entry['to']}: {result.stderr.strip()}")
        return False
    
    # Verificar respuesta JSON
    try:
        resp = json.loads(result.stdout.strip())
        if resp.get('status') != 'sent':
            print(f"⚠️ SkyMailer devolvió: {resp}")
            return False
    except Exception as e:
        print(f"⚠️ No se pudo parsear respuesta SkyMailer: {e}")
        return False
    
    return True

def main():
    # Cargar pendientes
    index = load_index()
    pending = [e for e in index if e.get('status') == 'pending']
    
    if not pending:
        print('✅ No hay emails pendientes')
        return
    
    print(f"📧 {len(pending)} emails pendientes")
    
    # Verificar límite diario
    sent_today = len([e for e in index if e.get('status') == 'sent' and e.get('sent_date', '').startswith('2026-08-04')])
    remaining_today = MAX_DAILY - sent_today
    
    if remaining_today <= 0:
        print('❌ Límite diario de Gmail alcanzado. Esperando mañana.')
        return
    
    # Limitar según lo que queda hoy
    to_send = min(remaining_today, len(pending), BATCH_SIZE)
    batch = pending[:to_send]
    
    print(f'🚀 Enviando lote de {to_send} emails ({remaining_today} restantes hoy)')
    
    # Enviar lote
    sent_count = 0
    for i, entry in enumerate(batch):
        print(f'📤 Enviando {i+1}/{to_send}: {entry["to"]}')
        
        if send_email_with_skymailer(entry):
            # Marcar como enviado
            entry['status'] = 'sent'
            entry['sent_date'] = date.today().isoformat()
            
            # Mover archivo a sent/
            src = OUTBOX / entry['filename']
            dst = SENT_DIR / entry['filename']
            if src.exists():
                src.rename(dst)
            
            sent_count += 1
            print(f'✅ Enviado exitosamente: {entry["to"]}')
        else:
            print(f'❌ Falló: {entry["to"]}')
        
        # Esperar antes del siguiente email
        if i < len(batch) - 1:
            print(f'⏱️ Esperando {DELAY_BETWEEN_EMAILS}s...')
            time.sleep(DELAY_BETWEEN_EMAILS)
    
    # Guardar cambios
    save_index(index)
    
    print(f'🎉 Lote completado: {sent_count}/{to_send} enviados')
    
    if sent_count == to_send:
        # Si se envió todo el lote, esperar antes del siguiente lote
        if remaining_today > to_send:
            print(f'⏱️ Próximo lote en {DELAY_BETWEEN_BATCHES}s...')
            time.sleep(DELAY_BETWEEN_BATCHES)
            print('✅ Listo para próximo lote')

if __name__ == "__main__":
    main()