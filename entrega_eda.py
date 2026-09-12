"""Genera el PDF de entrega de la evaluacion 2 (EDA), con el link al repositorio.

Una pagina. El texto se edita aca, no en el PDF.
Nada de subindices Unicode (t con subindice 50): Helvetica los dibuja como cuadrados.

Uso:  uv run python capstone/entrega_eda.py
"""
from pathlib import Path

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                TableStyle, KeepTogether)

# --- Lo unico que hay que editar si cambia el repositorio --------------------
USUARIO = "fleivadiaz"
REPO = "capstone-natacion"
URL = f"https://github.com/{USUARIO}/{REPO}"
# ----------------------------------------------------------------------------

SALIDA = str(Path(__file__).resolve().parent / "Entrega_EDA_Leiva_Fuentes.pdf")

TINTA = colors.HexColor("#1a1a1a")
GRIS = colors.HexColor("#5a5a5a")
LINEA = colors.HexColor("#c8c8c8")
FONDO = colors.HexColor("#f0f0f0")
DESTACA = colors.HexColor("#eaf1f7")
AZUL = colors.HexColor("#0b4f8a")

ss = getSampleStyleSheet()

titulo = ParagraphStyle("titulo", parent=ss["Normal"], fontName="Helvetica-Bold",
                        fontSize=14, leading=17, textColor=TINTA, spaceAfter=2)
subtitulo = ParagraphStyle("subtitulo", parent=ss["Normal"], fontName="Helvetica",
                           fontSize=8.5, leading=11.5, textColor=GRIS, spaceAfter=12)
h = ParagraphStyle("h", parent=ss["Normal"], fontName="Helvetica-Bold",
                   fontSize=10, leading=12.5, textColor=TINTA,
                   spaceBefore=10, spaceAfter=4, keepWithNext=1)
p = ParagraphStyle("p", parent=ss["Normal"], fontName="Helvetica", fontSize=8.7,
                   leading=11.7, textColor=TINTA, alignment=4, spaceAfter=4.5)
nota = ParagraphStyle("nota", parent=p, fontSize=7.6, leading=10, textColor=GRIS)
enlace = ParagraphStyle("enlace", parent=ss["Normal"], fontName="Helvetica-Bold",
                        fontSize=11.5, leading=15, textColor=AZUL, alignment=1)
celda = ParagraphStyle("celda", parent=ss["Normal"], fontName="Helvetica",
                       fontSize=7.3, leading=9, textColor=TINTA)
celda_b = ParagraphStyle("celda_b", parent=celda, fontName="Helvetica-Bold")


def tabla(datos, anchos, alinear_centro=()):
    filas = [[Paragraph(c, celda_b if i == 0 else celda) for c in fila]
             for i, fila in enumerate(datos)]
    t = Table(filas, colWidths=anchos, hAlign="LEFT")
    estilo = [
        ("BACKGROUND", (0, 0), (-1, 0), FONDO),
        ("LINEBELOW", (0, 0), (-1, 0), 0.6, LINEA),
        ("LINEBELOW", (0, 1), (-1, -2), 0.25, colors.HexColor("#e4e4e4")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 2.6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2.6),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
    ]
    for c in alinear_centro:
        estilo.append(("ALIGN", (c, 0), (c, -1), "CENTER"))
    t.setStyle(TableStyle(estilo))
    return t


doc = SimpleDocTemplate(SALIDA, pagesize=A4,
                        leftMargin=2.1 * cm, rightMargin=2.1 * cm,
                        topMargin=1.8 * cm, bottomMargin=1.7 * cm,
                        title="Entrega 2 - Primer analisis exploratorio de datos",
                        author="Felipe Leiva y Javier Fuentes")

S = []
A = S.append

A(Paragraph("Entrega 2 &nbsp;·&nbsp; Primer análisis exploratorio de datos", titulo))
A(Paragraph(
    "¿Es equivalente la exigencia para clasificar según el tipo de piscina "
    "en que se nade?<br/>"
    "<b>Felipe Leiva y Javier Fuentes</b> &nbsp;·&nbsp; "
    "Diplomado en Ciencia de Datos Aplicada, UTFSM &nbsp;·&nbsp; "
    "Módulo 1 &nbsp;·&nbsp; martes 15 de septiembre de 2026", subtitulo))

# --- El link ----------------------------------------------------------------
caja = Table([[Paragraph(f'<link href="{URL}">{URL}</link>', enlace)]],
             colWidths=[doc.width], hAlign="LEFT")
caja.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, -1), DESTACA),
    ("BOX", (0, 0), (-1, -1), 0.6, LINEA),
    ("TOPPADDING", (0, 0), (-1, -1), 9),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 9),
]))
A(caja)
A(Spacer(1, 4))
A(Paragraph(
    "El repositorio es público, así que no hace falta ninguna invitación para "
    "abrirlo: el link basta. El entregable es el notebook "
    "<b>03_eda_capstone.ipynb</b>, ejecutado de principio a fin, que se ve "
    "renderizado en la propia página de GitHub.", nota))

# --- Qué hay y en qué orden -------------------------------------------------
A(Paragraph("Qué contiene el repositorio y en qué orden se ejecuta", h))
A(Paragraph(
    "La entrega consta de un notebook y dos scripts auxiliares que producen los "
    "archivos que ese notebook lee. El notebook no importa ningún otro archivo "
    "de la carpeta: con los dos insumos en su lugar, corre entero por sí solo.", p))
