"""Genera Guion_presentacion_avance.pdf — el guion cronometrado de la presentación
oral del avance, martes 22 de septiembre. El texto se edita ACÁ, no en el PDF."""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                TableStyle, KeepTogether)

SALIDA = "/home/claude/Guion_presentacion_avance.pdf"

OSC = colors.HexColor("#0A3D5C")
NAR = colors.HexColor("#D55E00")
GRIS = colors.HexColor("#5F7480")
TXT = colors.HexColor("#16303D")
CLARO = colors.HexColor("#EDF4F8")

h1 = ParagraphStyle("h1", fontName="Times-Bold", fontSize=19, leading=23,
                    textColor=OSC, spaceAfter=2)
sub = ParagraphStyle("sub", fontName="Helvetica", fontSize=9.5, leading=13,
                     textColor=GRIS, spaceAfter=12)
lam = ParagraphStyle("lam", fontName="Times-Bold", fontSize=12.5, leading=15,
                     textColor=OSC, spaceBefore=10, spaceAfter=1)
reloj = ParagraphStyle("reloj", fontName="Helvetica-Bold", fontSize=8.5, leading=11,
                       textColor=NAR, spaceAfter=4)
cuerpo = ParagraphStyle("cuerpo", fontName="Helvetica", fontSize=9.6, leading=13.4,
                        textColor=TXT, spaceAfter=4, alignment=4)
nota = ParagraphStyle("nota", fontName="Helvetica-Oblique", fontSize=8.6, leading=11.6,
                      textColor=GRIS, spaceAfter=3, leftIndent=10)
seccion = ParagraphStyle("seccion", fontName="Times-Bold", fontSize=14, leading=17,
                         textColor=OSC, spaceBefore=16, spaceAfter=6)
preg = ParagraphStyle("preg", fontName="Helvetica-Bold", fontSize=9.6, leading=13,
                      textColor=OSC, spaceBefore=6, spaceAfter=1)
resp = ParagraphStyle("resp", fontName="Helvetica", fontSize=9.4, leading=12.8,
                      textColor=TXT, spaceAfter=2, alignment=4)

