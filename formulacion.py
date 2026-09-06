"""Genera el PDF de la formulacion del Capstone (3 paginas)."""
from pathlib import Path

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                TableStyle, KeepTogether)

SALIDA = str(Path(__file__).resolve().parent /
             "Formulacion_Capstone_Leiva_Fuentes.pdf")

TINTA = colors.HexColor("#1a1a1a")
GRIS = colors.HexColor("#5a5a5a")
LINEA = colors.HexColor("#c8c8c8")
FONDO = colors.HexColor("#f0f0f0")

ss = getSampleStyleSheet()

titulo = ParagraphStyle("titulo", parent=ss["Normal"], fontName="Helvetica-Bold",
                        fontSize=14, leading=17, textColor=TINTA, spaceAfter=2)
subtitulo = ParagraphStyle("subtitulo", parent=ss["Normal"], fontName="Helvetica",
                           fontSize=8.5, leading=11.5, textColor=GRIS, spaceAfter=10)
# keepWithNext evita que un titulo quede solo al pie de una pagina.
h = ParagraphStyle("h", parent=ss["Normal"], fontName="Helvetica-Bold",
                   fontSize=10, leading=12.5, textColor=TINTA,
                   spaceBefore=9, spaceAfter=3.5, keepWithNext=1)
p = ParagraphStyle("p", parent=ss["Normal"], fontName="Helvetica", fontSize=8.7,
                   leading=11.7, textColor=TINTA, alignment=4, spaceAfter=4.5)
nota = ParagraphStyle("nota", parent=p, fontSize=7.6, leading=10, textColor=GRIS)
celda = ParagraphStyle("celda", parent=ss["Normal"], fontName="Helvetica",
                       fontSize=7.3, leading=9, textColor=TINTA)
celda_b = ParagraphStyle("celda_b", parent=celda, fontName="Helvetica-Bold")


def tabla(datos, anchos, alinear_der=()):
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
    for c in alinear_der:
        estilo.append(("ALIGN", (c, 0), (c, -1), "RIGHT"))
    t.setStyle(TableStyle(estilo))
    return t


doc = SimpleDocTemplate(SALIDA, pagesize=A4,
                        leftMargin=2.1*cm, rightMargin=2.1*cm,
                        topMargin=1.8*cm, bottomMargin=1.7*cm,
                        title="Formulacion del proyecto Capstone",
                        author="Felipe Leiva y Javier Fuentes")

S = []
A = S.append

A(Paragraph("Formulación del proyecto Capstone", titulo))
A(Paragraph(
    "¿Es equivalente la exigencia para clasificar según el tipo de piscina "
    "en que se nade?<br/>"
    "<b>Felipe Leiva y Javier Fuentes</b> &nbsp;·&nbsp; "
    "Diplomado en Ciencia de Datos Aplicada, UTFSM &nbsp;·&nbsp; "
    "Módulo 1 &nbsp;·&nbsp; 7 de septiembre de 2026", subtitulo))

# ---------------------------------------------------------------- 1
A(Paragraph("1. El problema y la pregunta", h))
A(Paragraph(
    "La natación competitiva se disputa en dos tipos de piscina: 50 metros "
    "(larga) y 25 metros (corta). Sobre la misma distancia, la piscina corta "
    "obliga al doble de virajes, y cada viraje incluye un impulso en la pared y "
    "una fase subacuática más rápida que el nado en superficie. Los calendarios "
    "alternan ambas, de modo que un mismo nadador acumula marcas en las dos a lo "
    "largo del año, y compararlas es una operación cotidiana para entrenadores, "
    "federaciones y medios.", p))
A(Paragraph(
    "No existe una equivalencia validada entre ambas. World Aquatics no convierte "
    "tiempos: publica <b>dos tablas separadas de marcas mínimas</b>, una por tipo "
    "de piscina, y acepta el tiempo logrado en cualquiera de las dos contra la "
    "tabla que corresponda. Al exigir 4:37.46 minutos en piscina corta y 4:43.06 "
    "en larga —5,60 segundos de diferencia— por el mismo cupo en 400 combinado "
    "femenino, la federación declara de hecho que ambas actuaciones son "
    "equivalentes. En el ámbito de clubes y entrenadores, las calculadoras de "
    "conversión de uso habitual aplican reglas mecánicas —un factor de escala más "
    "un incremento fijo por viraje— iguales para todos.", p))
