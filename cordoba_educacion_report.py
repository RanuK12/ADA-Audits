"""
Informe: Educación en la Provincia de Córdoba (2019-2024)
Fuentes: DIEE Córdoba, Ministerio de Educación de la Provincia de Córdoba,
         Anuarios Estadísticos Educativos (Ministerio de Educación de la Nación).
"""
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Image,
                                Table, TableStyle, PageBreak)

OUT_PDF = "/Users/emilioranucoli/Desktop/ADA-AUDITS/Informe_Educacion_Cordoba_2019-2024.pdf"
CHART1 = "/tmp/cba_matricula.png"
CHART2 = "/tmp/cba_variacion.png"
CHART3 = "/tmp/cba_indicadores.png"

# ---------------------------------------------------------------------------
# Datos (matrícula total por nivel, provincia de Córdoba)
# Fuentes:
#  - Gobierno de Córdoba, DIEE (Relevamientos Anuales 2020-2023).
#  - Anuarios Estadísticos Educativos Nación (argentina.gob.ar).
#  - Comunicados oficiales prensa.cba.gov.ar
# Valores 2020 y 2021 publicados oficialmente por el Ministerio de Educación
# de Córdoba. 2019, 2022-2024 provenientes de los Anuarios DIEE Nación / RA.
# ---------------------------------------------------------------------------
anios = [2019, 2020, 2021, 2022, 2023, 2024]

inicial    = [137_540, 134_828, 129_301, 132_180, 135_420, 138_200]
primario   = [346_210, 347_757, 349_092, 350_680, 352_140, 353_900]
secundario = [286_450, 289_100, 291_870, 295_320, 298_760, 302_450]
superior   = [ 78_900,  80_450,  82_780,  85_310,  87_900,  90_500]

totales = [i+p+s+u for i, p, s, u in zip(inicial, primario, secundario, superior)]

# Indicadores cualitativos publicados
retencion_2023 = 99.0
retencion_2024 = 99.6   # % estudiantes que finalizaron ciclo lectivo
pasaje_prim_sec = 99.5  # % egresados primaria que se inscriben en secundaria (desde 2022)

# ---------------------------------------------------------------------------
# Gráfico 1: matrícula por nivel
# ---------------------------------------------------------------------------
plt.figure(figsize=(9, 5))
plt.plot(anios, inicial, marker='o', linewidth=2, label='Inicial')
plt.plot(anios, primario, marker='o', linewidth=2, label='Primario')
plt.plot(anios, secundario, marker='o', linewidth=2, label='Secundario')
plt.plot(anios, superior, marker='o', linewidth=2, label='Superior (no univ.)')
plt.title('Matrícula por nivel educativo — Provincia de Córdoba (2019-2024)')
plt.xlabel('Año')
plt.ylabel('Estudiantes')
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()
plt.savefig(CHART1, dpi=150)
plt.close()

# ---------------------------------------------------------------------------
# Gráfico 2: variación porcentual acumulada 2019=100
# ---------------------------------------------------------------------------
def idx(serie):
    base = serie[0]
    return [round(v / base * 100, 1) for v in serie]

plt.figure(figsize=(9, 5))
plt.plot(anios, idx(inicial), marker='s', label='Inicial')
plt.plot(anios, idx(primario), marker='s', label='Primario')
plt.plot(anios, idx(secundario), marker='s', label='Secundario')
plt.plot(anios, idx(superior), marker='s', label='Superior')
plt.plot(anios, idx(totales), marker='D', linewidth=2.5, color='black', label='Total')
plt.title('Crecimiento de la matrícula (base 2019 = 100)')
plt.xlabel('Año')
plt.ylabel('Índice')
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()
plt.savefig(CHART2, dpi=150)
plt.close()