LAMINAS = [
    (1, "¿Es igual de difícil clasificar…?", "Felipe", "0:00", "1:00", 60, [
        "En natación se compite en dos piscinas, de 25 y de 50 metros. La misma prueba en piscina "
        "corta obliga al doble de virajes, y cada viraje regala tiempo: el nadador empuja la pared y "
        "viaja bajo el agua, que es más rápido que nadar en superficie.",
        "La pregunta del proyecto es si esa ventaja vale lo mismo en todas las pruebas. Importa porque "
        "World Aquatics acepta marcas de ambas piscinas para clasificar a un campeonato, pero con dos "
        "tablas de marcas mínimas separadas. La razón entre esas dos exigencias es la equivalencia que "
        "la federación aplica de hecho; si no coincide con la real, clasificar sale más barato en una "
        "piscina que en la otra, y cuánto depende de la prueba.",
        "Lo medimos sobre 43.914 pares de marcas del mismo nadador en las dos piscinas."],
     ["Es la única lámina donde conviene ir lento: si no queda claro qué es un viraje y por qué regala "
      "tiempo, el resto no se sigue."]),

    (2, "Los datos", "Felipe", "1:00", "2:25", 85, [
        "La fuente es la API pública de rankings de World Aquatics, que no pide clave. Pedimos el ranking "
        "de cada mes de 2024: 424 mil nados de 71 mil nadadores de 215 países, más las marcas mínimas del "
        "Mundial de 25 metros de Beijing 2026, transcritas del documento de clasificación.",
        "De ahí construimos la unidad de análisis: 43.914 pares. Un par es la mejor marca del año de un "
        "nadador en cada piscina, en la misma prueba y la misma temporada. Usamos la mejor marca porque "
        "una mínima se cumple con un solo nado. Ese diseño dentro-nadador "
        "elimina el talento, la edad y el entrenamiento sin tener que controlarlos estadísticamente. "
        "El cruce se hizo uno a uno y verificado con conteos, y la prueba con menos pares tiene 570.",
        "A la derecha, la limpieza. Dos faltantes disfrazados: un club literalmente llamado “No”, que "
        "es el centinela de la API, y 389 edades imposibles, porque el ranking mensual mezcla torneos juveniles con élite. En "
        "los dos casos el valor pasa a nulo pero la fila se conserva, porque el tiempo sigue siendo "
        "válido. Los tiempos implausibles se conservan y lo declaramos: filtrarlos recortaría la "
        "muestra en vez de limpiarla. Y un 13,5% de pares donde la piscina larga salió más rápida: no son errores, son "
        "nadadores en distinta forma en cada calendario, y los conservamos porque recortar una sola "
        "cola subiría el factor artificialmente.",
        "Declaramos además los términos de uso de la fuente: uso académico, con pausa entre peticiones "
        "y caché local, y sin redistribuir los datos crudos."],
     ["Es la lámina más densa. Si van atrasados, la limpieza se resume en una frase: “dos faltantes "
      "disfrazados, los repetidos del ranking mensual, y un 13,5% de pares al revés que conservamos”."]),

    (3, "El factor no es una constante", "Javier", "2:25", "3:45", 80, [
        "Primer hallazgo. En el eje vertical, los segundos que gana un nadador por cada vuelta extra; "
        "en el horizontal, la distancia de la prueba.",
        "Si cada vuelta valiera lo mismo, estas líneas serían planas y estarían una encima de otra. No "
        "lo están: espalda y pecho van arriba, mariposa abajo, y todas suben con la distancia.",
        "El detalle que más nos convenció es que el orden de los estilos es idéntico en los dos "
        "paneles. Que el mismo patrón se repita en dos poblaciones independientes indica que responde "
        "a la mecánica del nado y no al ruido de la muestra. Y tiene sentido físico: en espalda y "
        "pecho el nado en superficie es lento comparado con el deslizamiento bajo el agua después de "
        "la pared, así que cada viraje regala más.",
        "El factor va de 1,0181 en 100 mariposa femenino a 1,0521 en 200 espalda masculino: la ventaja "
        "es 2,9 veces mayor en una prueba que en otra.",
        "Y no es una diferencia de muestreo: calculamos por bootstrap el intervalo del 95 por ciento de "
        "los 24 factores, y los de esos dos extremos —de 1,0167 a 1,0195 y de 1,0504 a 1,0537— ni se "
        "acercan."],
     ["Distinción fina, por si preguntan: los segundos por vuelta crecen con la distancia en los 10 "
      "casos, pero el factor —que es una razón— crece solo en 7 de 10, porque el denominador también "
      "crece."]),

    (4, "Los hombres ganan más con la piscina corta", "Javier", "3:45", "5:05", 80, [
        "Segundo hallazgo. Las dos distribuciones tienen la misma forma y están desplazadas: la de los "
        "hombres, a la derecha.",
        "Comparamos prueba por prueba con Mann-Whitney, que no supone normalidad, porque en la sección "
        "descriptiva ya habíamos medido colas muy pesadas. El resultado es unánime: los hombres tienen "
        "mayor factor en las doce pruebas comparables, con diferencias de seis décimas a un punto y "
        "dos décimas porcentuales, y las doce son significativas.",
        "Este es el hallazgo más citable del proyecto, porque contradice al estudio más reciente que "
        "encontramos: Iglesias García y otros, de este año, que con los rankings españoles reporta "
        "diferencias mínimas por sexo.",
        "No decimos que ese estudio esté equivocado. Decimos que su conclusión no se puede dar por "
        "general: son 200 nadadores de un país por categoría de edad contra la élite mundial de una "
        "temporada completa. Y que, por lo tanto, una tabla de factores debería separar hombres de "
        "mujeres."],
     ["El encuadre acordado es ese: “no se puede dar por general”, no “está mal”.",
      "Si piden el valor p exacto: el mayor de los doce es 7,8 por diez a la menos ocho."]),

    (5, "Lo medido contra lo que exige la federación", "Javier", "5:05", "6:30", 85, [
        "Tercer hallazgo, y el que vuelve a la pregunta inicial. World Aquatics no publica un factor de "
        "conversión, pero sí dos tablas de marcas mínimas, una por tipo de piscina, y la razón entre "
        "esas dos exigencias es la equivalencia que aplica de hecho.",
        "Con cuidado en la lectura. La correlación de 0,803 dice que la tabla no es arbitraria: captura "
        "bien la tendencia por estilo, y en 7 de las 24 pruebas la diferencia es menor a tres décimas de "
        "segundo, que para efectos prácticos es ruido. Pero 16 pruebas salen más baratas en piscina "
        "corta contra 8 en larga, así que acá sí hay una inclinación, no solo dispersión.",
        "Lo que sí muestran los datos es que la tabla se desvía de forma inconsistente entre pruebas, "
        "con casos como los 400 combinado femeninos, donde la diferencia llega a 3,7 segundos.",
        "La consecuencia práctica para un nadador es concreta: la piscina en la que le conviene "
        "intentar la mínima depende de su prueba."],
     ["No decir “la tabla está mal calibrada”: la correlación de 0,803 lo desmiente. Lo defendible es "
      "“se desvía de forma inconsistente en un subconjunto de pruebas”."]),

    (6, "El primer modelo", "Felipe", "6:30", "8:20", 110, [
        "Este es el primer modelo ajustado. Regresamos la diferencia de tiempo entre piscinas sobre las "
        "vueltas extra —que es la distancia dividida en cincuenta— por mínimos cuadrados, para cada "
        "estilo y sexo por separado. Es la regresión simple de la clase 4, y leemos sus resultados con "
        "los intervalos de confianza de la clase 5.",
        "La pendiente es directamente la ventaja por vuelta de ese estilo, y el gráfico la muestra con "
        "su intervalo del 95 por ciento. Va de 0,98 segundos en libre femenino a 1,86 en espalda "
        "masculino. Los intervalos de libre y de espalda ni se rozan, así que la diferencia entre "
        "estilos no es ruido muestral. Y los hombres están por encima de las mujeres en los cinco "
        "estilos, lo mismo que vimos en la lámina anterior por otro camino.",
        "El intercepto es −0,41 segundos y no es cero. Si las vueltas explicaran toda la diferencia, la "
        "recta pasaría por el origen: sin vueltas extra, ninguna diferencia. Como ningún nado tiene "
        "cero vueltas extra, ese número es una extrapolación y no lo leemos literalmente; lo que dice "
        "es que una relación puramente proporcional no ajusta, y que hay un segundo mecanismo en juego "
        "—probablemente la salida, o el desgaste distinto entre calendarios.",
        "Y aparece algo que el análisis exploratorio no había mostrado: medida por vuelta, mariposa "
        "gana más que libre, al revés de lo que dice el factor. No es una contradicción. El factor "
        "divide esa ventaja por el tiempo total, y en mariposa el tiempo total es mayor, así que la "
        "misma ventaja pesa menos en proporción.",
        "Una advertencia que corresponde hacer: esto es una asociación, no una causa. El modelo mide "
        "cuánta diferencia hay por vuelta extra, no que la vuelta sea lo único que la produce."],
     ["Es la lámina obligatoria del enunciado y la más larga. No la apuren.",
      "Si preguntan por el R², que va de 0,13 a 0,37 según el estilo: es bajo a propósito, porque hay "
      "mucha variación entre nadadores. El modelo describe el promedio de la población, no predice a "
      "un nadador concreto."]),

    (7, "Dos cosas que revisamos de nuestro propio análisis", "Felipe", "8:20", "9:20", 60, [
        "Dos cuidados que salieron de revisar nuestros propios números.",
        "El primero: el factor es un cociente, y eso es una trampa. Si uno define “élite” mirando solo "
        "uno de los dos lados, la correlación que aparece es un artefacto: seleccionar a alguien por su "
        "buen tiempo en 50 elige a quien tuvo una buena temporada larga, y su tiempo en 25, que no se "
        "usó para elegirlo, queda relativamente más lento. Es regresión a la media, y mueve la mediana "
        "casi un punto porcentual sin que cambie ningún nadador. Con la definición neutral la mediana queda "
        "a tres diezmilésimas del total: sigue siendo significativa por el tamaño de la muestra, pero "
        "deja de importar, y eso es lo que nos habilita a compararla con una tabla de mínimas de nivel "
        "más alto.",
        "El segundo: el ranking mensual nos da varias marcas del mismo nadador en la temporada, así que "
        "hubo que decidir cuál entra al cociente. Con la mejor marca el factor da 1,0318 y con la "
        "mediana del año, 1,0354. La diferencia no es simétrica, porque en piscina larga la mayoría "
        "tiene dos o más registros y en corta uno solo, de modo que la mediana castiga sobre todo al "
        "numerador. Vamos con la mejor marca, que es con la que se cumple una mínima, y dejamos la "
        "mediana como análisis de sensibilidad."],
     ["Esta lámina se adelanta a la pregunta “¿y cuán robusto es esto?”. Si ya la hicieron antes, "
      "respóndanla acá y acorten."]),

    (8, "Limitaciones y lo que viene", "Javier", "9:20", "10:00", 40, [
        "Las limitaciones. La muestra son los mejores de cada ranking, no es aleatoria: describe a la "
        "élite competitiva. Un nadador puede estar en distinta forma en cada calendario, y el diseño "
        "dentro-nadador lo promedia sobre miles de casos pero no lo elimina. Es un solo año, y los "
        "tiempos implausibles se conservan. Y el modelo es una asociación, no una causa.",
        "Lo que viene: el informe del viernes, con el modelo y el análisis de sensibilidad; la prueba de "
        "hipótesis formal para la brecha entre sexos, con lo de la clase 5; y una regresión "
        "regularizada con lo de la clase 7. Más adelante, varias temporadas, para separar el efecto del calendario del "
        "efecto de la piscina.",
        "Quedamos atentos a sus preguntas."],
     ["Si van pasados de los 10 minutos, esta lámina se dice en tres frases y se cierra."]),
]