A(Paragraph(
    "El problema es que ninguna de esas equivalencias se ha contrastado con lo que "
    "los nadadores efectivamente hacen. La consecuencia es una decisión concreta: "
    "si la equivalencia implícita no coincide con la real, <b>clasificar a un "
    "campeonato resulta más difícil en una piscina que en otra, y la diferencia "
    "depende de la prueba que se nade</b>.", p))
A(Paragraph(
    "<b>Pregunta.</b> ¿Es constante el factor de conversión entre piscina de 25 y "
    "50 metros, o depende del estilo, la distancia y el sexo? ¿Y coincide con la "
    "equivalencia implícita en las marcas mínimas vigentes de World Aquatics?", p))
A(Paragraph(
    "<b>Hipótesis.</b> Si la ventaja de la piscina corta proviniera únicamente de "
    "dar más virajes, y cada viraje aportara lo mismo, la diferencia de tiempo "
    "entre ambas piscinas sería proporcional al número de virajes adicionales "
    "(distancia/50) y el factor sería constante entre pruebas. Sostenemos que no "
    "lo es: la ventaja por viraje depende del estilo, y es mayor en espalda y "
    "pecho, donde la fase subacuática es más ventajosa respecto de la velocidad en "
    "superficie. En consecuencia, un factor único subestima la conversión en unos "
    "estilos y la sobreestima en otros.", p))

# ---------------------------------------------------------------- 2
A(Paragraph("2. Los datos y sus metadatos", h))
A(Paragraph(
    "<b>Fuente 1.</b> La API pública de rankings de World Aquatics "
    "(<font face='Courier' size='7.8'>api.worldaquatics.com/fina/rankings/swimming</font>), "
    "organismo que rige la natación mundial y consolida los resultados que le "
    "reportan las federaciones nacionales y los organizadores de cada competencia. "
    "Cada fila es la mejor marca del año de un nadador en una prueba y un tipo de "
    "piscina. Se descargó la temporada 2024 completa para 12 pruebas × 2 sexos × 2 "
    "tipos de piscina: <b>193.142 nados de 56.035 nadadores, 201 países y 306 "
    "competencias</b>. De ahí se construye la tabla de análisis: <b>30.257 pares</b> "
    "—mismo nadador, misma temporada, una marca en cada piscina—, aportados por "
    "12.531 nadadores distintos, con un mínimo de 570 pares en la combinación "
    "menos poblada.", p))
A(Paragraph(
    "<b>Población.</b> Nadadores rankeados por World Aquatics durante 2024 en 50, "
    "100, 200 y 400 libre; 100 y 200 espalda; 100 y 200 pecho; 100 y 200 mariposa; "
    "y 200 y 400 combinado, que registren al menos una marca en cada tipo de "
    "piscina. Quedan fuera 800 y 1500 libre, que rara vez se nadan en piscina "
    "corta, y 100 combinado, que solo existe en piscina corta.", p))
A(Paragraph(
    "<b>Fuente 2.</b> Las marcas mínimas de clasificación al Mundial de 25 m "
    "Beijing 2026, publicadas por World Aquatics en PDF: dos tablas (piscina de 25 "
    "y de 50 m) × dos niveles de exigencia (A y B) × 24 pruebas.", p))

A(Spacer(1, 2))
A(tabla([
    ["Variable", "Tipo", "Unidad o valores", "Nulos", "Quién lo produce"],
    ["person_id", "texto (UUID)", "identificador de nadador", "0%", "World Aquatics"],
    ["sexo", "categórica", "M / F", "0%", "World Aquatics"],
    ["estilo", "categórica", "5 estilos", "0%", "World Aquatics"],
    ["distancia", "entera", "metros: 50 / 100 / 200 / 400", "0%", "World Aquatics"],
    ["piscina", "categórica", "LCM (50 m) / SCM (25 m)", "0%", "World Aquatics"],
    ["tiempo_s", "decimal", "segundos", "0%", "cronometraje oficial del torneo"],
    ["puntos_fina", "decimal", "puntos, 8 a 1.078", "0%", "World Aquatics"],
    ["fecha", "fecha", "día del nado", "0%", "organizador de la competencia"],
    ["competencia", "texto", "nombre del torneo", "0%", "organizador de la competencia"],
    ["edad", "decimal", "años cumplidos al nadar", "6,3%", "World Aquatics"],
], [2.6*cm, 2.1*cm, 5.0*cm, 1.3*cm, 5.6*cm], alinear_der=(3,)))
A(Spacer(1, 5))
A(Paragraph(
    "Variables construidas: <b>factor</b> = tiempo_lcm / tiempo_scm (razón entre "
    "dos tiempos, sin unidad; la variable central), <b>diferencia_s</b> "
    "(segundos), <b>vueltas_extra</b> = distancia/50 (conteo) y "
    "<b>por_vuelta_s</b> = diferencia / vueltas extra (segundos por vuelta). El "
    "diccionario completo de las 25 variables se genera desde los datos y acompaña "
    "al código.", p))
