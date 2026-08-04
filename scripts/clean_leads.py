#!/usr/bin/env python3
import csv
import json
import re
import sys
import os

# Función para validar email
def is_valid_email(email):
    if not email or email.strip() == "":
        return False
    
    # Regex básico para email
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email.strip()) is not None

# Función para limpiar el CSV
def clean_csv():
    input_file = 'prospectos/leads.csv'
    output_file = 'prospectos/leads_cleaned.csv'
    rejected_file = 'prospectos/rejected-emails.json'
    
    valid_emails = []
    invalid_emails = []
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            
            # Escribir header en el archivo limpio
            with open(output_file, 'w', encoding='utf-8', newline='') as out_f:
                writer = csv.DictWriter(out_f, fieldnames=reader.fieldnames)
                writer.writeheader()
                
                for row in reader:
                    email = row.get('owner_email', '')
                    
                    # Saltar filas vacías
                    if not email or email.strip() == "":
                        continue
                    
                    if is_valid_email(email):
                        valid_emails.append(email)
                        writer.writerow(row)
                    else:
                        invalid_emails.append({
                            'email': email,
                            'domain': row.get('domain', ''),
                            'business_name': row.get('business_name', ''),
                            'reason': 'invalid_format'
                        })
        
        # Guardar emails rechazados
        with open(rejected_file, 'w', encoding='utf-8') as rej_f:
            json.dump(invalid_emails, rej_f, indent=2)
        
        print(f"✅ CSV limpio: {len(valid_emails)} emails válidos")
        print(f"❌ Rechazados: {len(invalid_emails)} emails inválidos")
        
        # Guardar lista de emails válidos para el script de envío
        os.makedirs('../outbox', exist_ok=True)
        with open('outbox/valid_emails.txt', 'w', encoding='utf-8') as emails_f:
            for email in valid_emails:
                emails_f.write(f"{email}\n")
        
        return valid_emails, invalid_emails
        
    except Exception as e:
        print(f"❌ Error al limpiar CSV: {e}")
        return [], []

if __name__ == "__main__":
    clean_csv()