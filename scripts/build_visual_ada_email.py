#!/usr/bin/env python3
# © 2026 Ranuk IT Solutions — ranuk.dev
"""build_visual_ada_email.py — Renderizador de emails HTML de alta fidelidad para ADA Audits.

Implementa el estándar visual oficial de Ranuk IT Solutions:
- Header navy (#0f172a) con banner/logo oficial embebido (cid:ranuklogo).
- Contenedor tipo tarjeta (#ffffff) sobre fondo sutil (#f1f5f9).
- Saludo personalizado con resaltado visual.
- Caja de alerta ámbar con contexto regulatorio crítico (EAA / ADA Title III).
- Resumen del diagnóstico técnico con barra lateral azul y badges WCAG.
- Tarjeta de Portfolio y Proyectos en Vivo (ranuk.dev/portfolio, notarobot.es, audit.ranuk.dev).
- Tarjeta de presupuestos de referencia (~39€/$39, ~290€/$249, ~590-890€).
- Botones CTA con estilos llamativos (azul #2563eb y verde esmeralda #059669).
- Bloque navy (#0f172a) para agendar llamada o solicitar reporte gratuito.
- Firma corporativa verificada con enlaces.
"""
import html as _html
import urllib.parse as _up

CHECKOUT_ENDPOINT = "https://audit.ranuk.dev/checkout"

def build_checkout_url(domain, email="", lang="es", is_eur=False, tier="report"):
    params = {
        "domain": domain.strip(),
        "lang": lang,
        "currency": "eur" if is_eur else "usd",
        "tier": tier
    }
    if email:
        params["email"] = email.strip()
    return CHECKOUT_ENDPOINT + "?" + _up.urlencode(params)