A(Paragraph(
    "<b>Calidad, medida y no supuesta.</b> La clave (person_id, piscina, prueba) "
    "identifica una fila sin duplicados en las 193.142. Se detectaron cuatro "
    "problemas que se documentan: <i>edad</i> viene incompleta (6,3%) y con "
    "valores imposibles —dos nadadores de 119 años—, por lo que no se usa en el "
    "análisis; <i>club</i> trae el texto literal “No” en 30.483 filas (15,8%) en "
    "lugar de un valor faltante, un ausente disfrazado que al contar clubes se "
    "sumaría como uno más, y aparecería como el mayor de todos, con 33 veces los "
    "nadadores del que le sigue; tres tiempos son físicamente imposibles para una "
    "competencia oficial —entre 2,5 y 3,1 segundos por metro, cuando el resto del "
    "conjunto va de 0,40 a 1,10— y se descartan; y los campos <i>result_id</i> y "
    "<i>event_id</i> <b>no identifican el nado</b>, pues son constantes para cada "
    "nadador aun entre pruebas y piscinas distintas. Esto último se verificó en la "
    "respuesta cruda de la API, de modo que es una limitación de la fuente y no "
    "del procesamiento, y descarta usar esos identificadores para recuperar los "
    "tiempos parciales.", p))

# ---------------------------------------------------------------- 3
A(Paragraph("3. Estrategia de obtención", h))
A(Paragraph(
    "<b>Fuente 1.</b> Se descarga con un script escrito solo con la biblioteca "
    "estándar de Python: 48 consultas, una por combinación de prueba, sexo y tipo "
    "de piscina, con los parámetros <i>timesMode=BEST_TIMES</i> y "
    "<i>pageSize=5000</i>. El script espera medio segundo entre peticiones, "
    "reintenta hasta tres veces ante error y guarda cada respuesta en un caché "
    "local, de modo que volver a ejecutarlo no genera tráfico nuevo. La descarga "
    "completa produce 193.142 filas y 60 MB.", p))
A(Paragraph(
    "<b>Restricciones de acceso, medidas y no supuestas.</b> Dos sondas "
    "establecieron los límites del servicio. <i>La API no pagina</i>: se probaron "
    "ocho parámetros distintos (page, pageNumber, pageIndex, offset, start, skip, "
    "from, firstResult) y los ocho se ignoran, la respuesta siempre empieza en el "
    "primer puesto. <i>pageSize tiene un tope de 5.000</i>; con valores mayores el "
    "servicio responde 404. De ahí se sigue la decisión de diseño más importante de "
    "la descarga: usar BEST_TIMES, una fila por nadador, en vez de ALL_TIMES, con "
    "el cual los 5.000 registros disponibles los aportan unas pocas decenas de "
    "nadadores que compiten muchas veces al año. Este límite implica un sesgo de "
    "cobertura que se declara: la muestra corresponde a los 5.000 mejores de cada "
    "prueba, no a una muestra aleatoria de la población de nadadores.", p))
A(Paragraph(
    "<b>Permisos.</b> El servicio no requiere autenticación ni clave. Los términos "
    "de uso del sitio de World Aquatics prohíben la extracción automatizada de "
    "contenidos sin licencia escrita. El proyecto se limita a un uso académico, sin "
    "fines comerciales: acota la frecuencia de las peticiones, cachea cada "
    "respuesta para no repetir tráfico, no redistribuye los datos crudos y publica "
    "únicamente el código de descarga. Una difusión de los resultados fuera del "
    "ámbito del curso requeriría solicitar autorización expresa.", p))
A(Paragraph(
    "<b>Frecuencia.</b> Los rankings se actualizan de forma continua a medida que "
    "las federaciones cargan resultados. El proyecto trabaja sobre la temporada "
    "2024, ya cerrada, por lo que el conjunto es estable: el corte se tomó el 1 de "
    "septiembre de 2026 y no cambiará. Ampliar el estudio a otras temporadas "
    "consiste en editar una lista de años en el script. <b>Fuente 2</b> es un "
    "documento PDF de acceso público que se descarga una vez y cuyos 96 tiempos se "
    "transcriben al código, verificados contra el original; se publica una vez por "
    "ciclo y no cambia dentro del período de clasificación.", p))