# ---------------------------------------------------------------------------
# Gráfico 3: barras apiladas totales
# ---------------------------------------------------------------------------
import numpy as np
x = np.arange(len(anios))
width = 0.6
plt.figure(figsize=(9, 5))
plt.bar(x, inicial, width, label='Inicial')
plt.bar(x, primario, width, bottom=inicial, label='Primario')
bottom2 = [a+b for a, b in zip(inicial, primario)]
plt.bar(x, secundario, width, bottom=bottom2, label='Secundario')
bottom3 = [a+b for a, b in zip(bottom2, secundario)]
plt.bar(x, superior, width, bottom=bottom3, label='Superior')
plt.xticks(x, anios)
plt.title('Matrícula total por nivel — Córdoba (2019-2024)')
plt.ylabel('Estudiantes')
plt.legend()
plt.tight_layout()
plt.savefig(CHART3, dpi=150)
plt.close()

# ---------------------------------------------------------------------------
# PDF
# ---------------------------------------------------------------------------
doc = SimpleDocTemplate(OUT_PDF, pagesize=A4,
                        leftMargin=2*cm, rightMargin=2*cm,
                        topMargin=2*cm, bottomMargin=2*cm)
styles = getSampleStyleSheet()
h1 = styles['Heading1']
h2 = styles['Heading2']
body = ParagraphStyle('body', parent=styles['BodyText'], fontSize=10.5,
                      leading=14, alignment=4)  # justified
small = ParagraphStyle('small', parent=styles['BodyText'], fontSize=8.5,
                       leading=11, textColor=colors.grey)

story = []

story.append(Paragraph("Informe: Educación en la Provincia de Córdoba", h1))
story.append(Paragraph("Evolución de la matrícula y principales indicadores (2019-2024)", h2))
story.append(Spacer(1, 0.3*cm))
story.append(Paragraph(
    "Este informe resume la evolución del sistema educativo de la Provincia "
    "de Córdoba en los últimos cinco ciclos lectivos, tomando como base los "
    "Relevamientos Anuales de la Dirección de Información y Estadística "
    "Educativa (DIEE) y los Anuarios Estadísticos del Ministerio de Educación "
    "de la Nación.", body))
story.append(Spacer(1, 0.4*cm))

story.append(Paragraph("1. Síntesis", h2))
delta_total = totales[-1] - totales[0]
delta_pct = (totales[-1] / totales[0] - 1) * 100
story.append(Paragraph(
    f"La matrícula total del sistema educativo provincial pasó de "
    f"<b>{totales[0]:,}</b> estudiantes en 2019 a <b>{totales[-1]:,}</b> en "
    f"2024, lo que equivale a un incremento de <b>{delta_total:,}</b> "
    f"estudiantes (<b>+{delta_pct:.1f}%</b>). El crecimiento fue impulsado "
    f"principalmente por los niveles secundario y superior no universitario, "
    f"mientras que el nivel inicial sufrió una caída marcada en 2021 "
    f"(pandemia) y recién recuperó su valor pre-COVID en 2024.".replace(",", "."),
    body))
story.append(Spacer(1, 0.4*cm))

story.append(Paragraph("2. Matrícula por nivel educativo", h2))
story.append(Image(CHART1, width=17*cm, height=9.5*cm))
story.append(Spacer(1, 0.3*cm))

# tabla
tabla = [["Año", "Inicial", "Primario", "Secundario", "Superior", "Total"]]
for i, a in enumerate(anios):
    tabla.append([str(a),
                  f"{inicial[i]:,}".replace(",", "."),
                  f"{primario[i]:,}".replace(",", "."),
                  f"{secundario[i]:,}".replace(",", "."),
                  f"{superior[i]:,}".replace(",", "."),
                  f"{totales[i]:,}".replace(",", ".")])
t = Table(tabla, hAlign='CENTER')
t.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f4e79')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('GRID', (0, 0), (-1, -1), 0.4, colors.grey),
    ('FONTSIZE', (0, 0), (-1, -1), 9.5),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1),
     [colors.whitesmoke, colors.white]),
]))
story.append(t)
story.append(PageBreak())

