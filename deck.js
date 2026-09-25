const pptxgen = require("pptxgenjs");
const pres = new pptxgen();
pres.layout = "LAYOUT_16x9";           // 10" x 5.625"
pres.author = "Felipe Leiva · Javier Fuentes";
pres.title = "Capstone natación — avance";

const OSC   = "0A3D5C";
const AZUL  = "0072B2";
const NAR   = "D55E00";
const VERDE = "009E73";
const AMAR  = "E69F00";
const TXT   = "16303D";
const GRIS  = "5F7480";
const CLARO = "EDF4F8";
const BCO   = "FFFFFF";

const H1 = "Cambria";
const BODY = "Calibri";
const FIG = "/mnt/user-data/uploads/diplomado-cdd/capstone/figuras_eda";

function titulo(s, t, sub) {
  s.addText(t, { x: 0.55, y: 0.30, w: 8.9, h: 0.62, isTextBox: true, margin: 0,
    fontFace: H1, fontSize: 27, bold: true, color: OSC });
  if (sub) {
    s.addText(sub, { x: 0.55, y: 0.93, w: 8.9, h: 0.38, isTextBox: true, margin: 0,
      fontFace: BODY, fontSize: 13, color: GRIS });
  }
}
function stat(s, x, y, w, h, num, lab, color) {
  s.addShape(pres.ShapeType.roundRect, { x, y, w, h, rectRadius: 0.06,
    fill: { color: CLARO }, line: { color: CLARO } });
  s.addText(num, { x: x + 0.12, y: y + 0.09, w: w - 0.24, h: h * 0.54, isTextBox: true, margin: 0,
    fontFace: H1, fontSize: 24, bold: true, color: color || OSC });
  s.addText(lab, { x: x + 0.12, y: y + h * 0.57, w: w - 0.24, h: h * 0.40, isTextBox: true, margin: 0,
    fontFace: BODY, fontSize: 10, color: GRIS });
}
function tarjeta(s, x, y, w, h, fill) {
  s.addShape(pres.ShapeType.roundRect, { x, y, w, h, rectRadius: 0.05,
    fill: { color: fill || CLARO }, line: { color: fill || CLARO } });
}

// =====================================================================
// 1 · EL PROBLEMA Y LA PREGUNTA
// =====================================================================
let s1 = pres.addSlide();
s1.background = { color: OSC };
s1.addText("Diplomado en Ciencia de Datos Aplicada · UTFSM · Módulo 1 · Avance del proyecto",
  { x: 0.55, y: 0.45, w: 8.9, h: 0.3, isTextBox: true, margin: 0,
    fontFace: BODY, fontSize: 11, color: "9FC4D6", charSpacing: 0.6 });
s1.addText("¿Es igual de difícil clasificar nadando\nen piscina de 25 metros que en una de 50?",
  { x: 0.55, y: 1.05, w: 8.9, h: 1.35, isTextBox: true, margin: 0,
    fontFace: H1, fontSize: 32, bold: true, color: BCO, lineSpacingMultiple: 1.05 });
s1.addText("En piscina corta se dan el doble de vueltas, y cada vuelta regala tiempo. World Aquatics acepta marcas de las dos piscinas para clasificar, con dos tablas de mínimas distintas. Si esas exigencias no son equivalentes, clasificar sale más barato en una piscina que en la otra.",
  { x: 0.55, y: 2.55, w: 5.5, h: 1.20, isTextBox: true, margin: 0,
    fontFace: BODY, fontSize: 13, color: "CFE3EE", lineSpacingMultiple: 1.15 });

s1.addShape(pres.ShapeType.roundRect, { x: 6.35, y: 2.50, w: 3.1, h: 1.32, rectRadius: 0.06,
  fill: { color: "0F4E72" }, line: { color: "0F4E72" } });