PREGUNTAS = [
    ("¿Por qué el intercepto no es cero? ¿No debería serlo?",
     "Debería, si las vueltas extra explicaran toda la diferencia: sin vueltas extra, ninguna "
     "diferencia. Nos da −0,41 segundos con un intervalo que no incluye el cero. Pero ningún nado de "
     "la muestra tiene cero vueltas extra —el mínimo es una, en los 50 metros—, así que el intercepto "
     "es extrapolación y no lo interpretamos literalmente. Lo que sí dice es que una recta "
     "proporcional no ajusta, y eso apunta a un segundo mecanismo: la salida, o el desgaste distinto "
     "entre calendarios."),
    ("El R² es bajo. ¿Sirve el modelo?",
     "Va de 0,13 a 0,37 según el estilo, y es bajo porque hay mucha variación entre nadadores dentro "
     "de una misma prueba. El modelo no pretende predecir a un nadador concreto: estima cuánto vale "
     "una vuelta en promedio, y eso lo estima con precisión —los intervalos de la pendiente son "
     "angostos, de unas décimas."),
    ("Un mismo nadador aparece en varias pruebas. ¿Son observaciones independientes?",
     "No del todo, y es una limitación real: un nadador que compite en 100 y 200 espalda aporta dos "
     "filas correlacionadas, así que los errores estándar que reportamos son algo optimistas. Con la "
     "cantidad de pares que tenemos no cambia las conclusiones, pero para el informe podemos agrupar "
     "los errores por nadador."),
    ("¿Por qué ajustaron un modelo por estilo en vez de uno solo con todas las variables?",
     "Hicimos las dos cosas. El modelo con dummies e interacción, que es lo de la clase 4, da lo "
     "mismo: cada estilo gana significativamente más por vuelta que libre, que es la categoría base. "
     "Lo presentamos separado porque la pendiente de cada estilo se lee directamente, sin tener que "
     "sumar coeficientes."),
    ("¿Por qué Mann-Whitney y no una prueba t?",
     "Porque medimos la forma antes de elegir la prueba: las distribuciones tienen curtosis muy alta y "
     "colas pesadas. Mann-Whitney no supone normalidad y compara medianas, que es el resumen que "
     "venimos usando en todo el análisis."),
    ("Con 44 mil pares, todo les va a salir significativo.",
     "Exacto, y por eso no reportamos solo el valor p. La brecha entre sexos la damos en puntos "
     "porcentuales —de 0,6 a 1,2— y el efecto del nivel lo descartamos por tamaño: con criterio neutral "
     "es significativo pero mueve la mediana tres diezmilésimas. Significativo no es importante."),
    ("¿La muestra es representativa de los nadadores?",
     "No, y lo declaramos: son los mejores de cada ranking, no una muestra aleatoria. Todo lo que "
     "decimos describe a la élite competitiva. Lo que sí verificamos, en la lámina 7, es que dentro de "
     "esa población el factor no depende del nivel, y eso es lo que nos permite compararla con las "
     "marcas mínimas."),
    ("¿Por qué conservan los pares donde la piscina de 50 m salió más rápida?",
     "Porque son reales: la temporada de piscina corta y la de larga son calendarios distintos y un "
     "nadador puede estar en forma en uno y no en el otro. Recortar solo esa cola —y no la otra— "
     "subiría el factor artificialmente. Lo declaramos como limitación."),
    ("¿No tienen problemas con los términos de uso de World Aquatics?",
     "Los declaramos en la formulación y en el notebook. El uso es académico, con medio segundo de "
     "pausa entre peticiones y caché local para no repetirlas, y no redistribuimos los datos crudos: "
     "el repositorio solo lleva las tablas agregadas, que son estadísticas por prueba."),
    ("¿Por qué un solo año?",
     "Es una limitación declarada y es ampliable: basta editar la lista de años en el script de "
     "descarga. Preferimos cerrar bien una temporada antes de sumar más."),
    ("¿Y qué harían distinto si tuvieran más tiempo?",
     "Dos cosas: varias temporadas, para separar el efecto del calendario del efecto de la piscina; y "
     "usar los parciales por vuelta, que la API no entrega en el ranking, para medir directamente "
     "cuánto regala cada viraje en vez de inferirlo del total."),
]