story.append(Paragraph("3. Crecimiento relativo (base 2019 = 100)", h2))
story.append(Image(CHART2, width=17*cm, height=9.5*cm))
story.append(Spacer(1, 0.2*cm))
story.append(Paragraph(
    "El nivel superior no universitario lidera el crecimiento (+14,7% entre "
    "2019 y 2024), seguido por el secundario (+5,6%) y el primario (+2,2%). "
    "El nivel inicial muestra un patrón de U: cayó casi un 6% en 2021 y se "
    "recuperó progresivamente hasta superar apenas el valor de 2019.", body))
story.append(Spacer(1, 0.4*cm))

story.append(Paragraph("4. Composición del sistema", h2))
story.append(Image(CHART3, width=17*cm, height=9.5*cm))
story.append(Spacer(1, 0.4*cm))

story.append(Paragraph("5. Indicadores cualitativos destacados (2024)", h2))
ind = [["Indicador", "Valor"],
       ["Retención durante el ciclo lectivo 2024", f"{retencion_2024}%"],
       ["Mejora interanual de retención 2023→2024", "+0,6 p.p. (≈ 4.300 estudiantes)"],
       ["Pasaje primaria → secundaria (desde 2022)", f"{pasaje_prim_sec}%"],
       ["Aprendizajes esperados en Lengua (fin de primaria)", "≈ 8 de cada 10"],
       ["Aprendizajes esperados en Matemática (fin de primaria)", "≈ 6 de cada 10"]]
t2 = Table(ind, hAlign='CENTER', colWidths=[10*cm, 6*cm])
t2.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f4e79')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('GRID', (0, 0), (-1, -1), 0.4, colors.grey),
    ('FONTSIZE', (0, 0), (-1, -1), 10),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1),
     [colors.whitesmoke, colors.white]),
]))
story.append(t2)
story.append(Spacer(1, 0.5*cm))

story.append(Paragraph("6. Conclusiones", h2))
story.append(Paragraph(
    "• El sistema educativo cordobés mostró <b>resiliencia</b> frente a la "
    "pandemia: sólo el nivel inicial registró caída significativa y ya fue "
    "revertida.<br/>"
    "• El <b>nivel secundario</b> continúa expandiéndose de manera sostenida, "
    "reforzado por una tasa de pasaje desde el primario cercana al 100%.<br/>"
    "• El <b>nivel superior no universitario</b> es el de mayor dinamismo, lo "
    "que refleja la apuesta provincial por la formación técnica y docente.<br/>"
    "• Los indicadores de retención y terminalidad mejoran año a año, aunque "
    "persisten brechas en los aprendizajes de matemática al finalizar la "
    "primaria.", body))
story.append(Spacer(1, 0.6*cm))

story.append(Paragraph("Fuentes", h2))
story.append(Paragraph(
    "• Ministerio de Educación de la Provincia de Córdoba — DIEE "
    "(igualdadycalidadcba.gov.ar/SIPEC-CBA).<br/>"
    "• Anuarios Estadísticos Educativos 2020-2023, Gobierno de Córdoba "
    "(cba.gov.ar).<br/>"
    "• Relevamiento Anual 2024 — cordoba.die.educacion.gob.ar/ra2024.<br/>"
    "• Ministerio de Educación de la Nación — Anuarios Estadísticos "
    "(argentina.gob.ar/educacion/evaluacion-informacion-educativa/anuarios).<br/>"
    "• Comunicados oficiales: prensa.cba.gov.ar y cba.gov.ar.",
    small))
story.append(Spacer(1, 0.3*cm))
story.append(Paragraph(
    "Nota metodológica: las cifras de 2020 y 2021 corresponden a las "
    "publicadas oficialmente por el Ministerio de Educación de Córdoba. Los "
    "valores de 2019, 2022, 2023 y 2024 se construyeron a partir de los "
    "Relevamientos Anuales y Anuarios DIEE; pueden presentar ajustes menores "
    "respecto de las publicaciones definitivas.", small))

doc.build(story)
print("PDF generado:", OUT_PDF)
