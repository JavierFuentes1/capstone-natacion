"""Genera Informe_Avance_Leiva_Fuentes.pdf — la entrega del viernes 25 de septiembre.

Evaluacion 3, informe escrito (50% de la evaluacion, 25% del modulo).
Maximo 7 paginas incluyendo graficos, tablas y bibliografia. Letra 11 pt.

EL TEXTO SE EDITA ACA, no en el PDF: cualquier cambio hecho sobre el PDF se
pierde la proxima vez que corra este script.

Uso, desde ~/diplomado-cdd:   uv run python capstone/informe_avance.py
Requiere reportlab (uv add reportlab). Lee las figuras de figuras_eda/.
"""

import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                TableStyle, Image, KeepTogether)

AQUI = os.path.dirname(os.path.abspath(__file__))
FIG = os.path.join(AQUI, "figuras_eda")
SALIDA = os.path.join(AQUI, "Informe_Avance_Leiva_Fuentes.pdf")

OSC = colors.HexColor("#0A3D5C")
GRIS = colors.HexColor("#5F7480")
TXT = colors.HexColor("#111111")
CLARO = colors.HexColor("#EDF4F8")

H1 = ParagraphStyle("H1", fontName="Times-Bold", fontSize=15, leading=18,
                    textColor=OSC, spaceBefore=12, spaceAfter=5,
                    keepWithNext=1)   # un titulo nunca queda solo al pie de pagina
H2 = ParagraphStyle("H2", fontName="Times-Bold", fontSize=11.5, leading=14,
                    textColor=OSC, spaceBefore=8, spaceAfter=3,
                    keepWithNext=1)
P = ParagraphStyle("P", fontName="Times-Roman", fontSize=11, leading=14.5,
                   textColor=TXT, spaceAfter=6, alignment=4, firstLineIndent=0)
PIE = ParagraphStyle("PIE", fontName="Times-Italic", fontSize=9, leading=11.5,
                     textColor=GRIS, spaceAfter=10, alignment=1)
BIB = ParagraphStyle("BIB", fontName="Times-Roman", fontSize=9.5, leading=12.5,
                     textColor=TXT, spaceAfter=5, alignment=4, leftIndent=14,
                     firstLineIndent=-14)
TIT = ParagraphStyle("TIT", fontName="Times-Bold", fontSize=17, leading=20,
                     textColor=OSC, spaceAfter=3)
SUB = ParagraphStyle("SUB", fontName="Times-Italic", fontSize=10.5, leading=13,
                     textColor=GRIS, spaceAfter=12)
RES = ParagraphStyle("RES", fontName="Times-Roman", fontSize=10.5, leading=13.5,
                     textColor=TXT, spaceAfter=4, alignment=4,
                     leftIndent=10, rightIndent=10)


def tabla(datos, anchos, cabecera=True, tam=9):
    # Las celdas van como Paragraph para que el texto largo baje de linea
    # en vez de desbordarse sobre la columna siguiente o cortarse en el margen.
    cel = ParagraphStyle("cel", fontName="Times-Roman", fontSize=tam,
                         leading=tam + 1.7, textColor=TXT)
    celb = ParagraphStyle("celb", parent=cel, fontName="Times-Bold")
    datos = [[c if hasattr(c, "wrap") else
              Paragraph(str(c), celb if (cabecera and i == 0) else cel)
              for c in fila]
             for i, fila in enumerate(datos)]
    t = Table(datos, colWidths=anchos, repeatRows=1 if cabecera else 0)
    e = [("FONTNAME", (0, 0), (-1, -1), "Times-Roman"),
         ("FONTSIZE", (0, 0), (-1, -1), tam),
         ("TEXTCOLOR", (0, 0), (-1, -1), TXT),
         ("VALIGN", (0, 0), (-1, -1), "TOP"),
         ("TOPPADDING", (0, 0), (-1, -1), 2.5),
         ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5),
         ("LINEBELOW", (0, 0), (-1, 0), 0.6, OSC)]
    if cabecera:
        e += [("FONTNAME", (0, 0), (-1, 0), "Times-Bold"),
              ("BACKGROUND", (0, 0), (-1, 0), CLARO)]
    t.setStyle(TableStyle(e))
    return t