s1.addText("43.914", { x: 6.55, y: 2.60, w: 2.7, h: 0.60, isTextBox: true, margin: 0,
  fontFace: H1, fontSize: 33, bold: true, color: BCO });
s1.addText("pares de marcas del mismo nadador\nen las dos piscinas, temporada 2024",
  { x: 6.55, y: 3.20, w: 2.7, h: 0.54, isTextBox: true, margin: 0,
    fontFace: BODY, fontSize: 10, color: "9FC4D6", lineSpacingMultiple: 1.1 });

s1.addText("Felipe Leiva  ·  Javier Fuentes", { x: 0.55, y: 4.40, w: 5.5, h: 0.3, isTextBox: true, margin: 0,
  fontFace: BODY, fontSize: 13, bold: true, color: BCO });
s1.addText("Martes 22 de septiembre de 2026", { x: 0.55, y: 4.72, w: 5.5, h: 0.3, isTextBox: true, margin: 0,
  fontFace: BODY, fontSize: 11, color: "9FC4D6" });
s1.addNotes("En natación se compite en dos piscinas, de 25 y de 50 metros. La misma prueba en piscina corta obliga al doble de virajes, y cada viraje regala tiempo: el nadador empuja la pared y viaja bajo el agua, que es más rápido que nadar en superficie. La pregunta es si esa ventaja vale lo mismo en todas las pruebas. Importa porque World Aquatics acepta marcas de ambas piscinas para clasificar a un campeonato, pero con dos tablas de marcas mínimas separadas: la razón entre esas dos exigencias es la equivalencia que la federación aplica de hecho. Lo medimos sobre 43.914 pares de marcas del mismo nadador en las dos piscinas.");

// =====================================================================
// 2 · LOS DATOS
// =====================================================================
let s2 = pres.addSlide();
titulo(s2, "Los datos", "Ranking mensual de la API pública de World Aquatics, temporada 2024, más las marcas mínimas oficiales del Mundial de 25 m de Beijing 2026.");

const nums = [
  ["424.528", "nados · 25 columnas", OSC],
  ["71.514", "nadadores, 215 países", OSC],
  ["43.914", "pares 25 m ↔ 50 m", NAR],
  ["570", "pares en la prueba más chica", OSC],
];
nums.forEach(([n, l, c], i) => stat(s2, 0.55 + i * 2.27, 1.45, 2.10, 0.98, n, l, c));

tarjeta(s2, 0.55, 2.68, 4.35, 2.05);
s2.addText("Cada nadador contra sí mismo", { x: 0.75, y: 2.80, w: 3.95, h: 0.28, isTextBox: true, margin: 0,
  fontFace: H1, fontSize: 14, bold: true, color: OSC });
s2.addText([
  { text: "factor = tiempo en 50 m / tiempo en 25 m", options: { bold: true, color: AZUL, breakLine: true } },
  { text: "Comparamos la mejor marca del año de un nadador con la suya propia en la otra piscina, misma prueba y misma temporada. Eso deja fuera el talento, la edad y el entrenamiento sin tener que controlarlos. Es la mejor marca porque una mínima se cumple con un solo nado.", options: {} },
], { x: 0.75, y: 3.12, w: 3.95, h: 1.50, isTextBox: true, margin: 0, valign: "top",
  fontFace: BODY, fontSize: 10.5, color: TXT, lineSpacingMultiple: 1.12 });

tarjeta(s2, 5.10, 2.68, 4.35, 2.05);
s2.addText("Lo que encontramos al limpiar", { x: 5.30, y: 2.80, w: 3.95, h: 0.28, isTextBox: true, margin: 0,
  fontFace: H1, fontSize: 14, bold: true, color: OSC });