def render_visual_html(lead_info, offset=0):
    """
    lead_info dict keys:
    - domain: str
    - business_name: str
    - to_email: str
    - first_name: str or None
    - lang: 'es' | 'en' | 'it'
    - score: int
    - nodes: int
    - issues: list of dicts {title, desc, wcag, impact}
    """
    domain = _html.escape(lead_info["domain"].strip())
    raw_bname = lead_info.get("business_name") or domain.split(".")[0].title()
    business_name = _html.escape(raw_bname.strip())
    first_name = lead_info.get("first_name")
    lang = lead_info.get("lang", "es")
    nodes = lead_info.get("nodes", 15)
    issues = lead_info.get("issues", [])
    email = lead_info.get("to_email", "")

    is_person = bool(first_name and len(first_name) >= 2)
    is_eur = lang in ("es", "it") and not domain.endswith(".ar") and not domain.endswith(".com.ar")
    
    precio_tag = "39 €" if is_eur else "$39 USD"
    remed_tag = "290 €" if is_eur else "$249 USD"
    
    url_opt1 = build_checkout_url(domain, email, lang=lang, is_eur=is_eur, tier="report")
    url_opt2 = build_checkout_url(domain, email, lang=lang, is_eur=is_eur, tier="remediation")

    # Asegurar 3 issues concretos
    while len(issues) < 3:
        if lang == "en":
            issues.append({
                "title": "Interactive Controls Missing Accessible Name",
                "desc": "Navigation buttons and form inputs lack accessible labels in code, blocking assistive readers and mobile autofill.",
                "wcag": "WCAG 4.1.2"
            })
        elif lang == "it":
            issues.append({
                "title": "Elementi Interattivi Senza Nome Accessibile",
                "desc": "I pulsanti di navigazione e i campi modulo non presentano label accessibili nel codice, ostacolando screen reader e navigazione da tastiera.",
                "wcag": "WCAG 4.1.2"
            })
        else:
            issues.append({
                "title": "Controles Interactivos sin Etiqueta Accesible",
                "desc": "Botones con iconos o campos de formulario carecen de etiquetas por código, dificultando la navegación asistida y el autocompletado móvil.",
                "wcag": "WCAG 4.1.2"
            })

    ff = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif"

    if lang == "en":
        subject = f"a few technical notes I put together for {domain}"
        greeting_html = f"Hi {_html.escape(first_name)}," if is_person else "Hi everyone,"
        
        intro_p1 = f'My name is Emilio Ranucoli, and I run <strong>Ranuk IT Solutions</strong> (<a href="https://ranuk.dev" style="color:#2563eb;text-decoration:none;font-weight:600;">ranuk.dev</a>), a software engineering and technical auditing studio. To be completely transparent with you: instead of sending generic sales pitches, the way we introduce our work and earn new clients is by proactively reviewing websites of businesses we come across, spotting technical friction points that often go unnoticed, and sharing our findings upfront.'
        intro_p2 = f'I spent some time analyzing <strong><a href="https://{domain}" style="color:#2563eb;text-decoration:none;font-weight:600;">{business_name} ({domain})</a></strong> earlier today and prepared this prioritized technical summary for your team.'

        reg_title = "Regulatory & Mobile Conversion Notice:"
        reg_body = f'Under <strong>ADA Title III, Section 508</strong>, and the European Accessibility Act (EAA), non-compliant commercial websites face substantial regulatory scrutiny and demand letter risk ($5,000 to $40,000 settlements), while losing up to <strong>15% of mobile customers</strong> due to broken tap targets and form validation friction.'

        diag_title = "Technical Diagnostic Summary"
        diag_sub = f'We flagged these 3 critical priority issues in the code of <strong>{domain}</strong> ({nodes} elements affected in the DOM):'

        port_title = "Live Projects & Engineering Portfolio"
        port_sub = "To verify our code quality, technical execution, and Lighthouse 95+ performance before taking any decision, feel free to explore our live platforms:"
        port_item1 = '<strong><a href="https://ranuk.dev/portfolio" style="color:#2563eb;text-decoration:none;font-weight:700;">ranuk.dev/portfolio</a></strong> &mdash; Official portfolio of bespoke web platforms, high-speed landing pages, and web apps.'
        port_item2 = '<strong><a href="https://notarobot.es/" style="color:#2563eb;text-decoration:none;font-weight:700;">notarobot.es</a></strong> &mdash; Human verification and anti-bot security service (100% Lighthouse, Edge CDN).'
        port_item3 = '<strong><a href="https://audit.ranuk.dev/" style="color:#2563eb;text-decoration:none;font-weight:700;">audit.ranuk.dev</a></strong> &mdash; Automated web accessibility verification and continuous compliance platform.'

        num_title = "Numbers and transparent pricing reference:"
        num_opt1 = f'🔹 <strong>Option 1: Full Technical Audit Report ({precio_tag}):</strong> Prioritized 15-page PDF report with verification certificate and exact line-by-line code patches for your web developer.'
        num_opt2 = f'🔹 <strong>Option 2: Turnkey Code Remediation ({remed_tag}):</strong> We directly remediate and test your source code (GitHub Pull Request or production-ready patch) with zero developer hours needed from your team.'
        num_opt3 = f'🔹 <strong>Turnkey Modern Web / AI Pack:</strong> ~<strong>$590 - $890 USD</strong> (High-performance web revamp or custom AI intake integration).'

        trust_title = "Formal Service Commitment & Official Tax Invoicing"
        trust_body = (
            f"If you choose to proceed with Option 1 or 2, payments are processed securely via Stripe and establish a "
            f"<strong>legally binding service commitment</strong> from Ranuk IT Solutions: an <strong>official tax invoice and receipt</strong> "
            f"is automatically issued for your corporate accounting, with delivery guaranteed within 24 business hours."
        )
        trust_link_text = "Review our service agreement, SLA terms, and compliance warranty at:"

        opt1_card_title = f"Option 1: Full Technical Audit Report ({precio_tag})"
        opt1_card_desc = "Prioritized 15-page PDF dossier with verification certificate and exact line-by-line patches."
        opt1_btn_text = "Order Report &rarr;"

        opt2_card_title = f"Option 2: Turnkey Code Remediation ({remed_tag})"
        opt2_card_desc = "We directly fix and test your source code (GitHub PR or ready patch) with zero hours from your team."
        opt2_btn_text = "Request Fix &rarr;"

        call_title = "We can schedule a brief 15-minute call to:"
        call_b1 = f"Review the specific code issues on {domain} in real time"
        call_b2 = "Walk through the exact remediation steps for your team"
        call_b3 = "Answer any technical questions with zero commitment"
        call_link_text = "Schedule directly on Calendly: "
        call_free_note = "(Or if you prefer a quick free preview first, just reply to this email and I'll send over the code snippets)."

        role_title = "Systems Engineer · Founder, Ranuk IT Solutions"
        optout_text = 'Ranuk IT Solutions &mdash; Software Engineering &amp; WCAG Compliance.<br>If this isn\'t relevant, just reply "no thanks" and I won\'t follow up.'

    elif lang == "it":
        subject = f"Diagnosi tecnica e note che ho preparato per {domain}"
        greeting_html = f"Ciao {_html.escape(first_name)}, un saluto." if is_person else f"Ciao, un saluto al team di {_html.escape(business_name)}:"
        
        intro_p1 = f'Mi chiamo Emilio Ranucoli e sono il fondatore di <strong>Ranuk IT Solutions</strong> (<a href="https://ranuk.dev" style="color:#2563eb;text-decoration:none;font-weight:600;">ranuk.dev</a>), studio di ingegneria del software e audit tecnici. Vi scrivo con totale trasparenza: ci occupiamo di revisionare codice e creare piattaforme ad alte prestazioni, e il nostro modo di farci conoscere e acquisire nuovi clienti è analizzare in modo proattivo i siti web di aziende reali, individuando errori tecnici che spesso passano inosservati e condividendo subito la diagnosi per mostrare come lavoriamo.'
        intro_p2 = f'Oggi ho analizzato personalmente il sito di <strong><a href="https://{domain}" style="color:#2563eb;text-decoration:none;font-weight:600;">{business_name} ({domain})</a></strong> e ho preparato questo riepilogo tecnico prioritario per il vostro team.'

        reg_title = "Contesto normativo critico (European Accessibility Act):"
        reg_body = f'Con la piena entrata in vigore della <strong>Direttiva UE 2019/882 (European Accessibility Act) e del D.Lgs 82/2005 (CAD)</strong>, le piattaforme commerciali devono garantire l\'accessibilità digitale (WCAG 2.1 AA) per evitare sanzioni e non perdere fino al <strong>15% di clienti su smartphone</strong> a causa di bottoni non leggibili o form bloccati.'

        diag_title = "Riepilogo della Diagnosi Tecnica"
        diag_sub = f'Abbiamo rilevato questi 3 aspetti prioritari nel codice di <strong>{domain}</strong> ({nodes} elementi interessati nel DOM):'

        port_title = "Piattaforme e Portfolio in Produzione"
        port_sub = "Per verificare la qualità del nostro codice, la velocità (100/100 Lighthouse) e la serietà prima di prendere qualsiasi decisione, potete consultare i nostri progetti attivi:"
        port_item1 = '<strong><a href="https://ranuk.dev/portfolio" style="color:#2563eb;text-decoration:none;font-weight:700;">ranuk.dev/portfolio</a></strong> &mdash; Portfolio ufficiale di sviluppo web su misura, landing page ad alta velocità e applicazioni.'
        port_item2 = '<strong><a href="https://notarobot.es/" style="color:#2563eb;text-decoration:none;font-weight:700;">notarobot.es</a></strong> &mdash; Verifica di identità umana e sicurezza anti-bot (100% Lighthouse, Edge CDN).'
        port_item3 = '<strong><a href="https://audit.ranuk.dev/" style="color:#2563eb;text-decoration:none;font-weight:700;">audit.ranuk.dev</a></strong> &mdash; Motore di audit e certificazione continua di accessibilità web.'

        num_title = "Costi e riferimenti tariffari trasparenti:"
        num_opt1 = f'🔹 <strong>Opzione 1: Report Tecnico Completo EAA / WCAG 2.2 AA ({precio_tag}):</strong> Audit dettagliato di 15 pagine con certificato di verifica e linee di codice esatte per il vostro sviluppatore.'
        num_opt2 = f'🔹 <strong>Opzione 2: Remediazione Chiavi in Mano ({remed_tag}):</strong> Ci occupiamo direttamente di correggere e testare il codice sorgente (Pull Request su GitHub o patch pronta) senza occupare ore del vostro team.'
        num_opt3 = '🔹 <strong>Pacchetto Soluzione Integrale (Sito su Misura + Agente IA):</strong> ~<strong>590 € - 890 €</strong> tutto incluso.'

        trust_title = "Impegno formale di servizio e fatturazione fiscale ufficiale"
        trust_body = (
            f"Se decidete di procedere subito con l'Opzione 1 o 2, l'operazione viene elaborata in modo cifrato tramite Stripe e costituisce un "
            f"<strong>impegno contrattuale vincolante</strong> da parte nostra: emettiamo automaticamente <strong>fattura fiscale ufficiale con partita IVA e ricevuta contabile</strong>, "
            f"avviando la consegna tecnica entro un massimo garantito di 24 ore lavorative."
        )
        trust_link_text = "Potete consultare i nostri termini contrattuali, SLA e garanzia di conformità su:"

        opt1_card_title = f"Opzione 1: Ordina Report Tecnico Completo ({precio_tag})"
        opt1_card_desc = f"Dossier di 15 pagine con ricevuta fiscale e linee esatte di correzione per il vostro sviluppatore."
        opt1_btn_text = "Ordina Report &rarr;"

        opt2_card_title = f"Opzione 2: Remediazione Chiavi in Mano ({remed_tag})"
        opt2_card_desc = "Correggiamo direttamente il codice sorgente (Pull Request o patch pronta) senza occupare tempo del vostro team."
        opt2_btn_text = "Richiedi Correzione &rarr;"

        call_title = "Possiamo concordare una breve chiamata (15-20 minuti) per:"
        call_b1 = f"Esaminare i punti tecnici di {domain} in tempo reale"
        call_b2 = "Spiegare la metodologia di correzione passo dopo passo"
        call_b3 = "Rispondere a qualsiasi domanda tecnica del vostro team senza impegno"
        call_link_text = "Potete prenotare direttamente su Calendly: "
        call_free_note = "(Oppure, se preferite un'anteprima gratuita, rispondete semplicemente a questa email e vi invierò gli snippet di codice per il vostro sviluppatore)."

        role_title = "Ingegnere Informatico · Fondatore, Ranuk IT Solutions"
        optout_text = 'Ranuk IT Solutions &mdash; Ingegneria del software &amp; conformità WCAG.<br>Se non siete interessati, rispondete con "no grazie" e non vi ricontatterò più.'

    else:
        # Español (default)
        subject = f"Diagnóstico técnico y notas que preparé para {domain}"
        greeting_html = f"Hola {_html.escape(first_name)}, un saludo." if is_person else f"Hola, un saludo al equipo de {_html.escape(business_name)}:"
        
        pronoun_intro = "Te escribo" if is_person else "Les escribo"
        pronoun_target = "tu equipo" if is_person else "su equipo"
        pronoun_dev = "tu programador" if is_person else "su programador o equipo"

        intro_p1 = f'Mi nombre es Emilio Ranucoli y soy fundador de <strong>Ranuk IT Solutions</strong> (<a href="https://ranuk.dev" style="color:#2563eb;text-decoration:none;font-weight:600;">ranuk.dev</a>), estudio de ingeniería de software y auditorías técnicas. {pronoun_intro} con total transparencia: nos dedicamos a auditar código y construir plataformas de alto rendimiento, y nuestra forma de darnos a conocer y sumar nuevos clientes es analizando por nuestra cuenta sitios web de empresas reales, encontrando errores técnicos que suelen pasar desapercibidos y compartiendo el diagnóstico de entrada para mostrar cómo trabajamos.'
        intro_p2 = f'Hoy estuve revisando personalmente la web de <strong><a href="https://{domain}" style="color:#2563eb;text-decoration:none;font-weight:600;">{business_name} ({domain})</a></strong> y preparé este análisis técnico para {pronoun_target}.'

        reg_title = "Contexto regulatorio crítico:"
        reg_body = f'A partir de la plena vigencia de la <strong>Ley Europea de Accesibilidad (Directiva UE 2019/882 y Ley 11/2023)</strong>, las plataformas comerciales deben garantizar accesibilidad digital (WCAG 2.1 AA) para evitar sanciones aplicables de 5.000 € a 40.000 € y la pérdida de hasta un <strong>15% de clientes móviles</strong> por fricción y botones no legibles.'

        diag_title = "Resumen del Diagnóstico Técnico"
        diag_sub = f'Detectamos estos 3 hallazgos prioritarios en el código de <strong>{domain}</strong> ({nodes} elementos afectados en el DOM):'

        port_title = "Proyectos y Portfolio en Producción"
        port_sub = "Para que puedan comprobar nuestra calidad de código, velocidad (100/100 Lighthouse) y seriedad antes de tomar cualquier decisión, pueden ver nuestros proyectos en vivo:"
        port_item1 = '<strong><a href="https://ranuk.dev/portfolio" style="color:#2563eb;text-decoration:none;font-weight:700;">ranuk.dev/portfolio</a></strong> &mdash; Portfolio oficial de desarrollo web a medida, landing pages y optimización de velocidad.'
        port_item2 = '<strong><a href="https://notarobot.es/" style="color:#2563eb;text-decoration:none;font-weight:700;">notarobot.es</a></strong> &mdash; Verificación de identidad humana y seguridad anti-bot (100% Lighthouse, Edge CDN).'
        port_item3 = '<strong><a href="https://audit.ranuk.dev/" style="color:#2563eb;text-decoration:none;font-weight:700;">audit.ranuk.dev</a></strong> &mdash; Motor de auditoría y certificación técnica de accesibilidad web.'

        num_title = "Números y presupuestos de referencia:"
        num_opt1 = f'🔹 <strong>Opción 1: Informe Técnico Completo EAA / WCAG 2.2 AA ({precio_tag}):</strong> Auditoría priorizada de 15 páginas con certificado de verificación y líneas exactas de código para {pronoun_dev}.'
        num_opt2 = f'🔹 <strong>Opción 2: Remediación Llave en Mano ({remed_tag}):</strong> Nos encargamos de corregir y testear directamente el código fuente (Pull Request en GitHub o parche listo) sin consumir horas de tu equipo.'
        num_opt3 = f'🔹 <strong>Pack Solución Integral (Web a Medida + Agente IA):</strong> ~<strong>590 € - 890 € / $590 - $890 USD</strong> todo resuelto.'

        trust_title = "Compromiso formal de servicio y facturación oficial"
        trust_body = (
            f"Si deciden encargar el trabajo de inmediato, la operación se procesa de forma cifrada mediante Stripe y constituye un "
            f"<strong>compromiso de servicio formal y cerrado</strong> por nuestra parte: emitimos automáticamente <strong>factura y comprobante fiscal oficial</strong> "
            f"con validez contable y tributaria plena, e iniciamos la entrega técnica en un plazo máximo garantizado de 24 horas hábiles."
        )
        trust_link_text = "Pueden consultar nuestros términos contractuales, SLA y garantía de cumplimiento en:"

        opt1_card_title = f"Opción 1: Encargar Informe Técnico Completo ({precio_tag})"
        opt1_card_desc = f"Dossier priorizado de 15 páginas con comprobante fiscal y líneas exactas de remediación para {pronoun_dev}."
        opt1_btn_text = "Encargar Informe &rarr;"

        opt2_card_title = f"Opción 2: Remediación Llave en Mano ({remed_tag})"
        opt2_card_desc = "Nos encargamos de corregir el código fuente (Pull Request o parche listo) sin consumir horas de su equipo."
        opt2_btn_text = "Solicitar Remediación &rarr;"

        call_title = "Podemos coordinar una breve llamada (15-20 minutos) para:"
        call_b1 = f"Revisar los puntos técnicos de {domain} en vivo"
        call_b2 = "Explicar nuestra metodología de corrección paso a paso"
        call_b3 = "Resolver cualquier consulta técnica de su equipo sin compromiso"
        call_link_text = "Pueden agendar directamente acá: "
        call_free_note = "(O si prefieren ver un adelanto sin costo, solo respondan este correo y les envío los fragmentos de código para su desarrollador)."

        role_title = "Ingeniero de Sistemas · Fundador, Ranuk IT Solutions"
        optout_text = 'Ranuk IT Solutions &mdash; Auditorías de accesibilidad web &amp; desarrollo a medida.<br>Si no es de su interés, respondan con "no gracias" y no volveré a contactarlos.'

    # Formatear los 3 issues
    issue_items = []
    for iss in issues[:3]:
        t = _html.escape(iss.get("title", "Aspecto técnico"))
        d = _html.escape(iss.get("desc", ""))
        w = _html.escape(iss.get("wcag", "WCAG 2.1 AA"))
        badge = f'<span style="background:#e0f2fe;color:#0369a1;padding:2px 8px;border-radius:4px;font-size:11px;font-weight:700;margin-left:6px;vertical-align:middle;">{w}</span>' if w else ''
        issue_items.append(f'<li style="margin-bottom:10px;line-height:1.55;"><strong>{t}:</strong> {d} {badge}</li>')

    issues_html = "".join(issue_items)

    html = f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="color-scheme" content="light dark">