A(tabla([
    ["Orden", "Archivo", "Qué hace"],
    ["1", "descargar.py",
     "Descarga los rankings de la temporada 2024 desde la API de World Aquatics: "
     "48 consultas (12 pruebas x 2 sexos x 2 piscinas) en modo BEST_TIMES, con "
     "caché local y pausa entre peticiones. Produce datos/nados.csv"],
    ["2", "factor_implicito_wa.py",
     "Transcribe las marcas mínimas oficiales del Mundial de 25 m de Beijing 2026, "
     "calcula el factor de conversión implícito en ellas y su brecha contra el "
     "medido. Produce datos/comparacion_wa.csv, que sí va en el repositorio"],
    ["3", "03_eda_capstone.ipynb",
     "<b>El entregable.</b> Lee esos dos archivos y calcula todo lo demás: "
     "limpieza, cruce dentro-nadador, descriptivos, bivariado, las cinco figuras "
     "y los hallazgos"],
], [1.3 * cm, 3.6 * cm, doc.width - 4.9 * cm], alinear_centro=(0,)))
A(Spacer(1, 3))
A(Paragraph(
    "El README del repositorio documenta además el resto de los archivos "
    "versionados: las tablas agregadas de datos/, las dos sondas con que se "
    "midieron las restricciones de la API, los scripts de respaldo de lo que se "
    "afirma en el texto y el material de las entregas anteriores.", nota))

# --- Los datos --------------------------------------------------------------
A(Paragraph("Los datos crudos no se pueden compartir", h))
A(Paragraph(
    "Los términos legales de World Aquatics prohíben en su sección 3 la "
    "redistribución de sus contenidos. Por eso <b>datos/nados.csv</b> (62 MB, "
    "193.142 filas) y la tabla de pares <b>datos/pares_lcm_scm.csv</b> no están "
    "en el repositorio, y así se declara en la primera celda del notebook. Para "
    "regenerarlos basta correr <b>uv run python capstone/descargar.py</b>: son 48 "
    "consultas con pausa entre ellas, unos minutos la primera vez, y el script "
    "cachea cada respuesta, de modo que una segunda corrida no vuelve a pedir nada. "
    "Sí van en el repositorio las tablas agregadas (comparacion_wa.csv, "
    "factores_por_prueba.csv, factor_por_nivel.csv, metadatos.md): son estadísticas "
    "por prueba y no contienen marcas individuales.", p))

# --- Dónde está cada criterio ----------------------------------------------
A(Paragraph("Dónde se cumple cada criterio de la rúbrica", h))
A(tabla([
    ["Criterio", "Sección del notebook"],
    ["1. Los datos y su calidad",
     "Sección 1. Tipos y nulos (1.1); faltantes disfrazados, con los dos "
     "centinelas encontrados (1.2); duplicados, verificados con assert (1.3); "
     "valores imposibles en segundos por metro (1.4); el cruce LCM-SCM con "
     "validate one_to_one y conteos antes y después (1.5); y la bitácora con las "
     "siete decisiones de limpieza (1.6)"],
    ["2. Estadística descriptiva",
     "Sección 2. Centro, dispersión, asimetría y curtosis de las seis variables "
     "relevantes, interpretadas en el contexto, más la declaración de que los "
     "rankings no traen factores de expansión y por lo tanto no se inventan"],
    ["3. Análisis bivariado",
     "Sección 3, con el objetivo declarado antes de cada análisis: factor contra "
     "distancia con Pearson y Spearman (3.1); el sesgo de selección por nivel "
     "(3.2); la matriz de correlación de Spearman (3.3); el factor por estilo "
     "(3.4); la tabla de contingencia sexo x estilo (3.5); y la brecha entre "
     "sexos con Mann-Whitney, prueba por prueba (3.6)"],
    ["4. Visualización",
     "Sección 4. Cinco gráficos de tipos distintos: histograma (4.1), boxplot "
     "(4.2), dispersión con hexbin y ejes logarítmicos, que es el tratamiento "
     "del overplotting y las colas largas (4.3), líneas (4.4) y barras (4.5). "
     "Todos con título, ejes rotulados con unidad e interpretación escrita"],
    ["5. Hallazgos, código y reproducibilidad",
     "Sección 5. Cinco hallazgos en frases completas, el modelo que se ajustará "
     "en el informe de avance (diferencia_s contra vueltas_extra, por estilo y "
     "sexo) y las cuatro limitaciones declaradas"],
], [4.2 * cm, doc.width - 4.2 * cm]))

# --- IA ---------------------------------------------------------------------
A(Paragraph("Declaración de uso de inteligencia artificial", h))
A(Paragraph(
    "Se usó Claude (Anthropic) para explorar la documentación de la API de World "
    "Aquatics, discutir el diseño del análisis y revisar el código y la redacción. "
    "Los datos, las decisiones metodológicas y la interpretación son de los "
    "autores, que pueden explicar cada parte de lo entregado. La declaración está "
    "también en la primera celda del notebook.", p))

doc.build(S)
print("PDF escrito en:", SALIDA)
print("Link incluido  :", URL)