# ---------------------------------------------------------------- 4
A(Paragraph("4. Viabilidad", h))
A(Paragraph(
    "El riesgo principal de cualquier formulación es que los datos no existan, no "
    "se puedan obtener o no permitan responder la pregunta. En este proyecto ese "
    "riesgo ya está resuelto: los datos están descargados, revisados y cruzados, y "
    "el resultado central está calculado.", p))
A(Paragraph(
    "<b>Volumen y cómputo.</b> El conjunto completo son 193.142 filas y 60 MB. "
    "Leer los datos, cruzar las marcas de ambas piscinas y calcular el factor de "
    "las 24 combinaciones de sexo, estilo y distancia toma menos de un segundo en "
    "un computador personal.", p))
A(Paragraph(
    "<b>Herramientas.</b> Python, con Pandas y NumPy para construir y unir las "
    "tablas, SciPy y statsmodels para los contrastes y las regresiones, y "
    "Matplotlib para los gráficos.", p))
A(Paragraph(
    "<b>Contingencias.</b> Cada respuesta de la API quedó guardada en un caché "
    "local, de modo que el análisis es reproducible sin conexión aunque el servicio "
    "cambie. Las marcas mínimas están transcritas dentro del código. El equipo "
    "trabaja sobre un repositorio compartido.", p))

# ---------------------------------------------------------------- 5
A(Paragraph("5. Novedad e impacto", h))
A(Paragraph(
    "Que el rendimiento difiera entre piscinas es un fenómeno conocido. Iglesias "
    "García y colaboradores (2025) lo documentaron sobre los rankings de la "
    "Federación Española de Natación, encontrando diferencias mayores en espalda y "
    "pecho que en mariposa y libre, y más pronunciadas en los 200 metros. Análisis "
    "basados en récords nacionales e internacionales llegan a conclusiones "
    "similares y advierten que un factor de conversión único es inadecuado. Este "
    "proyecto no pretende descubrir ese fenómeno, sino medirlo con un diseño y una "
    "escala distintos y llevarlo hasta la decisión que depende de él.", p))
A(Paragraph(
    "<b>Diseño y escala.</b> El estudio disponible más cercano, el de Iglesias "
    "García y colaboradores, trabaja con los 200 mejores nadadores españoles de "
    "cada prueba en las temporadas 2017-2018 y 2018-2019. Aquí se comparan 30.257 "
    "pares de marcas, de 12.531 nadadores de 201 países en una misma temporada, y "
    "cada nadador se compara consigo mismo, lo que elimina el talento, la edad y el "
    "entrenamiento como variables de confusión sin necesidad de controlarlas "
    "estadísticamente.", p))
A(Paragraph(
    "<b>Un resultado que contradice a la literatura reciente.</b> El estudio de "
    "2025 reporta diferencias mínimas entre sexos. En esta muestra los hombres "
    "presentan un factor mayor que las mujeres en las doce pruebas comparables, sin "
    "excepción y con significación estadística en todas, con una diferencia de "
    "entre 0,6 y 1,2 puntos porcentuales. No sostenemos que ese estudio esté "
    "equivocado: mide a 200 nadadores de un solo país repartidos en categorías de "
    "edad, y esta muestra es la élite mundial de una temporada, de modo que la "
    "discrepancia puede venir de a quién se mide. Lo que sí se sigue es que la "
    "conclusión —que el sexo no altera la conversión— no puede darse por general, y "
    "que una tabla de factores debería separar hombres de mujeres. Delimitar hasta "
    "dónde vale un resultado ya publicado es en sí mismo un aporte.", p))
A(Paragraph(
    "<b>El contraste con la norma vigente.</b> Ningún análisis disponible compara "
    "el factor observado con la equivalencia implícita en las marcas mínimas en "
    "uso. Al hacerlo aparece que esa equivalencia oscila entre 1,003 y 1,062 según "
    "la prueba, y que en varias se aparta de la observada en más de dos segundos, "
    "en direcciones opuestas según el caso.", p))