const limp = [
  ["Un club llamado “No”", "centinela de la API en 18,2% de las filas → nulo"],
  ["389 edades imposibles", "de 4 a 119 años; el ranking mensual mezcla torneos juveniles → nulo"],
  ["Un nadador, varios registros", "es lo esperable con ranking mensual → se conserva su mejor marca"],
  ["13,5% de pares al revés", "temporadas distintas, no errores → se conservan"],
];
limp.forEach(([t, d], i) => {
  const y = 3.12 + i * 0.40;
  s2.addText([
    { text: t + "  ", options: { bold: true, color: TXT } },
    { text: d, options: { color: GRIS } },
  ], { x: 5.30, y: y, w: 3.95, h: 0.38, isTextBox: true, margin: 0, valign: "top",
    fontFace: BODY, fontSize: 9.6, lineSpacingMultiple: 1.05 });
});
s2.addText("Fuente: api.worldaquatics.com · Beijing 2026 (resources.fina.org). Uso académico, con pausa entre peticiones y caché; no se redistribuyen los datos crudos.",
  { x: 0.55, y: 4.86, w: 8.9, h: 0.30, isTextBox: true, margin: 0,
    fontFace: BODY, fontSize: 8.5, color: GRIS });
s2.addNotes("La fuente es la API pública de rankings de World Aquatics, que no pide clave: 424 mil nados de 71 mil nadadores de 215 países en la temporada 2024, pedidos mes a mes. De ahí sale la unidad de análisis, que son los 43.914 pares: el mismo nadador con marca en las dos piscinas, misma prueba y misma temporada. Ese diseño dentro-nadador elimina el talento, la edad y el entrenamiento sin tener que controlarlos. La variable central es el factor, el cociente entre ambos tiempos. Usamos la mejor marca del año de cada nadador, porque una marca mínima se cumple con un solo nado. A la derecha, la limpieza: dos faltantes disfrazados —un club llamado No, que es el centinela de la API, y 389 edades imposibles, porque el ranking mensual mezcla torneos juveniles con élite—, los registros repetidos que ese mismo ranking produce, y un trece y medio por ciento de pares donde la piscina larga salió más rápida. Esos últimos no son errores: son nadadores en distinta forma en cada calendario, y los conservamos porque recortar una sola cola subiría el factor artificialmente. Declaramos además los términos de uso: no redistribuimos los datos crudos.");

// =====================================================================
// 3 · HALLAZGO 1
// =====================================================================
let s3 = pres.addSlide();
titulo(s3, "El factor no es una constante", "Segundos que gana un nadador por cada vuelta extra: la mediana de cada prueba, con los dos sexos por separado.");
s3.addImage({ path: `${FIG}/4-4_lineas_hipotesis.png`, x: 0.62, y: 1.38, w: 8.20, h: 3.42 });
s3.addText([
  { text: "Mariposa < Libre < Combinado < Pecho < Espalda", options: { bold: true, color: OSC } },
  { text: "   ·   el mismo orden en los dos paneles. El factor va de 1,0181 a 1,0521 según la prueba, y los intervalos del 95% de esos dos extremos —[1,0167–1,0195] y [1,0504–1,0537]— ni se acercan.", options: { color: GRIS } },
], { x: 0.62, y: 4.84, w: 8.8, h: 0.50, isTextBox: true, margin: 0, valign: "top", fontFace: BODY, fontSize: 11 });
s3.addNotes("Primer hallazgo. En el eje vertical, los segundos que gana un nadador por cada vuelta extra; en el horizontal, la distancia. Si cada vuelta valiera lo mismo, estas líneas serían planas y estarían una encima de otra. No lo están: espalda y pecho van arriba, mariposa abajo, y todas suben con la distancia. Y el orden de los estilos es idéntico en los dos paneles; que el mismo patrón se repita en dos poblaciones independientes indica que responde a la mecánica del nado y no al ruido. Tiene sentido físico: en espalda y pecho el nado en superficie es lento comparado con el deslizamiento bajo el agua después de la pared, así que cada viraje regala más. El factor va de 1,0181 en 100 mariposa femenino a 1,0521 en 200 espalda masculino: la ventaja es 2,9 veces mayor en una prueba que en otra. Y calculamos por bootstrap el intervalo del 95 por ciento de los 24 factores: los de esos dos extremos son 1,0167 a 1,0195 y 1,0504 a 1,0537, así que ni se acercan. La diferencia no cabe dentro del error de muestreo.");

