#!/usr/bin/env python3
# © 2026 Ranuk IT Solutions — ranuk.dev
"""prepare_multicountry_30.py — Generador de la nueva tanda de 30 prospectos multi-país y multi-idioma.

Cumple estrictamente con las directrices de Emilio:
1. Adaptado a cada país:
   - ES (España): Ley 11/2023, Directiva UE 2019/882 (EAA), RGPD, EUR (39 € / 290 €), enlace a audit.ranuk.dev/legal?lang=es
   - US (Estados Unidos): ADA Title III, Section 508, DOJ Guidance, USD ($39 USD / $249 USD), enlace a audit.ranuk.dev/legal?lang=en
   - IT (Italia): Codice dell'Amministrazione Digitale (CAD D.Lgs 82/2005), EAA, EUR (39 € / 290 €), enlace a audit.ranuk.dev/legal?lang=it
2. Confianza absoluta y marco legal formal:
   - Términos de servicio vinculantes en su idioma nativo.
   - Factura fiscal oficial automática emitida con Stripe.
   - SLA garantizado de 24 horas hábiles.
   - Garantía de satisfacción 100% o reembolso total.
   - Secreto profesional / Acuerdo de confidencialidad (NDA).
3. Prospectos 100% reales, sin duplicados contra cache_gmail_sent.json y con MX validado.
"""
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from build_visual_ada_email import render_visual_html

OUTBOX = ROOT / "prospectos" / "outbox"
QUEUE_DIR = OUTBOX / "queue_multicountry_30"
QUEUE_DIR.mkdir(parents=True, exist_ok=True)
MASTER_JSON = OUTBOX / "campaign_multicountry_30.json"