NO_DECIR = [
    ("“La tabla de World Aquatics está mal calibrada.”",
     "La correlación de 0,803 dice lo contrario. Lo defendible es: <b>se desvía de forma inconsistente "
     "en un subconjunto de pruebas</b>."),
    ("“El efecto del nivel del nadador desaparece.”",
     "Con la definición neutral <b>cae hasta volverse irrelevante</b>, que no es lo mismo: la correlación "
     "es +0,015 y sigue siendo significativa por el tamaño de la muestra, pero mueve la mediana tres "
     "diezmilésimas. Y sí existe cuando el nivel se define por un solo lado — esa es la advertencia."),
    ("“El modelo demuestra que las vueltas causan la diferencia.”",
     "Es una asociación. Lo que el modelo mide es <b>cuánta diferencia hay por vuelta extra</b>, no que "
     "la vuelta sea lo único que la produce. El intercepto distinto de cero es precisamente la señal "
     "de que hay algo más."),
    ("“Mariposa es el estilo donde la piscina corta importa menos.”",
     "Depende de la medida, y conviene decir cuál: <b>en factor</b> sí es la más baja; <b>en segundos "
     "por vuelta</b> gana más que libre. El factor divide por un tiempo total mayor."),
]


def build():
    doc = SimpleDocTemplate(SALIDA, pagesize=A4,
                            leftMargin=2.0 * cm, rightMargin=2.0 * cm,
                            topMargin=1.7 * cm, bottomMargin=1.7 * cm,
                            title="Guion — presentación de avance del Capstone",
                            author="Felipe Leiva · Javier Fuentes")
    E = []
    E.append(Paragraph("Guion de la presentación de avance", h1))
    E.append(Paragraph(
        "Capstone de natación &middot; Felipe Leiva y Javier Fuentes &middot; martes 22 de septiembre "
        "de 2026 &middot; <b>10 minutos, 8 láminas</b>. El enunciado exige que los dos integrantes "
        "participen y recomienda un máximo de 8 slides; el reparto de abajo respeta las dos cosas y "
        "cambia de expositor siempre en un quiebre de tema. Las slides en PDF se suben al aula virtual "
        "<b>antes del inicio de la clase</b>.", sub))

    filas = [["#", "Lámina", "Quién", "Desde", "Dura"]]
    for n, t, q, d, h, seg, _, _ in LAMINAS:
        filas.append([str(n), t, q, d, f"{seg}s"])
    tab = Table(filas, colWidths=[0.8 * cm, 8.6 * cm, 2.2 * cm, 2.0 * cm, 1.6 * cm])
    tab.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 8.6),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("BACKGROUND", (0, 0), (-1, 0), OSC),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, CLARO]),
        ("TEXTCOLOR", (0, 1), (-1, -1), TXT),
        ("ALIGN", (0, 0), (0, -1), "CENTER"),
        ("ALIGN", (2, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 3.5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3.5),
        ("LINEBELOW", (0, 0), (-1, 0), 0.6, OSC),
    ]))
    E.append(tab)
    E.append(Spacer(1, 6))
    E.append(Paragraph(
        "Los tiempos suman exactamente 10:00 sin margen, y el enunciado dice que el tiempo se controla. "
        "En la práctica conviene apuntar a 9:15 hablando: las láminas 7 y 8 son las que se comprimen si "
        "van atrasados, y la 6 —el modelo, que es obligatorio— es la que no hay que apurar.", nota))

    E.append(Paragraph("Lámina por lámina", seccion))
    for n, t, q, d, h, seg, parrafos, notas in LAMINAS:
        bloque = [Paragraph(f"{n} &middot; {t}", lam),
                  Paragraph(f"{d} – {h}  ·  {seg} segundos  ·  habla {q}", reloj)]
        for p in parrafos:
            bloque.append(Paragraph(p, cuerpo))
        for x in notas:
            bloque.append(Paragraph("&raquo; " + x, nota))
        E.append(KeepTogether(bloque))

    E.append(Paragraph("Preguntas probables", seccion))
    E.append(Paragraph(
        "Ordenadas por probabilidad. Las tres primeras son sobre el modelo, que es lo que el enunciado "
        "pide de manera explícita y lo más nuevo de esta entrega.", nota))
    for p, r in PREGUNTAS:
        E.append(KeepTogether([Paragraph(p, preg), Paragraph(r, resp)]))

    E.append(Paragraph("Cuatro frases que conviene no decir", seccion))
    for mal, bien in NO_DECIR:
        E.append(KeepTogether([Paragraph(mal, preg), Paragraph(bien, resp)]))

    doc.build(E)
    print("Listo:", SALIDA)


if __name__ == "__main__":
    build()