// =====================================================================
// 4 · HALLAZGO 2
// =====================================================================
let s4 = pres.addSlide();
titulo(s4, "Los hombres ganan más con la piscina corta", "Y lo hacen en las doce pruebas comparables, sin una sola excepción.");
s4.addImage({ path: `${FIG}/4-1_histograma_factor.png`, x: 0.50, y: 1.55, w: 5.95, h: 2.68 });

tarjeta(s4, 6.62, 1.42, 2.88, 3.35);
s4.addText("12 de 12", { x: 6.80, y: 1.54, w: 2.55, h: 0.44, isTextBox: true, margin: 0,
  fontFace: H1, fontSize: 25, bold: true, color: NAR });
s4.addText("pruebas con mayor factor en hombres, todas significativas (Mann-Whitney; el mayor de los doce valores p es 7,8e-8).",
  { x: 6.80, y: 1.98, w: 2.55, h: 0.70, isTextBox: true, margin: 0,
    fontFace: BODY, fontSize: 10, color: GRIS, lineSpacingMultiple: 1.1 });
s4.addText("0,6 a 1,2", { x: 6.80, y: 2.72, w: 2.55, h: 0.36, isTextBox: true, margin: 0,
  fontFace: H1, fontSize: 21, bold: true, color: OSC });
s4.addText("puntos porcentuales de diferencia, según la prueba.",
  { x: 6.80, y: 3.08, w: 2.55, h: 0.40, isTextBox: true, margin: 0,
    fontFace: BODY, fontSize: 10, color: GRIS, lineSpacingMultiple: 1.1 });
s4.addText([
  { text: "Contradice ", options: { color: TXT } },
  { text: "a Iglesias García et al. (2025)", options: { bold: true, color: TXT } },
  { text: ", que sobre 200 nadadores españoles por categoría halla diferencias mínimas por sexo, y coincide con el análisis de récords de Curl (2014).", options: { color: TXT } },
], { x: 6.80, y: 3.55, w: 2.55, h: 1.10, isTextBox: true, margin: 0,
  fontFace: BODY, fontSize: 10, lineSpacingMultiple: 1.12 });
s4.addNotes("Segundo hallazgo. Las dos distribuciones tienen la misma forma y están desplazadas: la de los hombres, a la derecha. Comparamos prueba por prueba con Mann-Whitney, que no supone normalidad, porque ya habíamos medido colas muy pesadas. El resultado es unánime: los hombres tienen mayor factor en las doce pruebas comparables, con diferencias de seis décimas a un punto y dos décimas porcentuales. Este es el hallazgo más citable, porque contradice al estudio más reciente que encontramos, de este año, con los rankings españoles. No decimos que ese estudio esté equivocado: decimos que su conclusión no se puede dar por general, porque son doscientos nadadores de un país por categoría de edad contra la élite mundial de una temporada. Y que, por lo tanto, una tabla de factores debería separar hombres de mujeres.");

// =====================================================================
// 5 · HALLAZGO 3
// =====================================================================
let s5 = pres.addSlide();
titulo(s5, "Lo medido contra lo que exige la federación", "La razón entre las dos marcas mínimas de World Aquatics es la equivalencia que la federación aplica de hecho.");
s5.addImage({ path: `${FIG}/4-5_barras_brecha_wa.png`, x: 0.50, y: 1.42, w: 4.04, h: 3.40 });