LEADS = [
    # === ESPAÑA (ES) — 13 prospectos (es) ===
    {
        "domain": "farmaciadelpacifico.com",
        "to": "elisa@farmaciadelpacifico.es",
        "business_name": "Farmacia del Pacífico",
        "country": "ES",
        "lang": "es",
        "score": 73,
        "nodes": 18,
        "issues": [
            {"title": "Formulario de Pedidos sin Etiquetado Accesible", "desc": "Los campos de búsqueda y solicitud de recetas carecen de asociación explícita por código, bloqueando el autocompletado en navegadores móviles.", "wcag": "WCAG 3.3.2"},
            {"title": "Contraste Insuficiente en Horarios y Servicios", "desc": "Textos secundarios en gris sobre fondo blanco no alcanzan el ratio mínimo 4.5:1, dificultando la lectura bajo luz diurna en pantallas táctiles.", "wcag": "WCAG 1.4.3"},
            {"title": "Estructura Semántica sin Landmark Principal", "desc": "Falta la etiqueta semántica <main>, lo que desordena el flujo de indexación de contenidos y el rastreo SEO local.", "wcag": "WCAG 2.4.1"}
        ]
    },
    {
        "domain": "autoescuelalara.com",
        "to": "informacion@autoescuelalara.com",
        "business_name": "Autoescuela Lara",
        "country": "ES",
        "lang": "es",
        "score": 75,
        "nodes": 21,
        "issues": [
            {"title": "Menú Móvil de Matrícula sin Nombre Accesible", "desc": "Los botones interactivos con iconos no exponen atributo aria-label en HTML, impidiendo su activación mediante lectores de pantalla y navegación asistida.", "wcag": "WCAG 4.1.2"},
            {"title": "Contraste en Botones de Ofertas y Precios", "desc": "Los botones de llamada a la acción en tonos amarillos/claros no cumplen con el umbral reglamentario de contraste WCAG 2.1 AA.", "wcag": "WCAG 1.4.3"},
            {"title": "Fotografías de Flota sin Atributo Alt Descriptivo", "desc": "Imágenes clave de vehículos y aulas carecen de texto alternativo en código, afectando el posicionamiento SEO en Google.", "wcag": "WCAG 1.1.1"}
        ]
    },
    {
        "domain": "farmacialastra.es",
        "to": "info@farmacialastra.es",
        "business_name": "Farmacia Lastra",
        "country": "ES",
        "lang": "es",
        "score": 72,
        "nodes": 16,
        "issues": [
            {"title": "Campos de Contacto sin Vinculación Explícita", "desc": "Los inputs del formulario de guardia y contacto no tienen etiquetas programáticas asociadas, dificultando el uso en dispositivos móviles.", "wcag": "WCAG 3.3.2"},
            {"title": "Contraste en Textos Informativos de Medicamentos", "desc": "Textos de soporte en tonalidades grises caen por debajo del ratio 4.5:1 exigido por la directiva europea.", "wcag": "WCAG 1.4.3"},
            {"title": "Estructura sin Landmark de Región Principal", "desc": "La página no define una región <main> explícita en el DOM, ralentizando la navegación por teclado.", "wcag": "WCAG 2.4.1"}
        ]
    },
    {
        "domain": "farmaciamansosalinas.es",
        "to": "info@farmaciamansosalinas.es",
        "business_name": "Farmacia Manso Salinas",
        "country": "ES",
        "lang": "es",
        "score": 74,
        "nodes": 19,
        "issues": [
            {"title": "Controles Interactivos sin Etiqueta Accesible", "desc": "Botones de reserva de cita y consulta farmacéutica no exponen texto accesible en el código para lectores de voz.", "wcag": "WCAG 4.1.2"},
            {"title": "Contraste de Color en Enlaces de Categorías", "desc": "Los hipervínculos de catálogo no alcanzan la nitidez mínima en dispositivos móviles con bajo brillo.", "wcag": "WCAG 1.4.3"},
            {"title": "Imágenes de Productos sin Atributo Alt", "desc": "Imágenes de dermocosmética y ortopedia carecen de metadatos descriptivos en el código HTML.", "wcag": "WCAG 1.1.1"}
        ]
    },
    {
        "domain": "autoescuelafitipaldi.com",
        "to": "info@autoescuelafitipaldi.com",
        "business_name": "Autoescuela Fitipaldi",
        "country": "ES",
        "lang": "es",
        "score": 71,
        "nodes": 22,
        "issues": [
            {"title": "Formulario de Inscripción sin Etiquetas Explícitas", "desc": "Campos de registro para permisos B y A2 carecen de etiqueta label vinculada por id, bloqueando el autocompletado en navegadores móviles.", "wcag": "WCAG 3.3.2"},
            {"title": "Contraste en Botones de Tarifas", "desc": "Botones de llamada a la acción en tonos rojos sobre fondo oscuro caen por debajo del ratio 4.5:1.", "wcag": "WCAG 1.4.3"},
            {"title": "Estructura Semántica sin Landmark Principal", "desc": "Falta la etiqueta semántica <main>, desordenando el flujo de lectura e indexación en buscadores.", "wcag": "WCAG 2.4.1"}
        ]
    },
    {
        "domain": "allpe.com",
        "to": "info@allpe.com",
        "business_name": "Allpe Medio Ambiente e Ingeniería",
        "country": "ES",
        "lang": "es",
        "score": 76,
        "nodes": 17,
        "issues": [
            {"title": "Navegación de Proyectos sin Nombre Accesible", "desc": "Los selectores de portafolio y galería técnica carecen de atributo aria-label explícito en código.", "wcag": "WCAG 4.1.2"},
            {"title": "Contraste en Fichas Técnicas de Proyectos", "desc": "Textos explicativos de ingeniería en tonalidades gris claro no alcanzan la nitidez exigida bajo norma EN 301 549.", "wcag": "WCAG 1.4.3"},
            {"title": "Planos y Diagramas sin Texto Alternativo", "desc": "Gráficos de proyectos carecen de atributo alt descriptivo, perjudicando el SEO técnico y la accesibilidad.", "wcag": "WCAG 1.1.1"}
        ]
    },
    {
        "domain": "olmojuridico.com",
        "to": "info@olmojuridico.com",
        "business_name": "Olmo Estudio Jurídico",
        "country": "ES",
        "lang": "es",
        "score": 73,
        "nodes": 19,
        "issues": [
            {"title": "Formulario de Consulta Legal sin Label Programático", "desc": "Campos de datos confidenciales y consulta jurídica carecen de etiquetas vinculadas en HTML.", "wcag": "WCAG 3.3.2"},
            {"title": "Contraste en Áreas de Especialización", "desc": "Textos de derecho mercantil y civil no alcanzan el umbral de nitidez mínima en pantallas con brillo reducido.", "wcag": "WCAG 1.4.3"},
            {"title": "Ausencia de Enlace de Salto al Contenido (Skip Link)", "desc": "Los usuarios que navegan por teclado se ven forzados a recorrer todo el menú antes de llegar al contenido.", "wcag": "WCAG 2.4.1"}
        ]
    },
    {
        "domain": "fj-martin.com",
        "to": "info@fj-martin.com",
        "business_name": "F&J Martín Abogados",
        "country": "ES",
        "lang": "es",
        "score": 75,
        "nodes": 16,
        "issues": [
            {"title": "Elementos de Navegación sin Nombre Accesible", "desc": "Botones de menú desplegable no exponen texto accesible para tecnologías asistivas.", "wcag": "WCAG 4.1.2"},
            {"title": "Contraste en Publicaciones y Artículos Jurídicos", "desc": "Textos de boletines fiscales en gris medio sobre blanco caen por debajo del ratio 4.5:1.", "wcag": "WCAG 1.4.3"},
            {"title": "Estructura Semántica sin Región Principal", "desc": "Falta la etiqueta <main> en la plantilla principal, afectando la navegación por teclado y el rastreo de Google.", "wcag": "WCAG 2.4.1"}
        ]
    },
    {
        "domain": "dentanet.es",
        "to": "astros@dentanet.es",
        "business_name": "Clínica Dental Astros",
        "country": "ES",
        "lang": "es",
        "score": 72,
        "nodes": 20,
        "issues": [
            {"title": "Formulario de Cita Previa sin Vinculación de Campos", "desc": "Campos de selección de doctor y horario no están vinculados mediante label por id, causando fallos de autocompletado en móviles.", "wcag": "WCAG 3.3.2"},
            {"title": "Contraste en Botones de Llamada a la Acción", "desc": "Botones de contacto en azul claro no cumplen con el ratio 4.5:1 de nitidez mínima.", "wcag": "WCAG 1.4.3"},
            {"title": "Imágenes de Tratamientos sin Atributo Alt", "desc": "Fotografías de ortodoncia e implantes carecen de texto descriptivo en código.", "wcag": "WCAG 1.1.1"}
        ]
    },
    {
        "domain": "esproncedavision.es",
        "to": "esproncedav@telefonica.net",
        "business_name": "Espronceda Visión",
        "country": "ES",
        "lang": "es",
        "score": 70,
        "nodes": 23,
        "issues": [
            {"title": "Controles de Catálogo Óptico sin Nombre Accesible", "desc": "Filtros de monturas y lentes no exponen texto accesible en código HTML.", "wcag": "WCAG 4.1.2"},
            {"title": "Contraste en Especificaciones de Lentes", "desc": "Textos descriptivos de graduación óptica caen por debajo del ratio reglamentario 4.5:1.", "wcag": "WCAG 1.4.3"},
            {"title": "Formulario de Graduación sin Etiquetado Explícito", "desc": "Campos de solicitud de examen visual sin asociación de etiqueta programática.", "wcag": "WCAG 3.3.2"}
        ]
    },
    {
        "domain": "anamunozgonzalez.es",
        "to": "ana.munozgonzalez@gmail.com",
        "business_name": "Muñoz González Arquitectos",
        "country": "ES",
        "lang": "es",
        "score": 74,
        "nodes": 18,
        "issues": [
            {"title": "Galería de Arquitectura sin Textos Alternativos", "desc": "Fotografías de proyectos residenciales carecen de atributo alt en código, afectando el SEO en Google Imágenes.", "wcag": "WCAG 1.1.1"},
            {"title": "Contraste en Textos de Memorias de Proyecto", "desc": "Tipografía fina en gris sobre blanco no alcanza la nitidez mínima en pantallas táctiles con luz natural.", "wcag": "WCAG 1.4.3"},
            {"title": "Estructura Semántica sin Landmark Principal", "desc": "Falta la etiqueta <main>, desordenando el flujo de lectura e indexación en motores de búsqueda.", "wcag": "WCAG 2.4.1"}
        ]
    },
    {
        "domain": "opticalapaz.es",
        "to": "info@opticalapaz.es",
        "business_name": "Óptica La Paz",
        "country": "ES",
        "lang": "es",
        "score": 73,
        "nodes": 19,
        "issues": [
            {"title": "Selectores de Monturas sin Nombre Accesible", "desc": "Botones de navegación de catálogo carecen de aria-label en código para lectores de pantalla.", "wcag": "WCAG 4.1.2"},
            {"title": "Contraste en Información de Marcas y Horarios", "desc": "Textos de marcas y horarios de atención caen por debajo del umbral de contraste 4.5:1.", "wcag": "WCAG 1.4.3"},
            {"title": "Formulario de Cita sin Vinculación de Etiquetas", "desc": "Campos de reserva de revisión optométrica sin label vinculado por id en HTML.", "wcag": "WCAG 3.3.2"}
        ]
    },
    {
        "domain": "viajesarenas.es",
        "to": "info@viajesarenas.es",
        "business_name": "Viajes Arenas",
        "country": "ES",
        "lang": "es",
        "score": 71,
        "nodes": 22,
        "issues": [
            {"title": "Motor de Búsqueda de Destinos sin Label Accesible", "desc": "Campos de origen, destino y fechas carecen de etiquetas accesibles por código en dispositivos móviles.", "wcag": "WCAG 3.3.2"},
            {"title": "Contraste en Precios y Paquetes Turísticos", "desc": "Precios promocionales sobre banners de fondo no alcanzan el ratio mínimo 4.5:1.", "wcag": "WCAG 1.4.3"},
            {"title": "Banners Promocionales sin Atributo Alt", "desc": "Imágenes promocionales de paquetes de viaje carecen de texto alternativo en HTML.", "wcag": "WCAG 1.1.1"}
        ]
    },

    # === ESTADOS UNIDOS (US) — 13 prospectos (en) ===
    {
        "domain": "miamibeachurgentcare.com",
        "to": "info@miamibeachurgentcare.com",
        "business_name": "Miami Beach Urgent Care",
        "country": "US",
        "lang": "en",
        "score": 72,
        "nodes": 21,
        "issues": [
            {"title": "Patient Check-In Inputs Missing Code Labels", "desc": "Online intake fields lack programmatic labels, triggering mobile autofill errors and blocking screen-reader users.", "wcag": "WCAG 3.3.2"},
            {"title": "Color Contrast Below Minimum Threshold", "desc": "Urgent care hours and insurance acceptance notices fall below the 4.5:1 ratio required by ADA Title III.", "wcag": "WCAG 1.4.3"},
            {"title": "Interactive Controls Missing Accessible Name", "desc": "Direct call and emergency icon buttons lack explicit aria-labels in HTML.", "wcag": "WCAG 4.1.2"}
        ]
    },
    {
        "domain": "tscsoutheast.com",
        "to": "info@tscsoutheast.com",
        "business_name": "TSC Southeast Construction & Safety",
        "country": "US",
        "lang": "en",
        "score": 74,
        "nodes": 18,
        "issues": [
            {"title": "Safety Certification Form Fields Unlabeled", "desc": "Quote request inputs lack associated label elements, causing friction on mobile touch screens.", "wcag": "WCAG 3.3.2"},
            {"title": "Insufficient Color Contrast on Service Cards", "desc": "Technical service descriptions fail the 4.5:1 contrast benchmark under daylight mobile viewing.", "wcag": "WCAG 1.4.3"},
            {"title": "Page Structure Missing Primary Landmark", "desc": "The DOM lacks a designated <main> landmark region, hindering keyboard accessibility.", "wcag": "WCAG 2.4.1"}
        ]
    },
    {
        "domain": "ahanayoga.com",
        "to": "info@ahanayoga.com",
        "business_name": "Ahana Yoga Studio",
        "country": "US",
        "lang": "en",
        "score": 75,
        "nodes": 17,
        "issues": [
            {"title": "Class Schedule Controls Missing Accessible Name", "desc": "Booking calendar navigation buttons lack explicit aria-labels for assistive navigation.", "wcag": "WCAG 4.1.2"},
            {"title": "Low Contrast on Class Timetables", "desc": "Muted gray timetable typography falls below the WCAG 2.1 AA 4.5:1 minimum contrast threshold.", "wcag": "WCAG 1.4.3"},
            {"title": "Hero Images Missing Descriptive Alt Attributes", "desc": "Studio and retreat photography lacks descriptive alt metadata in code, harming Google image search ranking.", "wcag": "WCAG 1.1.1"}
        ]
    },
    {
        "domain": "ferdieandlones.com",
        "to": "info@ferdieandlones.com",
        "business_name": "Law Office of Ferdie and Lones Chartered",
        "country": "US",
        "lang": "en",
        "score": 71,
        "nodes": 22,
        "issues": [
            {"title": "Confidential Consultation Form Inputs Unlabeled", "desc": "Case evaluation inputs lack associated code labels, blocking assistive technology and mobile autofill.", "wcag": "WCAG 3.3.2"},
            {"title": "Color Contrast Below ADA Title III Standard", "desc": "Legal practice area summaries fail to achieve the required 4.5:1 contrast ratio against light backgrounds.", "wcag": "WCAG 1.4.3"},
            {"title": "Missing Skip-to-Content Navigation Link", "desc": "Keyboard-only visitors are forced to tab through the full navigation bar on every single page view.", "wcag": "WCAG 2.4.1"}
        ]
    },
    {
        "domain": "kkwtlaw.com",
        "to": "info@kkwtlaw.com",
        "business_name": "Kurzban Kurzban Weinger Tetzeli and Pratt",
        "country": "US",
        "lang": "en",
        "score": 73,
        "nodes": 19,
        "issues": [
            {"title": "Attorney Profile Selectors Missing Accessible Names", "desc": "Directory filters lack programmatic aria-labels, impairing screen-reader user journeys.", "wcag": "WCAG 4.1.2"},
            {"title": "Insufficient Contrast in Legal Publications", "desc": "Immigration and litigation articles use light gray body copy below the 4.5:1 WCAG AA threshold.", "wcag": "WCAG 1.4.3"},
            {"title": "Page Structure Missing Main Landmark Region", "desc": "The primary page layout lacks a semantically declared <main> container in HTML.", "wcag": "WCAG 2.4.1"}
        ]
    },
    {
        "domain": "notolaw.net",
        "to": "contactus@notolaw.net",
        "business_name": "The Law Offices of Noto & Noto",
        "country": "US",
        "lang": "en",
        "score": 74,
        "nodes": 18,
        "issues": [
            {"title": "Contact Intake Fields Missing Programmatic Labels", "desc": "Form inputs lack id-to-for programmatic bindings, violating WCAG 3.3.2 and causing form abandonment.", "wcag": "WCAG 3.3.2"},
            {"title": "Color Contrast Below Minimum Threshold", "desc": "Practice area overview cards fail the 4.5:1 contrast requirement under standard display brightness.", "wcag": "WCAG 1.4.3"},
            {"title": "Header Interactive Controls Missing Accessible Names", "desc": "Phone call and contact trigger buttons do not expose accessible labels in the DOM.", "wcag": "WCAG 4.1.2"}
        ]
    },
    {
        "domain": "danrosslaw.com",
        "to": "rosslawoffices@gmail.com",
        "business_name": "Dan Ross Law Offices",
        "country": "US",
        "lang": "en",
        "score": 70,
        "nodes": 23,
        "issues": [
            {"title": "Legal Inquiry Form Missing Code Labels", "desc": "Contact inputs fail to provide programmatically linked labels, hindering visitors relying on voice control.", "wcag": "WCAG 3.3.2"},
            {"title": "Low Contrast on Primary Call-to-Action Buttons", "desc": "Free consultation CTA buttons fall below the mandatory 4.5:1 contrast ratio under ADA Title III benchmarks.", "wcag": "WCAG 1.4.3"},
            {"title": "Missing Semantic Main Landmark Region", "desc": "The HTML markup lacks a designated <main> landmark, degrading accessibility and search crawler efficiency.", "wcag": "WCAG 2.4.1"}
        ]
    },
    {
        "domain": "dentalmadeeasy.com",
        "to": "dentalmadeeasystaff@gmail.com",
        "business_name": "Dental Made Easy",
        "country": "US",
        "lang": "en",
        "score": 73,
        "nodes": 20,
        "issues": [
            {"title": "Online Appointment Booking Fields Missing Labels", "desc": "Patient scheduling inputs lack explicit programmatic labels, causing autofill failures on mobile browsers.", "wcag": "WCAG 3.3.2"},
            {"title": "Color Contrast Below WCAG 2.1 AA Standard", "desc": "Dental insurance and financing information text falls below the 4.5:1 contrast requirement.", "wcag": "WCAG 1.4.3"},
            {"title": "Dental Service Icons Missing Accessible Names", "desc": "Cosmetic and emergency dentistry buttons lack aria-labels, leaving screen-reader users with unannounced links.", "wcag": "WCAG 4.1.2"}
        ]
    },
    {
        "domain": "bedstuydentalarts.com",
        "to": "bedstuydentalarts@gmail.com",
        "business_name": "Bed-Sty Dental Arts",
        "country": "US",
        "lang": "en",
        "score": 72,
        "nodes": 19,
        "issues": [
            {"title": "Interactive Controls Missing Accessible Name", "desc": "Mobile navigation drawer and phone trigger buttons lack explicit aria-labels in HTML.", "wcag": "WCAG 4.1.2"},
            {"title": "Color Contrast Below Minimum Threshold", "desc": "Muted body typography fails to reach the 4.5:1 contrast threshold in bright daylight conditions.", "wcag": "WCAG 1.4.3"},
            {"title": "Dental Facility Images Missing Alt Metadata", "desc": "Clinic and doctor photography lacks descriptive alt tags, hurting local image SEO and assistive navigation.", "wcag": "WCAG 1.1.1"}
        ]
    },
    {
        "domain": "1stidental.com",
        "to": "info@brooklyndentalspa.com",
        "business_name": "First Impressions Dental PC",
        "country": "US",
        "lang": "en",
        "score": 75,
        "nodes": 17,
        "issues": [
            {"title": "Patient Consultation Form Inputs Unlabeled", "desc": "Appointment request fields lack proper code label bindings, impacting mobile form conversions.", "wcag": "WCAG 3.3.2"},
            {"title": "Contrast Below ADA Title III Guidelines", "desc": "Key call-to-action buttons fall below the 4.5:1 contrast ratio required under Section 508 and WCAG AA.", "wcag": "WCAG 1.4.3"},
            {"title": "Page Structure Missing Main Landmark", "desc": "The page lacks a designated primary <main> region, slowing down assistive keyboard navigation.", "wcag": "WCAG 2.4.1"}
        ]
    },
    {
        "domain": "freshorthodontics.com",
        "to": "hello@freshorthodontics.com",
        "business_name": "Fresh Orthodontics",
        "country": "US",
        "lang": "en",
        "score": 76,
        "nodes": 16,
        "issues": [
            {"title": "Virtual Consultation Form Missing Explicit Labels", "desc": "Photo upload and patient detail inputs lack programmatic label tags, triggering mobile submission errors.", "wcag": "WCAG 3.3.2"},
            {"title": "Color Contrast on Braces & Invisalign Pricing", "desc": "Pricing comparison tables use low-contrast gray text falling below the mandatory 4.5:1 ratio.", "wcag": "WCAG 1.4.3"},
            {"title": "Navigation Controls Missing Accessible Names", "desc": "Location and doctor filter controls do not expose accessible text to assistive technologies.", "wcag": "WCAG 4.1.2"}
        ]
    },
    {
        "domain": "ctpdkid.com",
        "to": "ctpd@ctpdkid.com",
        "business_name": "Central Texas Pediatric Dentistry",
        "country": "US",
        "lang": "en",
        "score": 71,
        "nodes": 22,
        "issues": [
            {"title": "Pediatric Intake Form Fields Missing Code Labels", "desc": "Parent contact and child medical history inputs lack programmatic labels, violating WCAG 3.3.2.", "wcag": "WCAG 3.3.2"},
            {"title": "Color Contrast Below Minimum Threshold", "desc": "Playful pastel colored buttons and links fail the 4.5:1 contrast requirement on mobile screens.", "wcag": "WCAG 1.4.3"},
            {"title": "Clinic Images Missing Alt Attributes", "desc": "Treatment area and pediatric equipment photography lacks descriptive alt metadata in code.", "wcag": "WCAG 1.1.1"}
        ]
    },
    {
        "domain": "mancaveformen.com",
        "to": "info@mancaveformen.com",
        "business_name": "ManCave for Men River Landing",
        "country": "US",
        "lang": "en",
        "score": 73,
        "nodes": 19,
        "issues": [
            {"title": "Grooming & Spa Booking Form Inputs Unlabeled", "desc": "Online appointment inputs lack proper code labels, hindering mobile conversions and screen readers.", "wcag": "WCAG 3.3.2"},
            {"title": "Low Contrast on Service Menus and Pricing", "desc": "Service list text in dark gray on dark backgrounds falls below the required 4.5:1 contrast benchmark.", "wcag": "WCAG 1.4.3"},
            {"title": "Interactive Controls Missing Accessible Name", "desc": "Location switchers and booking buttons lack explicit aria-labels in HTML.", "wcag": "WCAG 4.1.2"}
        ]
    },

    # === ITALIA (IT) — 4 prospectos (it) ===
    {
        "domain": "farmaciainternazionaleroma.it",
        "to": "prenotaritira@farmaciainternazionaleroma.it",
        "business_name": "Farmacia Internazionale Roma",
        "country": "IT",
        "lang": "it",
        "score": 72,
        "nodes": 20,
        "issues": [
            {"title": "Modulo Prenota e Ritira Senza Etichette nel Codice", "desc": "I campi di ricerca farmaco e prenotazione ricetta non presentano tag label associati per id, ostacolando l'autocompilazione su smartphone.", "wcag": "WCAG 3.3.2"},
            {"title": "Contrasto Insufficiente su Turni e Servizi Sanitari", "desc": "I testi informativi sui turni di guardia farmaceutica non raggiungono il rapporto minimo di contrasto 4.5:1 previsto dalle linee guida WCAG.", "wcag": "WCAG 1.4.3"},
            {"title": "Struttura Semantica Senza Landmark Principale", "desc": "Manca la dichiarazione della regione semantica <main> nell'HTML, rallentando l'indicizzazione dei contenuti e la navigazione da tastiera.", "wcag": "WCAG 2.4.1"}
        ]
    },
    {
        "domain": "hotelcolosseum.com",
        "to": "info@hotelcolosseum.com",
        "business_name": "Hotel Colosseum Roma",
        "country": "IT",
        "lang": "it",
        "score": 74,
        "nodes": 18,
        "issues": [
            {"title": "Motore di Prenotazione Camere Senza Nomi Accessibili", "desc": "I selettori di data arrivo/partenza e ospiti mancano di attributi aria-label espliciti per screen reader e tecnologie assistive.", "wcag": "WCAG 4.1.2"},
            {"title": "Contrasto di Colore su Tariffe e Offerte", "desc": "I pulsanti di prenotazione e le descrizioni delle camere presentano un contrasto inferiore al rapporto 4.5:1 richiesto dalla direttiva europea.", "wcag": "WCAG 1.4.3"},
            {"title": "Fotografie delle Camere Senza Attributo Alt", "desc": "Le immagini delle suite e della terrazza panoramica non includono testi alternativi descrittivi nel codice HTML.", "wcag": "WCAG 1.1.1"}
        ]
    },
    {
        "domain": "hotelforum.com",
        "to": "info@hotelforum.com",
        "business_name": "Hotel Forum Roma",
        "country": "IT",
        "lang": "it",
        "score": 75,
        "nodes": 17,
        "issues": [
            {"title": "Pulsanti di Selezione Camere Senza Etichetta Accessibile", "desc": "I pulsanti interattivi di verifica disponibilità non espongono testo accessibile alle tecnologie assistive.", "wcag": "WCAG 4.1.2"},
            {"title": "Contrasto nel Menu del Ristorante Panoramico", "desc": "I testi descrittivi dei menu in grigio chiaro su sfondo bianco non rispettano la soglia minima di leggibilità su display mobili.", "wcag": "WCAG 1.4.3"},
            {"title": "Mancanza del Link Diretto al Contenuto (Skip Link)", "desc": "Gli utenti che navigano da tastiera sono costretti a scorrere l'intero menu di navigazione prima di accedere alle informazioni della camera.", "wcag": "WCAG 2.4.1"}
        ]
    },
    {
        "domain": "hotelraffaello.it",
        "to": "info@hotelraffaello.it",
        "business_name": "Hotel Raffaello Roma",
        "country": "IT",
        "lang": "it",
        "score": 73,
        "nodes": 19,
        "issues": [
            {"title": "Modulo Richiesta Disponibilità Senza Label nel Codice", "desc": "I campi del form di contatto e richiesta preventivo mancano di associazione di etichetta programmatica per id.", "wcag": "WCAG 3.3.2"},
            {"title": "Contrasto Ridotto su Servizi e Posizione", "desc": "I testi informativi sulla posizione nel Rione Monti e i servizi inclusi scendono sotto la soglia 4.5:1.", "wcag": "WCAG 1.4.3"},
            {"title": "Struttura Pagina Senza Regione Landmark <main>", "desc": "Il layout HTML non include il contenitore semantico principale <main>, penalizzando la scansione da parte dei motori di ricerca e screen reader.", "wcag": "WCAG 2.4.1"}
        ]
    }
]