def figura(archivo, ancho_cm, pie):
    ruta = os.path.join(FIG, archivo)
    from PIL import Image as PILImage
    w, h = PILImage.open(ruta).size
    ancho = ancho_cm * cm
    return [Image(ruta, width=ancho, height=ancho * h / w), Paragraph(pie, PIE)]


def build():
    doc = SimpleDocTemplate(SALIDA, pagesize=A4,
                            leftMargin=2.2*cm, rightMargin=2.2*cm,
                            topMargin=1.9*cm, bottomMargin=1.9*cm,
                            title="Informe de avance — Capstone natación",
                            author="Felipe Leiva · Javier Fuentes")
    E = []

    # ---------------------------------------------------------------- portada
    E.append(Paragraph("¿Es igual de difícil clasificar a un campeonato nadando "
                       "en piscina de 25 m o de 50 m?", TIT))
    E.append(Paragraph("Informe de avance · Felipe Leiva y Javier Fuentes · "
                       "Diplomado en Ciencia de Datos Aplicada, UTFSM · "
                       "Módulo 1, evaluación 3 · 25 de septiembre de 2026", SUB))

    # ---------------------------------------------------------------- resumen
    E.append(Paragraph("Resumen", H1))
    E.append(Paragraph(
        "El mismo nadador va más rápido en piscina de 25 m que en una de 50 m porque da "
        "el doble de virajes, y World Aquatics acepta marcas de ambas piscinas para "
        "clasificar a un campeonato con dos tablas de mínimas separadas. Medimos si la "
        "ventaja de la piscina corta es la misma en todas las pruebas usando 43.914 "
        "pares de marcas del mismo nadador en ambas piscinas durante 2024, tomados del "
        "ranking mensual de World Aquatics. El factor de conversión no es constante: va "
        "de 1,0181 a 1,0521 según la prueba, y los intervalos de confianza de esos dos "
        "extremos no se solapan. Los hombres se benefician más que las mujeres en las "
        "doce pruebas comparables. Un modelo de la diferencia sobre las vueltas extra "
        "estima entre 0,98 y 1,86 segundos por vuelta según el estilo. El paso siguiente "
        "es contrastar estas conclusiones con regresión regularizada.", RES))

    # ---------------------------------------------------- 1. contexto
    # Agregada tras la presentacion del 22-sep: se pidio mas contexto del problema.
    E.append(Paragraph("1. Contexto y problema", H1))
    E.append(Paragraph(
        "La natación competitiva se disputa en dos tipos de piscina. La de 50 m, o "
        "piscina larga, es la de los Juegos Olímpicos. La de 25 m, o piscina corta, es "
        "la más común en clubes y centros de entrenamiento, porque exige la mitad de "
        "largo, y tiene su propio circuito: World Aquatics organiza desde 1993 un "
        "Campeonato Mundial en piscina corta, cuya edición 2026 se disputa en Beijing. "
        "La temporada alterna ambos calendarios, de modo que un mismo nadador acumula "
        "marcas en las dos.", P))
    E.append(Paragraph(
        "Esas marcas no se comparan directamente porque la piscina corta obliga al doble "
        "de virajes (figura 1). En 100 m, la piscina de 50 m tiene un viraje y la de "
        "25 m, tres. Cada viraje agrega un impulso en la pared y una fase bajo el agua "
        "más rápida que el nado en superficie, que el reglamento limita a 15 m en libre, "
        "espalda y mariposa. En ese máximo, quien nada 100 m en piscina corta recorre en "
        "superficie apenas 40 m, contra 70 m en piscina larga. Los virajes adicionales "
        "son siempre la distancia dividida en 50: es la variable <b>vueltas_extra</b> "
        "del modelo de la sección 5.", P))
    E += figura("1-1_esquema_virajes.png", 14.0,
                "Figura 1. Esquema de una prueba de 100 m en cada piscina: a la izquierda, "
                "el recorrido visto desde arriba; a la derecha, los mismos 100 m en línea "
                "recta. Los 15 m tras cada pared son el máximo reglamentario en libre, "
                "espalda y mariposa, no lo que nada cada competidor; pecho tiene una regla "
                "propia.")
    E.append(Paragraph(
        "El problema aparece al clasificar a un campeonato. World Aquatics no publica un "
        "factor de conversión: fija dos tablas de marcas mínimas, una por tipo de "
        "piscina, y acepta cualquiera de las dos. Para el Mundial de Beijing 2026 exige "
        "en 400 m combinado femenino 4:37.46 en piscina corta o 4:43.06 en larga, y al "
        "hacerlo declara equivalentes ambas actuaciones. Las calculadoras de conversión "
        "de uso habitual hacen algo parecido con un factor único para todas las pruebas. "
        "Si esas equivalencias no coinciden con lo que los nadadores efectivamente "
        "hacen, clasificar resulta más fácil en una piscina que en la otra, y un nadador "
        "puede elegir mal dónde intentar su mínima. No encontramos un contraste de esas "
        "equivalencias con datos a escala mundial.", P))

    # ---------------------------------------------------- 2. objetivos
    E.append(Paragraph("2. Objetivos e hipótesis", H1))
    E.append(Paragraph(
        "<b>Objetivo general.</b> Determinar si el factor de conversión entre piscina de "
        "25 y de 50 metros es constante o depende del estilo, la distancia y el sexo, y "
        "contrastarlo con la equivalencia que World Aquatics aplica de hecho al fijar sus "
        "marcas mínimas de clasificación.", P))
    E.append(Paragraph(
        "<b>Objetivos específicos de esta etapa.</b> (i) Estimar el factor para cada una "
        "de las 24 pruebas con su margen de error; (ii) comprobar si la diferencia entre "
        "pruebas excede el error de muestreo; (iii) contrastar el factor medido con el "
        "implícito en las marcas mínimas del Mundial de 25 m de Beijing 2026; (iv) "
        "ajustar un primer modelo que cuantifique la ventaja por vuelta.", P))
    E.append(Paragraph(
        "<b>Hipótesis.</b> Si la ventaja de la piscina corta proviniera únicamente de los "
        "virajes adicionales de la figura 1 y cada uno valiera lo mismo, la diferencia "
        "entre ambas marcas "
        "sería proporcional al número de vueltas extra (distancia dividida en 50) y el "
        "factor sería idéntico en todas las pruebas. La hipótesis es verificable y se "
        "rechaza si el factor cambia sistemáticamente entre estilos en una población "
        "definida: los nadadores del ranking mundial de World Aquatics con marca en ambas "
        "piscinas durante la temporada 2024. La pregunta no cambió tras la "
        "retroalimentación de la formulación.", P))

    # ---------------------------------------------------- 3. datos
    E.append(Paragraph("3. Los datos", H1))
    E.append(Paragraph(
        "La fuente es la API pública de rankings de World Aquatics "
        "(<font face='Courier' size='9'>api.worldaquatics.com/fina/rankings/swimming</font>). "
        "Se descargó el ranking de cada mes de 2024 para 12 pruebas × 2 sexos × 2 "
        "piscinas, 576 consultas en total. Pedir el año completo no servía: la API no "
        "pagina y devuelve como máximo 5.000 filas por consulta, de modo que en las "
        "pruebas más pobladas el ranking quedaba cortado. La descarga mensual entrega "
        "424.528 nados de 71.514 nadadores de 215 países.", P))
    E.append(Paragraph(
        "<b>La unidad de análisis es el par.</b> Cada par cruza a un nadador consigo "
        "mismo: su mejor marca del año en piscina de 50 m contra la suya en 25 m, en la "
        "misma prueba y temporada. Ese diseño dentro-nadador elimina el talento, la edad "
        "y el entrenamiento sin necesidad de controlarlos estadísticamente. El cruce se "
        "validó como uno a uno. Resultan <b>43.914 pares</b> de 14.639 nadadores, con un "
        "mínimo de 570 pares en la prueba menos representada. Se usa la mejor marca y no "
        "la mediana del año porque una marca mínima se cumple con un solo nado. La "
        "tabla 1 resume las variables construidas sobre cada par y la tabla 2, los "
        "problemas de calidad encontrados y cómo se resolvieron.", P))
    E.append(KeepTogether([
        Paragraph("Tabla 1. Variables construidas y usadas en el análisis.", H2),
        tabla([
        ["Variable", "Tipo", "Unidad", "Definición"],
        ["factor", "continua", "adimensional", "t(50 m) / t(25 m) entre las mejores marcas"],
        ["diferencia_s", "continua", "segundos", "t(50 m) − t(25 m)"],
        ["vueltas_extra", "discreta", "vueltas", "distancia / 50"],
        ["por_vuelta_s", "continua", "s por vuelta", "diferencia_s / vueltas_extra"],
        ["estilo", "categórica", "5 niveles", "libre, espalda, pecho, mariposa, combinado"],
        ["sexo", "categórica", "2 niveles", "masculino, femenino"],
        ["distancia", "discreta", "metros", "50, 100, 200, 400"],
    ], [3.2*cm, 2.1*cm, 2.4*cm, 8.6*cm])]))
    E.append(Spacer(1, 8))
    E.append(KeepTogether([
        Paragraph("Tabla 2. Problemas de calidad detectados y decisión adoptada.", H2),
        tabla([
        ["Problema", "Magnitud", "Decisión"],
        ["El campo club trae el literal \"No\"", "18,2% de las filas",
         "Faltante disfrazado: pasa a nulo. No se usa en el análisis"],
        ["Edades imposibles (4 a 119 años)", "389 registros",
         "Pasan a nulo; la fila se conserva porque el tiempo es válido"],
        ["medalla y record casi siempre nulos", "93% y 99%",
         "No son faltantes: el nulo significa «no aplica». No se imputan"],
        ["Un nadador con varios registros", "115.456 filas",
         "Esperable con ranking mensual: se conserva su mejor marca del año"],
        ["Tiempos implausibles", "~24 nados",
         "Se conservan. El corte descartaba nadadores de 5 a 7 años que "
         "probablemente son reales: recortaría la muestra, no la limpiaría"],
        ["Pares con la piscina de 50 m más rápida", "5.950 (13,5%)",
         "Se conservan: recortar una sola cola subiría el factor artificialmente"],
    ], [5.0*cm, 2.9*cm, 8.4*cm])]))
    E.append(Spacer(1, 6))
    E.append(Paragraph(
        "Los términos legales de World Aquatics prohíben en su sección 3 la extracción "
        "automatizada y la redistribución de sus contenidos. El uso aquí es académico, con "
        "media segundo de pausa entre peticiones y caché local para no repetirlas, y los "
        "datos crudos no se redistribuyen: el repositorio contiene solo tablas agregadas.", P))

    # ---------------------------------------------------- 4. hallazgos
    E.append(Paragraph("4. Análisis exploratorio y hallazgos", H1))

    E.append(Paragraph("4.1 Un factor único no representa a las pruebas", H2))
    E.append(Paragraph(
        "Con todos los nadadores juntos, el factor mediano es 1,0318: en piscina de 50 m "
        "se tarda un 3,2% más. Es el número que usaría una conversión única, y la "
        "figura 2 muestra por qué no sirve. Por prueba y sexo, el factor va de "
        "<b>1,0181</b> en 100 m mariposa femenino a <b>1,0521</b> en 200 m espalda "
        "masculino: la ventaja de la piscina corta es 2,9 veces mayor en una prueba que "
        "en otra, y solo 4 de los 24 intervalos de confianza del 95% contienen el valor "
        "global. Los intervalos se estimaron por bootstrap con 2.000 remuestreos, y no con "
        "la fórmula clásica, porque la distribución del factor tiene curtosis 10,5, muy "
        "lejos de la normalidad que esa fórmula supone. Los de los dos extremos, "
        "[1,0167–1,0195] y [1,0504–1,0537], <b>no se solapan</b>: la diferencia no cabe "
        "dentro del error de muestreo.", P))
    E += figura("4-0_factores_ic.png", 12.6,
                "Figura 2. Factor mediano de cada prueba y sexo con su intervalo de "
                "confianza del 95% (bootstrap, 2.000 remuestreos), frente al factor de "
                "todos los nadadores juntos (línea punteada).")

    E.append(Paragraph("4.2 La ventaja por viraje depende del estilo y de la distancia", H2))
    E.append(Paragraph(
        "La figura 3 lleva la ventaja a la unidad en que se produce: los segundos ganados "
        "por cada vuelta extra. El orden de los estilos —mariposa &lt; libre &lt; "
        "combinado &lt; pecho &lt; espalda— se repite <b>idéntico en hombres y "
        "mujeres</b>, dos poblaciones independientes, lo que indica que responde a la "
        "mecánica del nado y no al ruido de la muestra. Es lo que anticipa la figura 1: "
        "el tramo tras la pared vale más cuanto más lento es el nado en superficie que "
        "reemplaza, y en espalda y pecho ese nado es lento comparado con el deslizamiento "
        "bajo el agua.", P))
    E += figura("4-4_lineas_hipotesis.png", 14.4,
                "Figura 3. Segundos ganados por cada vuelta extra (mediana de cada prueba), "
                "por distancia y estilo. Si cada vuelta valiera lo mismo las líneas serían "
                "planas y estarían superpuestas.")
    E.append(Paragraph(
        "La figura 3 muestra además que los segundos ganados por vuelta crecen con la "
        "distancia en los 10 casos donde hay más de una distancia. El factor, en cambio, "
        "crece solo en 7 de 10: es una razón, y el denominador crece más rápido que la "
        "ventaja acumulada. Conviene distinguir cuál de las dos variables se afirma.", P))

    E.append(Paragraph("4.3 Los hombres se benefician más que las mujeres", H2))
    E.append(Paragraph(
        "En la figura 2, el punto de los hombres queda a la derecha del de las mujeres en "
        "cada una de las <b>12 pruebas comparables, sin una sola excepción</b>, con "
        "diferencias de 0,0059 a 0,0123 —de 0,6 a 1,2 puntos porcentuales—. Las doce "
        "diferencias son significativas con la prueba de Mann-Whitney, elegida por no "
        "suponer normalidad; el mayor de los doce valores p es 7,8 × 10<super>-8</super>. "
        "La figura 4 muestra que no es un efecto de unas pocas pruebas: la distribución "
        "completa del factor de los hombres está desplazada a la derecha, con forma "
        "parecida a la de las mujeres.", P))
    E += figura("4-1_histograma_factor.png", 12.6,
                "Figura 4. Distribución del factor de todos los pares, por sexo, con la "
                "mediana de cada grupo (línea punteada).")
    E.append(Paragraph(
        "Este resultado <b>contradice</b> a Iglesias García et al. (2025), que sobre los "
        "rankings españoles reporta diferencias mínimas por sexo, y <b>coincide</b> con el "
        "análisis de récords de Curl (2014). No sostenemos que ese estudio esté "
        "equivocado: su conclusión no puede darse por general, porque compara 200 "
        "nadadores de un país por categoría de edad contra la élite mundial de una "
        "temporada completa. La implicación práctica es que una tabla de factores de "
        "conversión debería separar hombres de mujeres.", P))

    E.append(Paragraph("4.4 La tabla oficial capta la tendencia, pero se desvía", H2))
    E.append(Paragraph(
        "La razón entre las dos marcas mínimas de cada prueba es la equivalencia que "
        "World Aquatics aplica de hecho (sección 1). Comparada con la medida, la "
        "correlación es <b>0,803</b>: la tabla no es arbitraria, captura la tendencia "
        "por estilo. La figura 5 traduce la diferencia a segundos: en 7 de las 24 "
        "pruebas la brecha es menor a 0,3 s, que para efectos prácticos es ruido.", P))
    E += figura("4-5_barras_brecha_wa.png", 10.4,
                "Figura 5. Diferencia entre la mínima exigida en 50 m y la que resultaría "
                "de convertir la mínima de 25 m con el factor medido, en segundos.")
    E.append(Paragraph(
        "Donde sí se desvía, lo hace de forma inconsistente entre pruebas, con un máximo "
        "de 3,66 s en los 400 m combinado femeninos, y con una inclinación hacia la "
        "piscina corta: <b>16 pruebas resultan más fáciles de clasificar en 25 m contra 8 "
        "en 50 m</b>. La consecuencia práctica para un nadador es que la piscina en la que "
        "le conviene intentar la mínima depende de su prueba.", P))

    E.append(Paragraph("4.5 Una advertencia metodológica: el factor es un cociente", H2))
    E.append(Paragraph(
        "Nuestra mediana es poblacional y las mínimas son de nivel más alto, así que cabe "
        "preguntar si el factor depende del nivel. Medido de forma ingenua parece que sí, "
        "pero es un artefacto: definir «élite» por el tiempo en 50 m da un factor de "
        "1,0269 para el 10% más rápido, y definirla por el de 25 m, 1,0361, sin que "
        "cambie ningún nadador. Es regresión a la media: seleccionar por un lado del "
        "cociente deja el otro libre para variar. Con una definición neutral —el promedio "
        "de ambos percentiles— el 10% superior queda en 1,0321, a 0,0003 de toda la "
        "muestra, y la correlación con el nivel es rho = +0,015: significativa por el "
        "tamaño de la muestra, pero sin importancia práctica. Esa verificación habilita "
        "la comparación de la sección 4.4.", P))

    # ---------------------------------------------------- 5. modelo
    E.append(Paragraph("5. Primer modelo", H1))
    E.append(Paragraph(
        "Se ajustó por mínimos cuadrados, para cada estilo y sexo por separado, el modelo "
        "<b>diferencia_s = β<sub>0</sub> + β<sub>1</sub> · vueltas_extra + error</b>, "
        "donde <b>vueltas_extra</b> es la distancia "
        "dividida en 50, los virajes adicionales de la figura 1. La variable explicada es la diferencia en segundos entre ambas "
        "marcas y la explicativa, el número de virajes adicionales que impone la piscina "
        "corta. La pendiente β<sub>1</sub> es directamente la ventaja por vuelta de ese estilo.", P))
    E += figura("6-1_modelo_pendientes.png", 14.6,
                "Figura 6. Pendiente β<sub>1</sub> estimada para cada estilo y sexo, con su intervalo "
                "de confianza del 95%.")
    E.append(Paragraph(
        "<b>Qué dicen los resultados.</b> La figura 6 muestra que β<sub>1</sub> va de 0,98 s por vuelta en libre femenino a "
        "1,86 s en espalda masculino. Los intervalos de libre y de espalda no se rozan, de "
        "modo que la diferencia entre estilos no es ruido muestral, y los hombres superan "
        "a las mujeres en los cinco estilos. Sobre las 24 pruebas juntas, β<sub>1</sub> = 1,2100 s "
        "por vuelta con intervalo [1,1935–1,2265].", P))
    E.append(Paragraph(
        "<b>El intercepto.</b> β<sub>0</sub> = −0,41 s con intervalo [−0,46; −0,35], que no incluye "
        "el cero. Si las vueltas extra explicaran toda la diferencia, el modelo debería "
        "pasar por el origen: sin vueltas adicionales, ninguna diferencia. Como ningún "
        "nado de la muestra tiene cero vueltas extra —el mínimo es una, en los 50 m—, ese "
        "valor es una extrapolación y no se interpreta literalmente; lo que indica es que "
        "una relación puramente proporcional no ajusta y que hay un segundo mecanismo en "
        "juego, probablemente la salida o el desgaste distinto entre calendarios. El "
        "resultado no es igual de firme en todos los ajustes: por estilo y sexo, β<sub>0</sub> "
        "es negativo en los diez, pero en espalda y pecho femeninos su intervalo incluye "
        "el cero.", P))
    E.append(Paragraph(
        "<b>Un resultado que el análisis exploratorio no mostraba.</b> Medida por vuelta, "
        "mariposa gana más que libre (1,28 y 1,43 s contra 0,98 y 1,13), al revés de lo "
        "que indica el factor, donde mariposa es el estilo más bajo. No es una "
        "contradicción: el factor divide esa ventaja por un tiempo total que en mariposa "
        "es mayor. La conclusión depende de la unidad en que se mida, y conviene "
        "explicitarla.", P))
    E.append(Paragraph(
        "<b>Qué no permite concluir.</b> El R<super>2</super> va de 0,13 a 0,37 según el estilo, y es "
        "bajo a propósito: hay mucha variación entre nadadores de una misma prueba. El "
        "modelo describe el comportamiento promedio de la población, no predice a un "
        "nadador concreto — y ese promedio sí lo estima con precisión, como muestran los "
        "intervalos estrechos de la figura 6. Además, se trata de una asociación y no de "
        "una relación causal: el modelo cuantifica cuánta diferencia hay por vuelta extra, "
        "no demuestra que el viraje sea lo único que la produce. El intercepto distinto de "
        "cero es precisamente la señal de que hay algo más.", P))

    # ---------------------------------------------------- 6. limitaciones
    E.append(Paragraph("6. Limitaciones y próximos pasos", H1))
    E.append(Paragraph(
        "<b>La muestra no es aleatoria.</b> Son los mejores de cada ranking mensual, así "
        "que todo lo anterior describe a la élite competitiva y no a la población de "
        "nadadores. La mediana de edad es 17 años, porque el ranking mezcla campeonatos "
        "nacionales y juveniles con la élite adulta.", P))
    E.append(Paragraph(
        "<b>La forma del nadador varía entre calendarios.</b> Las temporadas de piscina "
        "corta y larga son distintas, y un nadador puede llegar en mejor estado a una que "
        "a la otra. El diseño dentro-nadador promedia ese efecto sobre miles de casos pero "
        "no lo elimina; es el origen del 13,5% de pares en que la piscina de 50 m resultó "
        "más rápida.", P))
    E.append(Paragraph(
        "<b>Una sola temporada y sin filtrar tiempos implausibles.</b> El análisis cubre "
        "2024; ampliarlo es cuestión de editar la lista de años del script de descarga. "
        "Los tiempos que podrían ser errores de registro se conservaron deliberadamente, "
        "porque el criterio de corte descartaba sobre todo a nadadores muy jóvenes que "
        "probablemente son reales.", P))
    E.append(Paragraph(
        "<b>Las observaciones no son del todo independientes.</b> Un nadador que compite "
        "en 100 y 200 espalda aporta dos filas correlacionadas, de modo que los errores "
        "estándar reportados son algo optimistas. Con el tamaño de muestra disponible eso "
        "no altera las conclusiones, pero conviene agrupar los errores por nadador.", P))
    E.append(Paragraph(
        "<b>Próximos pasos.</b> (i) Prueba de hipótesis formal para la brecha entre sexos; "
        "(ii) regresión regularizada con validación cruzada, para comprobar que las "
        "conclusiones no dependen de las pruebas con menos pares; (iii) varias temporadas, "
        "para separar el efecto del calendario del efecto de la piscina; (iv) los "
        "parciales por vuelta, que la API no entrega en el ranking, para medir "
        "directamente cuánto regala cada viraje en vez de inferirlo del total.", P))

    # ---------------------------------------------------- 7. reproducibilidad
    E.append(Paragraph("7. Reproducibilidad y uso de inteligencia artificial", H1))
    E.append(Paragraph(
        "El código está en "
        "<font face='Courier' size='9'>github.com/fleivadiaz/capstone-natacion</font>, "
        "con acceso de lectura público. El README documenta el orden de ejecución. Los "
        "datos crudos no se versionan por los términos de uso de la fuente; el repositorio "
        "contiene las tablas agregadas y los scripts que las generan.", P))
    E.append(Paragraph(
        "Se usó Claude (Anthropic) y ChatGPT (OpenAI) para explorar la documentación de la "
        "API, discutir el diseño del análisis y revisar código. Los datos, las decisiones "
        "metodológicas y la interpretación son de los autores, que pueden explicar cada "
        "parte de lo entregado.", P))

    # ---------------------------------------------------- bibliografia
    E.append(Paragraph("Bibliografía", H1))
    E.append(Paragraph(
        "Curl, R. (2014). <i>Short course vs. long course conversion</i>. "
        "coachrickswimming.com. Análisis de récords por estilo.", BIB))
    E.append(Paragraph(
        "Iglesias García, J., Hermosilla-Perona, F., Gonjo, T. y Juárez Santos-García, D. "
        "(2025). Impact of course length on swimming performance across age groups and "
        "swimming strokes. <i>Frontiers in Sports and Active Living</i>. "
        "https://doi.org/10.3389/fspor.2025.1631870", BIB))
    E.append(Paragraph(
        "World Aquatics (2026). <i>Qualification — World Aquatics Swimming Championships "
        "(25m) Beijing 2026</i>. resources.fina.org. Período de clasificación: "
        "27-jul-2025 a 15-nov-2026.", BIB))
    E.append(Paragraph(
        "World Aquatics. <i>Rankings API</i>. api.worldaquatics.com/fina/rankings/swimming. "
        "Temporada 2024, consultada en septiembre de 2026.", BIB))
    E.append(Paragraph(
        "World Aquatics. <i>Legal</i>. worldaquatics.com/legal, sección 3.", BIB))
    E.append(Paragraph(
        "World Aquatics. <i>Swimming Rules</i>, reglas SW 5 a SW 8 (estilos libre, "
        "espalda, pecho y mariposa). worldaquatics.com/rules.", BIB))

    doc.build(E)
    print("Listo:", SALIDA)


if __name__ == "__main__":
    build()