const notas5 = [
  ["0,803", "es la correlación entre el factor oficial y el medido: la tabla no es arbitraria, captura la tendencia por estilo.", AZUL],
  ["16 contra 8", "pruebas más fáciles de clasificar en 25 m que en 50 m, con una brecha mediana de 0,47 s.", NAR],
  ["3,66 s", "es el caso extremo, los 400 combinado femeninos. En 7 de las 24 pruebas la brecha es menor a 0,3 s, o sea ruido.", NAR],
];
notas5.forEach(([n, t, c], i) => {
  const y = 1.42 + i * 1.10;
  s5.addText(n, { x: 5.10, y: y, w: 4.35, h: 0.36, isTextBox: true, margin: 0,
    fontFace: H1, fontSize: 21, bold: true, color: c });
  s5.addText(t, { x: 5.10, y: y + 0.38, w: 4.35, h: 0.66, isTextBox: true, margin: 0,
    fontFace: BODY, fontSize: 11, color: TXT, lineSpacingMultiple: 1.12 });
});
s5.addText("Para un nadador, la consecuencia práctica es que la piscina en la que conviene intentar la mínima depende de su prueba.",
  { x: 5.10, y: 4.72, w: 4.35, h: 0.52, isTextBox: true, margin: 0,
    fontFace: BODY, fontSize: 11, bold: true, color: OSC, lineSpacingMultiple: 1.1 });
s5.addNotes("Tercer hallazgo, y el que conecta con la pregunta inicial. World Aquatics no publica un factor de conversión, pero sí dos tablas de marcas mínimas, una por tipo de piscina, y la razón entre ambas es la equivalencia que aplica de hecho. Con cuidado en la lectura: la correlación de 0,803 dice que la tabla no es arbitraria, captura bien la tendencia por estilo, y en siete de las veinticuatro pruebas la diferencia es menor a tres décimas de segundo, que es ruido. Pero dieciséis pruebas salen más baratas en piscina corta contra ocho en larga. Lo que sí muestran los datos es que se desvía de forma inconsistente entre pruebas, con casos como los 400 combinado femeninos, donde la diferencia llega a 3,7 segundos. La afirmación que sostenemos es esa, no que la tabla esté mal calibrada.");

// =====================================================================
// 6 · EL PRIMER MODELO
// =====================================================================
let s6 = pres.addSlide();
titulo(s6, "El primer modelo", "diferencia_s = β₀ + β₁ · vueltas_extra + ε, ajustado por mínimos cuadrados para cada estilo y sexo (n = 43.914).");
s6.addImage({ path: `${FIG}/6-1_modelo_pendientes.png`, x: 0.40, y: 1.48, w: 6.14, h: 3.20 });

tarjeta(s6, 6.70, 1.34, 2.80, 3.42);
s6.addText("Qué dice", { x: 6.88, y: 1.44, w: 2.48, h: 0.28, isTextBox: true, margin: 0,
  fontFace: H1, fontSize: 14, bold: true, color: OSC });
s6.addText([
  { text: "β₁ es la ventaja por vuelta.", options: { bold: true, breakLine: true } },
  { text: "Va de 0,98 s en libre femenino a 1,86 s en espalda masculino. Los intervalos de libre y de espalda no se tocan: la diferencia entre estilos no es ruido.", options: { breakLine: true, color: GRIS } },
  { text: "β₀ = −0,41 s, y no es cero.", options: { bold: true, breakLine: true } },
  { text: "Si las vueltas explicaran toda la diferencia, el modelo pasaría por el origen. Como ningún nado tiene cero vueltas extra, no se lee literal: dice que una recta proporcional no ajusta.", options: { color: GRIS } },
], { x: 6.88, y: 1.76, w: 2.48, h: 2.24, isTextBox: true, margin: 0, valign: "top",
  fontFace: BODY, fontSize: 9.8, color: TXT, lineSpacingMultiple: 1.1 });
