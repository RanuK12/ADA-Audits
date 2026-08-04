#!/usr/bin/env python3
"""
Sistema de seguimiento de respuestas y follow-ups para ADA Audits.
Uso: ada-follow-up-tracker.py --status-file follow-up-status.json
"""
import csv
import json
import os
from pathlib import Path
from datetime import datetime, timedelta

ROOT = Path(__file__).resolve().parent.parent
LEADS = ROOT / "prospectos" / "leads_cleaned.csv"
STATUS_FILE = ROOT / "outbox" / "follow-up-status.json"
FOLLOWUP_SCHEDULE = {
    'day1': 1,    # 1 día después
    'day3': 3,    # 3 días después
    'day7': 7,    # 7 días después
    'day14': 14   # 14 días después
}

def load_leads():
    """Carga leads desde CSV"""
    with open(LEADS) as f:
        return list(csv.DictReader(f))

def load_followup_status():
    """Carga estado de seguimiento"""
    if STATUS_FILE.exists():
        with open(STATUS_FILE) as f:
            return json.load(f)
    return {}

def save_followup_status(status):
    """Guarda estado de seguimiento"""
    with open(STATUS_FILE, 'w') as f:
        json.dump(status, f, indent=2)

def update_lead_status(lead, status_key, value):
    """Actualiza status de un lead"""
    if 'status_updates' not in lead:
        lead['status_updates'] = {}
    lead['status_updates'][status_key] = value
    return lead

def check_and_schedule_followups():
    """Verifica respuestas y programa follow-ups"""
    leads = load_leads()
    followup_status = load_followup_status()
    
    today = datetime.now()
    scheduled_actions = []
    
    for lead in leads:
        email = lead.get('owner_email')
        if not email:
            continue
            
        # Si el lead fue enviado pero no respondido
        if lead.get('status') == 'sent' and not lead.get('replied'):
            sent_date = lead.get('email_sent_date')
            if not sent_date:
                continue
                
            sent_datetime = datetime.strptime(sent_date, '%Y-%m-%d')
            days_since_sent = (today - sent_datetime).days
            
            # Verificar si es momento para follow-up
            for followup_day in FOLLOWUP_SCHEDULE.values():
                if days_since_sent == followup_day:
                    followup_key = f"followup_day{followup_day}"
                    
                    if email not in followup_status or followup_key not in followup_status[email]:
                        # Programar follow-up
                        scheduled_actions.append({
                            'email': email,
                            'business_name': lead.get('business_name', ''),
                            'followup_day': followup_day,
                            'action': 'send_followup'
                        })
                        
                        # Marcar como programado
                        if email not in followup_status:
                            followup_status[email] = {}
                        followup_status[email][followup_key] = {
                            'scheduled': today.strftime('%Y-%m-%d'),
                            'sent': False
                        }
                        
                        print(f"🔄 Follow-up programado para {email} (día {followup_day})")
    
    # Guardar estado actualizado
    save_followup_status(followup_status)
    
    return scheduled_actions

def generate_followup_email(lead, followup_day):
    """Genera email de follow-up"""
    business_name = lead.get('business_name', 'su negocio')
    
    if followup_day == 1:
        subject = f"Seguimiento: Propuesta de Accesibilidad Web para {business_name}"
        body = f"""
Hola,

Le escribo para hacer seguimiento a mi propuesta de mejora de accesibilidad web para {business_name}.

Sé que está ocupado, pero quería asegurarme de que mi email anterior no se perdió en su bandeja de entrada.

La accesibilidad web no solo es una cuestión legal (ADA), sino también de negocio: sitios accesibles tienen mejor conversión y llegan a más clientes.

¿Le interesaría agendar esa breve llamada de 15 minutos para discutir los hallazgos de su auditoría inicial gratuita?

Atentamente,
Emilio Ranucoli
"""
    elif followup_day == 3:
        subject = f"Recordatorio: Accesibilidad Web - {business_name}"
        body = f"""
Hola,

Un recordatorio amistoso sobre mi propuesta de accesibilidad web para {business_name}.

En la ADA, la prevención es clave. Muchos negocios no se dan cuenta de los problemas de accesibilidad hasta que enfrentan una demanda.

¿Tendría 15 minutos esta semana para revisar los hallazgos de su auditoría gratuita?

Saludos,
Emilio Ranucoli
"""
    elif followup_day == 7:
        subject = f"Último intento: Propuesta ADA para {business_name}"
        body = f"""
Hola,

Este es mi último intento de contacto sobre la mejora de accesibilidad web para {business_name.

La normativa de accesibilidad web se está volviendo cada vez más estricta. En 2025, el número de demandas por accesibilidad web aumentó un 45%.

Mi oferta de auditoría inicial gratuita sigue abierta. ¿Le interesaría aprovecharla antes de que sea demasiado tarde?

Atentamente,
Emilio Ranucoli
"""
    else:
        subject = f"Recomendación de Accesibilidad Web para {business_name}"
        body = f"""
Hola,

Aunque no he recibido respuesta, considero importante compartirle que la accesibilidad web es crucial para cualquier negocio en la actualidad.

En Ranuk IT Solutions, ayudamos negocios como {business_name} a cumplir con la ADA y mejorar su experiencia de usuario.

Si en algún momento necesita nuestros servicios, estaré encantado de ayudarle.

Saludos cordiales,
Emilio Ranucoli
"""
    
    return subject, body

def main():
    print("🔄 ADA Follow-up Tracker - Verificando respuestas...")
    
    # Verificar y programar follow-ups
    scheduled_actions = check_and_schedule_followups()
    
    if scheduled_actions:
        print(f"\n📅 {len(scheduled_actions)} acciones programadas:")
        for action in scheduled_actions:
            print(f"   - {action['email']} (día {action['followup_day']})")
    else:
        print("✅ No hay follow-ups pendientes en este momento")
    
    # Guardar reporte
    report = {
        'date': datetime.now().strftime('%Y-%m-%d'),
        'actions_scheduled': len(scheduled_actions),
        'actions': scheduled_actions
    }
    
    with open(ROOT / "outbox" / "followup-report.json", 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"\n📊 Reporte guardado en followup-report.json")

if __name__ == "__main__":
    main()