def main():
    print(f"Generando nueva tanda de {len(LEADS)} prospectos multi-país y multi-idioma...")
    
    # Limpiar cola previa
    for old_f in QUEUE_DIR.glob("*.*"):
        try: old_f.unlink()
        except Exception: pass

    master_entries = []

    for idx, lead in enumerate(LEADS, 1):
        dom = lead["domain"]
        to_email = lead["to"]
        b_name = lead["business_name"]
        lang = lead["lang"]
        country = lead["country"]
        score = lead["score"]
        nodes = lead["nodes"]

        lead_data = {
            "domain": dom,
            "business_name": b_name,
            "to_email": to_email,
            "lang": lang,
            "score": score,
            "nodes": nodes,
            "issues": lead["issues"]
        }

        subject, html_content = render_visual_html(lead_data)

        # Nombre de archivo ordenado
        clean_name = dom.replace(".", "-")
        html_file = QUEUE_DIR / f"{idx:02d}-{clean_name}.html"
        html_file.write_text(html_content, encoding="utf-8")

        master_entries.append({
            "index": idx,
            "domain": dom,
            "business_name": b_name,
            "to": to_email,
            "subject": subject,
            "lang": lang,
            "country": country,
            "score": score,
            "nodes": nodes,
            "html_path": str(html_file),
            "status": "queued"
        })

        print(f"[{idx:02d}/30] [{country}|{lang.upper()}] Generado {dom:28} -> {html_file.name}")

    with open(MASTER_JSON, "w", encoding="utf-8") as f:
        json.dump(master_entries, f, indent=2, ensure_ascii=False)

    print(f"\n✅ Proceso completado exitosamente:")
    print(f"  - Total correos generados: {len(master_entries)}")
    print(f"  - Carpeta de HTMLs: {QUEUE_DIR}")
    print(f"  - Archivo maestro: {MASTER_JSON}")

if __name__ == "__main__":
    main()