s6.addText("Y una sorpresa: por vuelta, mariposa gana más que libre — al revés que en el factor, porque el factor divide por un tiempo total mayor.",
  { x: 6.88, y: 4.02, w: 2.48, h: 0.66, isTextBox: true, margin: 0, valign: "top",
    fontFace: BODY, fontSize: 9.8, bold: true, color: NAR, lineSpacingMultiple: 1.1 });
s6.addNotes("Este es el primer modelo. Regresamos la diferencia de tiempo entre piscinas sobre las vueltas extra, que es la distancia dividida en cincuenta, ajustado por mínimos cuadrados para cada estilo y sexo. La pendiente es directamente la ventaja por vuelta de ese estilo, y el gráfico la muestra con su intervalo de confianza del 95 por ciento. Va de 0,98 segundos en libre femenino a 1,86 en espalda masculino, y los intervalos de libre y de espalda ni se rozan: la diferencia entre estilos no es ruido muestral. Los hombres están por encima de las mujeres en los cinco estilos, consistente con el hallazgo anterior. El intercepto es −0,41 segundos y no es cero: si las vueltas explicaran toda la diferencia, la recta pasaría por el origen. Como ningún nado tiene cero vueltas extra, ese número es extrapolación y no lo leemos literalmente; lo que dice es que una relación puramente proporcional no ajusta, y que hay un segundo mecanismo en juego. Y hay una sorpresa: medida por vuelta, mariposa gana más que libre, al revés de lo que dice el factor. No es contradicción: el factor divide esa ventaja por un tiempo total que en mariposa es mayor. Un modelo lineal es una asociación, no una causa; lo que afirmamos es cuánta diferencia hay por vuelta, no que la vuelta sea lo único que la produce.");

// =====================================================================
// 7 · LO QUE HAY QUE CUIDAR
// =====================================================================
let s7 = pres.addSlide();
titulo(s7, "Dos cosas que revisamos de nuestro propio análisis", "Las dos cambian cómo hay que leer el factor, y las dos entran en el informe.");

tarjeta(s7, 0.55, 1.42, 4.35, 3.35);
s7.addText("1 · El factor es un cociente: una trampa", { x: 0.75, y: 1.54, w: 3.95, h: 0.32, isTextBox: true, margin: 0,
  fontFace: H1, fontSize: 14, bold: true, color: OSC });
s7.addText("Definir “élite” mirando uno solo de los dos lados mueve la mediana casi un punto porcentual sin que cambie ningún nadador: es regresión a la media.",
  { x: 0.75, y: 1.94, w: 3.95, h: 0.62, isTextBox: true, margin: 0,
    fontFace: BODY, fontSize: 10.5, color: TXT, lineSpacingMultiple: 1.12 });
const niveles = [
  ["Élite por su tiempo en 50 m", "1,0269"],
  ["Élite por su tiempo en 25 m", "1,0361"],
  ["Élite por el promedio (neutral)", "1,0321"],
  ["Todos los pares", "1,0318"],
];
niveles.forEach(([l, v], i) => {
  const y = 2.72 + i * 0.32;
  s7.addText(l, { x: 0.75, y: y, w: 2.95, h: 0.28, isTextBox: true, margin: 0,
    fontFace: BODY, fontSize: 10.5, color: i === 3 ? GRIS : TXT, italic: i === 3 });
  s7.addText(v, { x: 3.72, y: y, w: 0.98, h: 0.28, isTextBox: true, margin: 0,
    fontFace: BODY, fontSize: 10.5, bold: true, color: i === 3 ? GRIS : OSC, align: "right" });
});
s7.addText("Con la definición neutral la mediana queda a 0,0003 del total: sigue siendo significativa por el tamaño de la muestra, pero deja de importar. Por eso podemos compararla con una tabla de mínimas de nivel más alto.",
  { x: 0.75, y: 4.10, w: 3.95, h: 0.56, isTextBox: true, margin: 0,
    fontFace: BODY, fontSize: 10, color: GRIS, lineSpacingMultiple: 1.1 });