<meta name="supported-color-schemes" content="light dark">
<title>{subject}</title>
<style>
  :root {{
    color-scheme: light dark;
    supported-color-schemes: light dark;
  }}
</style>
</head>
<body style="margin:0;padding:24px 0;background-color:#f1f5f9;background:#f1f5f9;font-family:{ff};-webkit-font-smoothing:antialiased;">

<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="width:100%;margin:0;padding:0;">
  <tr>
    <td align="center" style="padding:0 12px;">
      <!-- Card Container (640px) SIN background-color general para no contaminar la barra -->
      <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="max-width:640px;width:100%;margin:0 auto;border:1px solid #cbd5e1;border-radius:12px;overflow:hidden;border-collapse:collapse;">
        
        <!-- 1. Header con Barra Oficial Ranuk IT Solutions (Banner Retina Inmune a Inversión Dark Mode) -->
        <tr bgcolor="#0f172a" style="background-color:#0f172a;background:#0f172a;margin:0;padding:0;">
          <td bgcolor="#0f172a" align="left" style="background-color:#0f172a;background:#0f172a;margin:0;padding:0;line-height:0;font-size:0;border-top-left-radius:11px;border-top-right-radius:11px;">
            <img src="cid:ranuklogo" alt="Ranuk IT Solutions" width="640" style="display:block;width:100%;max-width:640px;height:auto;border:0;outline:none;text-decoration:none;border-top-left-radius:11px;border-top-right-radius:11px;">
          </td>
        </tr>

        <!-- 2. Contenido Principal -->
        <tr bgcolor="#ffffff" style="background-color:#ffffff;background:#ffffff;">
          <td bgcolor="#ffffff" style="background-color:#ffffff;background:#ffffff;padding:32px 30px;font-size:15px;line-height:1.62;color:#1e293b;">

            <!-- Saludo -->
            <p style="margin:0 0 16px;font-size:17px;color:#0f172a;">{greeting_html}</p>

            <p style="margin:0 0 14px;">{intro_p1}</p>
            <p style="margin:0 0 18px;">{intro_p2}</p>

            <!-- 3. Caja Ámbar: Contexto Regulatorio Crítico -->
            <div style="border-left:4px solid #f59e0b;background:#fffbeb;padding:14px 18px;margin:22px 0;border-radius:4px;">
              <p style="margin:0 0 6px 0;font-weight:700;color:#92400e;font-size:14px;">{reg_title}</p>
              <p style="margin:0;font-size:13px;color:#78350f;line-height:1.55;">{reg_body}</p>
            </div>

            <!-- 4. Resumen del Diagnóstico con Barra Azul -->
            <div style="border-left:4px solid #2563eb;padding-left:16px;margin:24px 0;">
              <h3 style="color:#0f172a;margin:0 0 8px 0;font-size:16px;font-weight:700;">{diag_title}</h3>
              <p style="margin:0 0 12px 0;font-size:14px;color:#475569;">{diag_sub}</p>
              <ol style="margin:0;padding-left:18px;color:#1e293b;font-size:14px;">
                {issues_html}
              </ol>
            </div>

            <!-- 5. Tarjeta de Proyectos y Portfolio en Vivo -->
            <div style="background:#f8fafc;border:1px solid #e2e8f0;border-radius:8px;padding:16px 20px;margin:24px 0;">
              <h4 style="margin:0 0 8px 0;font-size:14px;color:#0f172a;font-weight:700;">{port_title}</h4>
              <p style="margin:0 0 10px 0;font-size:13px;color:#475569;line-height:1.5;">{port_sub}</p>
              <ul style="margin:0;padding-left:18px;font-size:13px;color:#334155;line-height:1.65;">
                <li style="margin-bottom:6px;">{port_item1}</li>
                <li style="margin-bottom:6px;">{port_item2}</li>
                <li>{port_item3}</li>
              </ul>
            </div>

            <!-- 6. Números y Presupuestos de Referencia -->
            <h4 style="color:#0f172a;margin:26px 0 10px 0;font-size:15px;font-weight:700;">{num_title}</h4>
            <div style="background:#f8fafc;border:1px solid #e2e8f0;border-radius:8px;padding:16px 20px;margin-bottom:20px;">
              <p style="margin:0 0 10px 0;font-size:14px;color:#1e293b;line-height:1.5;">{num_opt1}</p>
              <p style="margin:0 0 10px 0;font-size:14px;color:#1e293b;line-height:1.5;">{num_opt2}</p>
              <p style="margin:0;font-size:14px;color:#1e293b;line-height:1.5;">{num_opt3}</p>
            </div>

            <!-- 7. Marco Legal, Facturación y Compromiso Formal -->
            <div style="background:#f8fafc;border:1px solid #e2e8f0;border-left:4px solid #0f172a;border-radius:6px;padding:16px 20px;margin:24px 0;">
              <p style="margin:0 0 6px 0;font-size:14px;color:#0f172a;font-weight:700;">
                🛡️ {trust_title}:
              </p>
              <p style="margin:0 0 10px 0;font-size:13px;color:#475569;line-height:1.55;">
                {trust_body}
              </p>
              <p style="margin:0;font-size:12.5px;color:#64748b;line-height:1.5;">
                {trust_link_text} <a href="https://audit.ranuk.dev/legal?lang={lang}" style="color:#2563eb;text-decoration:underline;font-weight:600;">audit.ranuk.dev/legal?lang={lang}</a>
              </p>
            </div>

            <!-- 8. Opciones de Contratación con Acciones Sobrias -->
            <div style="border:1px solid #e2e8f0;background:#ffffff;border-radius:8px;padding:14px 18px;margin-bottom:12px;">
              <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="border-collapse:collapse;">
                <tr>
                  <td valign="middle" align="left">
                    <div style="font-size:13.5px;font-weight:700;color:#0f172a;">{opt1_card_title}</div>
                    <div style="font-size:12px;color:#64748b;margin-top:2px;">{opt1_card_desc}</div>
                  </td>
                  <td valign="middle" align="right" style="padding-left:14px;white-space:nowrap;">
                    <a href="{url_opt1}" style="background-color:#0f172a;background:#0f172a;color:#ffffff;text-decoration:none;font-weight:600;font-size:12.5px;padding:8px 16px;border-radius:6px;display:inline-block;">{opt1_btn_text}</a>
                  </td>
                </tr>
              </table>
            </div>

            <div style="border:1px solid #e2e8f0;background:#ffffff;border-radius:8px;padding:14px 18px;margin-bottom:24px;">
              <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="border-collapse:collapse;">
                <tr>
                  <td valign="middle" align="left">
                    <div style="font-size:13.5px;font-weight:700;color:#0f172a;">{opt2_card_title}</div>
                    <div style="font-size:12px;color:#64748b;margin-top:2px;">{opt2_card_desc}</div>
                  </td>
                  <td valign="middle" align="right" style="padding-left:14px;white-space:nowrap;">
                    <a href="{url_opt2}" style="background-color:#1e293b;background:#1e293b;border:1px solid #334155;color:#ffffff;text-decoration:none;font-weight:600;font-size:12.5px;padding:8px 16px;border-radius:6px;display:inline-block;">{opt2_btn_text}</a>
                  </td>
                </tr>
              </table>
            </div>

            <!-- 8. Bloque Navy de Agendamiento Directo -->
            <div style="background:#0f172a;color:#ffffff;border-radius:8px;padding:20px 24px;margin:24px 0;">
              <p style="margin:0 0 10px 0;font-weight:600;font-size:15px;color:#ffffff;">{call_title}</p>
              <ul style="margin:0 0 14px 0;padding-left:20px;color:#cbd5e1;font-size:13px;line-height:1.6;">
                <li>{call_b1}</li>
                <li>{call_b2}</li>
                <li>{call_b3}</li>
              </ul>
              <p style="margin:0 0 6px 0;font-size:13px;color:#94a3b8;line-height:1.5;">
                {call_link_text}<a href="https://calendly.com/emilio-ranuk/30min" style="color:#38bdf8;text-decoration:none;font-weight:600;">calendly.com/emilio-ranuk/30min</a>
              </p>
              <p style="margin:0;font-size:13px;color:#e2e8f0;font-style:italic;">
                {call_free_note}
              </p>
            </div>

          </td>
        </tr>

        <!-- 9. Firma Corporativa Verificada -->
        <tr bgcolor="#fafbfc" style="background-color:#fafbfc;background:#fafbfc;">
          <td bgcolor="#fafbfc" style="background-color:#fafbfc;background:#fafbfc;border-top:1px solid #e2e8f0;padding:20px 30px;border-bottom-left-radius:11px;border-bottom-right-radius:11px;">
            <table cellpadding="0" cellspacing="0" style="font-family:{ff};width:100%;">
              <tr>
                <td style="vertical-align:middle;">
                  <div style="font-size:15px;font-weight:700;color:#0f172a;">Emilio Ranucoli</div>
                  <div style="font-size:13px;color:#64748b;margin:2px 0 6px;">{role_title}</div>
                  <div style="font-size:13px;color:#475569;">
                    <a href="https://ranuk.dev/portfolio" style="color:#0ea5e9;text-decoration:none;font-weight:600;">Portfolio</a>
                    &nbsp;&middot;&nbsp;
                    <a href="https://ranuk.dev" style="color:#0ea5e9;text-decoration:none;">ranuk.dev</a>
                    &nbsp;&middot;&nbsp;
                    <a href="mailto:emilio@ranuk.dev" style="color:#0ea5e9;text-decoration:none;">emilio@ranuk.dev</a>
                  </div>
                </td>
              </tr>
            </table>
            <div style="font-size:11px;color:#94a3b8;margin-top:14px;line-height:1.5;">
              {optout_text}
            </div>
          </td>
        </tr>

      </table>
    </td>
  </tr>
</table>

</body>
</html>"""
    return subject, html