A(Spacer(1, 2))
A(KeepTogether([
    tabla([
        ["Prueba",
         "Factor implícito en las<br/>marcas mínimas (t50 / t25)",
         "Factor medido en 2024<br/>(t50 / t25; 30.257 pares)",
         "Diferencia<br/>(segundos)"],
        ["400 combinado femenino", "1,0202", "1,0334", "+3,66"],
        ["200 mariposa femenino", "1,0028", "1,0250", "+2,86"],
        ["400 libre femenino", "1,0161", "1,0254", "+2,30"],
        ["200 pecho masculino", "1,0324", "1,0450", "+1,60"],
        ["100 libre masculino", "1,0309", "1,0304", "−0,02"],
        ["100 espalda masculino", "1,0616", "1,0491", "−0,64"],
    ], [5.3*cm, 4.0*cm, 4.0*cm, 3.3*cm], alinear_der=(1, 2, 3)),
    Spacer(1, 3),
    Paragraph(
        "Resultados preliminares. Los factores son razones entre tiempos y no "
        "tienen unidad; la diferencia va en segundos. Una diferencia positiva "
        "significa que la marca exigida en 25 m es más lenta que la que "
        "correspondería a la exigida en 50 m según el factor medido: para el mismo "
        "cupo, la exigencia es menor en piscina corta. En 400 combinado "
        "femenino, por ejemplo, la marca de 25 m (4:37.46) equivale con el factor "
        "medido a 4:46.72 en piscina larga, pero la federación exige allí 4:43.06, "
        "3,66 segundos más rápido. Una diferencia negativa dice lo contrario. Que "
        "aparezcan ambos signos muestra que el desajuste no favorece de forma "
        "sistemática a un tipo de piscina, sino que cambia de una prueba a otra.",
        nota),
]))
A(Spacer(1, 4))
A(Paragraph(
    "<b>Una advertencia metodológica.</b> El factor de cada nadador es un cociente "
    "entre sus dos marcas, y por eso seleccionar a los mejores por una sola de "
    "ellas deforma el resultado. Quien firma su mejor marca del año en piscina "
    "corta suele hacerlo en un día especialmente bueno: al quedarse con los "
    "primeros de esa lista se toman tiempos de 25 m más rápidos de lo que ese "
    "nadador rinde habitualmente, el denominador del cociente queda bajo y el "
    "factor sube. Seleccionando por la marca de 50 m pasa lo contrario. Sin cambiar "
    "de nadadores, el factor de la «élite» va de 1,0277 a 1,0372 según con cuál de "
    "las dos marcas se la defina: casi un punto porcentual que no viene de nadar "
    "distinto, sino de cómo se armó el grupo. Con un criterio neutral —el promedio "
    "de ambas marcas— el efecto del nivel cae hasta volverse irrelevante (rho de "
    "Spearman de −0,02, frente a −0,28 del criterio sesgado), y esa es la cifra que "
    "el proyecto reporta.", p))
A(Paragraph(
    "<b>Quién usaría los resultados.</b> Las federaciones que fijan marcas mínimas, "
    "para calibrar ambas tablas sobre una equivalencia empírica y no sobre una "
    "regla fija; los entrenadores y nadadores, para interpretar si una marca "
    "lograda en la otra piscina representa una mejora real o un efecto del recinto; "
    "y quienes desarrollan las calculadoras de conversión de uso habitual. El "
    "producto concreto es una tabla de factores por estilo, distancia y sexo, con "
    "su incertidumbre, y el código que permite recalcularla para cualquier "
    "temporada.", p))

# ---------------------------------------------------------------- cierre
A(Paragraph("Fuentes y declaración de uso de IA", h))
A(Paragraph(
    "World Aquatics, <i>Qualification – World Aquatics Swimming Championships "
    "(25m) Beijing 2026</i>, resources.fina.org (marcas mínimas). · World Aquatics, "
    "API pública de rankings de natación. · Iglesias García, J., "
    "Hermosilla-Perona, F., Gonjo, T. y Juárez Santos-García, D. (2025). "
    "<i>Impact of course length on swimming performance across age groups and "
    "swimming strokes</i>. Frontiers in Sports and Active Living. · World "
    "Aquatics, términos legales del sitio (restricciones de uso).", nota))
A(Paragraph(
    "<b>Declaración de uso de IA.</b> Se utilizó Claude (Anthropic) como apoyo en "
    "la revisión de la normativa de clasificación, en la redacción y ordenamiento "
    "de este documento y en la escritura y depuración de los scripts de descarga y "
    "análisis. La pregunta de investigación, las decisiones metodológicas y la "
    "verificación de los resultados son de los autores, que pueden explicar cada "
    "parte de lo entregado.", nota))


def pie(canvas, documento):
    canvas.saveState()
    canvas.setFont("Helvetica", 7.2)
    canvas.setFillColor(GRIS)
    canvas.drawCentredString(A4[0] / 2, 1.05 * cm, str(documento.page))
    canvas.restoreState()


doc.build(S, onFirstPage=pie, onLaterPages=pie)
print("PDF generado:", SALIDA)