tarjeta(s7, 5.10, 1.42, 4.35, 3.35, "FBEEE5");
s7.addText("2 · Qué marca del año entra en el cociente", { x: 5.30, y: 1.54, w: 3.95, h: 0.32, isTextBox: true, margin: 0,
  fontFace: H1, fontSize: 14, bold: true, color: NAR });
s7.addText("El ranking mensual da varias marcas por nadador y temporada, así que hay que elegir cuál entra. La elección mueve el resultado:",
  { x: 5.30, y: 1.94, w: 3.95, h: 0.52, isTextBox: true, margin: 0, valign: "top",
    fontFace: BODY, fontSize: 10.5, color: TXT, lineSpacingMultiple: 1.12 });
const defs = [["Con la mejor marca del año", "1,0318"], ["Con la mediana del año", "1,0354"]];
defs.forEach(([l, v], i) => {
  const y = 2.56 + i * 0.32;
  s7.addText(l, { x: 5.30, y: y, w: 2.95, h: 0.28, isTextBox: true, margin: 0,
    fontFace: BODY, fontSize: 10.5, color: TXT });
  s7.addText(v, { x: 8.27, y: y, w: 0.98, h: 0.28, isTextBox: true, margin: 0,
    fontFace: BODY, fontSize: 10.5, bold: true, color: NAR, align: "right" });
});
s7.addText("No es neutro: en 50 m la mayoría tiene dos o más registros y en 25 m uno solo, así que la mediana castiga sobre todo al numerador e infla el factor. La diferencia es del mismo orden que la brecha entre sexos.",
  { x: 5.30, y: 3.28, w: 3.95, h: 0.80, isTextBox: true, margin: 0, valign: "top",
    fontFace: BODY, fontSize: 10.5, color: TXT, lineSpacingMultiple: 1.12 });
s7.addText("Vamos con la mejor marca: es la que se usa para clasificar. La mediana queda como análisis de sensibilidad.",
  { x: 5.30, y: 4.14, w: 3.95, h: 0.52, isTextBox: true, margin: 0, valign: "top",
    fontFace: BODY, fontSize: 10.5, bold: true, color: NAR, lineSpacingMultiple: 1.1 });
s7.addNotes("Dos cosas que revisamos de nuestro propio análisis. La primera: el factor es un cociente, y si uno define élite mirando solo uno de los dos lados, la correlación que aparece es un artefacto. Seleccionar a alguien por su buen tiempo en 50 elige a quien tuvo buena temporada larga, y su tiempo en 25, que no se usó para elegirlo, queda relativamente más lento. La mediana se mueve casi un punto porcentual sin que cambie ningún nadador. Con la definición neutral queda a tres diezmilésimas del total: sigue siendo significativa por el tamaño de la muestra, pero deja de importar, y eso es lo que nos habilita a compararla con una tabla de mínimas de nivel más alto. La segunda: el ranking mensual nos da varias marcas por nadador en la misma temporada, así que hubo que decidir cuál entra al cociente. Con la mejor marca el factor da 1,0318 y con la mediana del año 1,0354. La diferencia no es neutra, porque en piscina larga la mayoría tiene dos o más registros y en corta uno solo, de modo que la mediana castiga sobre todo al numerador. Vamos con la mejor marca, que es con la que efectivamente se cumple una mínima, y dejamos la mediana como análisis de sensibilidad.");

// =====================================================================
// 8 · LIMITACIONES Y PRÓXIMOS PASOS
// =====================================================================
let s8 = pres.addSlide();
s8.background = { color: OSC };
s8.addText("Limitaciones y lo que viene", { x: 0.55, y: 0.42, w: 8.9, h: 0.5, isTextBox: true, margin: 0,
  fontFace: H1, fontSize: 26, bold: true, color: BCO });

s8.addText("Qué no permiten decir los datos", { x: 0.55, y: 1.12, w: 4.20, h: 0.3, isTextBox: true, margin: 0,
  fontFace: BODY, fontSize: 12, bold: true, color: "9FC4D6" });
const lim = [
  "La muestra son los mejores de cada ranking, no es aleatoria: describe a la élite competitiva.",
  "Un nadador puede estar en distinta forma en cada calendario; el diseño dentro-nadador lo promedia, no lo elimina.",
  "Un solo año, 2024. Y los tiempos implausibles se conservan: no filtramos, para no recortar la muestra.",
  "El modelo es una asociación, no una causa: mide cuánta diferencia hay por vuelta, no que la vuelta sea lo único que la produce.",
];
lim.forEach((t, i) => {
  const y = 1.50 + i * 0.72;
  s8.addText("—", { x: 0.55, y: y, w: 0.22, h: 0.28, isTextBox: true, margin: 0, valign: "top",
    fontFace: BODY, fontSize: 10.5, bold: true, color: "5FA8CC" });
  s8.addText(t, { x: 0.82, y: y, w: 3.93, h: 0.66, isTextBox: true, margin: 0, valign: "top",
    fontFace: BODY, fontSize: 10.5, color: "CFE3EE", lineSpacingMultiple: 1.1 });
});

s8.addText("Qué sigue", { x: 5.25, y: 1.12, w: 4.20, h: 0.3, isTextBox: true, margin: 0,
  fontFace: BODY, fontSize: 12, bold: true, color: "9FC4D6" });
const sig = [
  ["Informe escrito, viernes 25", "con el modelo por estilo y sexo y el análisis de sensibilidad."],
  ["Prueba de hipótesis formal", "para la brecha entre sexos, con las herramientas de la clase 5."],
  ["Regresión regularizada", "para comprobar que nada dependa de las pruebas chicas (clase 7)."],
  ["Módulos siguientes", "varias temporadas, para separar el efecto del calendario del de la piscina."],
];
sig.forEach(([t, d], i) => {
  const y = 1.50 + i * 0.72;
  s8.addText(t, { x: 5.25, y: y, w: 4.20, h: 0.26, isTextBox: true, margin: 0,
    fontFace: BODY, fontSize: 11, bold: true, color: BCO });
  s8.addText(d, { x: 5.25, y: y + 0.26, w: 4.20, h: 0.42, isTextBox: true, margin: 0,
    fontFace: BODY, fontSize: 10, color: "CFE3EE", lineSpacingMultiple: 1.08 });
});

s8.addText("Felipe Leiva  ·  Javier Fuentes   ·   github.com/fleivadiaz/capstone-natacion   ·   Se usó IA (Claude, ChatGPT) para explorar la documentación de la API, discutir el diseño y revisar código.",
  { x: 0.55, y: 4.62, w: 8.9, h: 0.5, isTextBox: true, margin: 0,
    fontFace: BODY, fontSize: 9, color: "9FC4D6", lineSpacingMultiple: 1.1 });
s8.addNotes("Cerramos con las limitaciones. La muestra son los mejores de cada ranking, no es aleatoria: todo lo que decimos describe a la élite competitiva. Un nadador puede estar en distinta forma en cada calendario, y el diseño dentro-nadador lo promedia sobre miles de casos pero no lo elimina. Es un solo año. Y el modelo es una asociación, no una causa: mide cuánta diferencia hay por vuelta, no que la vuelta sea lo único que la produce. Lo que sigue es el informe del viernes, con el modelo y la base mensual ya incorporada, los intervalos de confianza por prueba con lo de la clase 5, y una regresión regularizada con lo de la clase 7 para comprobar que las conclusiones no dependen de las pruebas con menos pares. Más adelante, varias temporadas, para separar el efecto del calendario del efecto de la piscina. Quedamos atentos a preguntas.");

pres.writeFile({ fileName: "/home/claude/Presentacion_avance_Capstone.pptx" })
  .then(f => console.log("OK:", f));
