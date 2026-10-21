# Evaluación 2 — Dashboard para el Proyecto Capstone: tópicos a tener en cuenta

Módulo 2: Visualización e Inteligencia de Negocios · Profesores Michell Concha y José Luis Martí
**Plazo: domingo 25 de octubre de 2026, 23:59, por el aula virtual** (la pauta decía 18-oct; se
postergó una semana por la suspensión de clases por lluvias en Santiago).

Fuentes revisadas: `Evaluación 2.pdf` y las clases 1 a 6 de `Modulo 2/Clases/`. Cuando una
definición viene de las diapositivas se indica la clase y la lámina (p. ej. *C4-l13*); lo que
no está en las láminas se marca como **[complemento]**.

---

## 1. Qué pide la evaluación (checklist)

| Parte | Exigencia literal | Cómo se cumple |
|---|---|---|
| **a)** | Plantear **al menos tres KPI** que midan la **eficacia, efectividad o calidad** del proceso, **usando los pasos (elementos) vistos en clases** | Para cada KPI: recorrer los 6 pasos de selección (§2.5), llenar la ficha de diseño (§2.6), redactarlo con la estructura gramatical (§2.8) y fijar meta y referencia (§2.7) |
| **b)** | Dashboard en **Power BI o Tableau** con los 3 KPI **y** alguna(s) visualización(es) para **monitorear el proceso**. Datos reales y **anonimizados** en lo posible | Captura(s) del dashboard en el PDF; describir la fuente y cómo se anonimizó |
| **c)** | **Narrativa** sobre el dashboard: aspectos principales de su **diseño** e **interpretación** | Sección de texto que explique por qué cada elemento está donde está y cómo se lee |

**Formato de entrega:** un PDF, **máximo 10 páginas**, con: fases del diseño de los KPI,
dashboard, datos usados y narrativa.

Riesgos a vigilar:
- La pauta dice "los pasos (elementos) vistos en clases": si el PDF no muestra explícitamente esos
  pasos por KPI, se pierde puntaje aunque los KPI sean buenos.
- El dashboard debe hacerse en Power BI o Tableau. Un gráfico de matplotlib no cumple.
- Tres KPI es el mínimo. Más de cinco o seis contradice el principio de simplicidad (§3.3).

---

## 2. Diseño de KPI (Clase 4, parte 1): lo que el PDF debe reflejar

### 2.1 Definiciones base (*C4-l4, l14*)

- **Indicador de gestión:** "expresión esencialmente cuantitativa que señala el progreso de los
  objetivos a cumplir"; "expresión matemática que cuantifica el estado de la característica o
  hecho que se quiere medir".
- **Indicador:** dato o conjunto de datos que ayuda a medir objetivamente la evolución de un
  proceso o actividad. Forma: `Indicador = A (unidad) / B (unidad)`.
- **Índice:** medida estadística para estudiar las fluctuaciones de una magnitud en el tiempo o
  el espacio, comparada con un nivel de referencia:
  `Índice = [A/B] / Nivel de referencia × 100`.
  → *Diferencia clave:* el indicador es la razón; el índice la compara contra una referencia o meta.

### 2.2 Las cuatro medidas de Parmenter (*C4-l5, l7, l8*)

| Medida | Qué mide | Frecuencia / zona | ¿Financiera? |
|---|---|---|---|
| **KRI** (Key Result Indicator) | Resultado global de una perspectiva; informa al directorio, **no dice qué hacer** | Mensual/trimestral · pasado | Sí (resumen) |
| **RI** (Result Indicator) | Resumen de la actividad de varias acciones o equipos | Diaria/semanal/mensual · pasado–presente | Suele serlo |
| **PI** (Performance Indicator) | Acción concreta de un equipo, alineada con la estrategia | Diaria/semanal · pasado–presente–futuro | No |
| **KPI** (Key Performance Indicator) | Lo más crítico para el éxito **ahora**; se mide seguido y **dispara acción inmediata** | 24/7 o diaria · presente–futuro | No |

- Analogía de la cebolla: piel = KRI (lo que ve el directorio), capas = PI y RI, núcleo = KPI.
- "Error común: llamar KPI a un dato financiero de resumen" (*C4-l8*).
- Cantidad recomendada: ~10 KRI, hasta 80 RI/PI, ~10 KPI. Kaplan y Norton: no más de 20 KPI;
  Hope y Fraser: menos de 10 (*C4-l9*).

> **Ojo para nuestro caso:** en sentido estricto de Parmenter, varias métricas del Capstone son
> más bien RI/PI (se calculan una vez por temporada). Conviene **declararlo y justificar** por
> qué se tratan como KPI: son los indicadores clave del proceso que se quiere monitorear, y
> el dashboard está pensado para recalcularse al actualizar el ranking (mes a mes).

### 2.3 Eficacia, eficiencia, efectividad, calidad, economía

La pauta pide medir **eficacia, efectividad o calidad**. Las láminas dan:

- *C4-l10:* **Eficiencia** = costo por unidad de productos y resultados. **Eficacia** = calidad
  del trabajo realizado. **Entradas** = recursos para la actividad; **Salidas** = medidas
  cuantitativas de lo que produce; **Resultados** = impacto de la actividad (calidad, no solo
  resultados).
- *C4-l13 — Dimensiones sugeridas según el nivel del objetivo:*

| Cuando se mide | Se está midiendo | Indicadores recomendados |
|---|---|---|
| Impacto | Fin | Eficacia |
| Resultados | Propósito | Eficacia, eficiencia |
| Productos | Componente | Eficacia, eficiencia, **calidad** |
| Procesos | Actividades | Eficacia, eficiencia, economía |
| Insumos | — | — |

  "Es importante que los indicadores tengan relación directa con el nivel en que se encuentra
  el objetivo." → cada KPI debe decir **en qué nivel** está (fin, propósito, componente, actividad).

**[complemento]** Las láminas no definen *efectividad* de forma explícita. Definiciones de uso
habitual, para dejarlas escritas en el PDF:

| Dimensión | Pregunta que responde | Forma típica |
|---|---|---|
| **Eficacia** | ¿Se logró el objetivo / la meta? | logrado / programado |
| **Eficiencia** | ¿Con cuántos recursos? | resultado / recurso usado |
| **Efectividad** | ¿Se logró el objetivo **y** produjo el impacto buscado? (eficacia + eficiencia, o impacto) | impacto observado / impacto esperado |
| **Calidad** | ¿Cumple el estándar? ¿Sin errores? | unidades conformes / total |
| **Economía** | ¿Se obtuvieron los recursos al menor costo? | costo real / costo presupuestado |

### 2.4 Niveles estratégico, táctico y operativo (*C4-l10–l12*)

Los indicadores operativos (I.1, I.2, I.3) alimentan un indicador táctico/global (I.G 1), que a
su vez apunta a un objetivo estratégico. El tablero **estratégico** muestra medidas de éxito; el
**táctico y operativo** muestra entradas, salidas, resultados, eficiencia y eficacia.
→ Útil para un esquema en el PDF que muestre cómo los 3 KPI se conectan con el objetivo del Capstone.

### 2.5 Los 6 pasos para seleccionar indicadores (*C4-l16*) — **"los pasos vistos en clases"**

1. **Determinar el sistema / proceso a monitorear.**
2. **Identificar los factores claves de éxito.**
3. **Establecer indicadores por factor.**
4. **Definir metas.**
5. **Medir y analizar.**
6. **Estandarizar y formalizar.** (y el ciclo vuelve a 1)

> Probablemente lo más evaluado en la parte a). Sugerencia: una sección por paso, o una tabla
> por KPI donde cada fila sea un paso.

### 2.6 Ficha de diseño de cada indicador (*C4-l19*)

| Elemento | Qué poner |
|---|---|
| **Nombre** | Concreto; define objetivo y utilidad |
| **Forma de cálculo** | Fórmula exacta y cómo se relacionan los factores |
| **Unidades** | Las que resultan de la fórmula (%, s, adimensional…) |
| **Glosario** | Definición de cada factor que entra al cálculo |
| **Comportamiento histórico** | Tendencia |

Más los requisitos de la Clase 5 (*C5-l5*): **período y población de referencia**, **meta o
comparación pertinente**, **fuente y nivel de detalle**, **calidad y actualización
verificables**, **responsable de los datos**.

### 2.7 Comparación con un valor de referencia (*C4-l21*)

Todo KPI debe compararse con algo:
- **Valor inicial** (línea base)
- **Valor a alcanzar → Umbral** (meta)
- **Valor actual → Status**
- **Valores mínimo y máximo → Rango** (semáforo)
- **Promedio histórico**
- **Tendencia**

> En la lámina "antes y después" (*C5-l8*), lo que cambia el dashboard malo en uno bueno es
> justamente esto: "Ventas $600 M · Meta $625 M · Cumplimiento 96 %" en vez de un número suelto.
> **KPI sin contexto = error.**

### 2.8 Estructura gramatical del nombre (*C4-l22–l23*)

`PREPOSICIÓN` + `SUSTANTIVO PLURAL (variable 1)` + `VERBO EN PARTICIPIO (acción)` +
`ADJETIVO` + `COMPLEMENTO CIRCUNSTANCIAL (tiempo/lugar)` + `respecto de SUSTANTIVO PLURAL (variable 2)`

Ejemplo de clase: "**Porcentaje de** **solicitudes de cotizaciones** **respondidas** **a tiempo**,
respecto de las **ingresadas** **durante la semana**" =
`cotizaciones respondidas a tiempo / cotizaciones ingresadas en la semana × 100`.

### 2.9 Características de un buen indicador (*C4-l17, l18*)

Claro · Relevante · Adecuado · Monitoreable · Económico · Aporte marginal. En detalle: mide algo
importante; se relaciona con los objetivos del proceso; tiene interpretación única; es fácil de
medir; sus fuentes de verificación son accesibles; tiene estándares de calidad claros (para qué
se mide); se adapta al nivel de responsabilidad; es aceptado.
→ Conviene un párrafo o tabla breve que **justifique cada KPI contra estas seis características**.

---

## 3. Diseño del dashboard (Clase 5 y Clases 1–3)

### 3.1 Propósito y usuario: lo primero (*C5-l4*)

"El diseño comienza con la decisión que necesitamos apoyar."
- **Usuario:** quién lo consulta y qué sabe del negocio y de los datos.
- **Decisión:** qué pregunta responde y qué acción permite.
- **Alcance:** período, nivel de detalle, frecuencia de consulta.
- **Relevancia:** cada elemento aporta a la pregunta principal.

### 3.2 Jerarquía visual (*C5-l6*)

1. **Resumen**: KPI principales con su referencia (arriba, grande).
2. **Contexto**: tendencias, comparaciones, desgloses.
3. **Detalle**: información para profundizar.

"La posición, el tamaño y el contraste guían la atención."

### 3.3 Principios de diseño y elección de gráfico (*C5-l7*)

- **Simplicidad**: sin decoración innecesaria · **Consistencia**: formatos, escalas y tipografías
  uniformes · **Color con significado**: paleta limitada, contraste, etiquetas claras ·
  **Orden y legibilidad**: alineación, espacio.
- **La pregunta orienta el gráfico:**

| Pregunta | Gráfico |
|---|---|
| Comparación | Barras |
| Evolución | Líneas |
| Composición | Barras apiladas |
| Consulta de valores | Tabla / matriz |

Tipos de visualización en Power BI (*C4-l70*): **comparación, relación, composición, distribución**.
Gráficos vistos en Tableau (*C6*): barras, dispersión, caja y bigotes, histograma, Pareto, mapa de
calor, mapa de árbol, mapa geográfico, barras agrupadas, torta, anillo, lollipop, **pesas
(dumbbell)** y **matriz de símbolos para KPI**.

### 3.4 Interactividad con propósito (*C5-l9*)

- **Filtros / segmentadores**: mostrar qué selección está activa y cómo limpiarla.
- **Drill-down**: explorar niveles de una jerarquía manteniendo el contexto.
- **Tooltips**: solo para detalle complementario.
- "**La información esencial debe ser comprensible sin interactuar**" → clave, porque se entrega
  como PDF estático: las capturas deben leerse solas.

### 3.5 Validación y checklist antes de compartir (*C5-l10*)

- [ ] Propósito y KPI relevantes
- [ ] Filtros útiles y estado visible
- [ ] Datos y cálculos consistentes
- [ ] Etiquetas claras y formatos uniformes
- [ ] Jerarquía y gráficos adecuados
- [ ] Interacciones que aportan valor

Más: validar con el usuario (tareas reales), definir un responsable y el control de actualización.

### 3.6 Fundamentos de visualización (Clases 1–3), para justificar decisiones en la narrativa

- **Qué / por qué / cómo visualizar** (marco de Munzner).
- **Tipos de atributo** (*C1-l16*): categóricos (nominales, ordinales) y numéricos (discretos,
  continuos). Ej.: estilo = nominal; distancia = discreto ordenado; factor = continuo.
- **Acciones del usuario** (*C1-l19*): *consumir* (descubrir, presentar, disfrutar) vs *producir*
  (anotar, registrar, derivar); *buscar* (lookup, browse, locate, explore); *consultar*
  (identificar, comparar, resumir). Un dashboard de monitoreo es "consumir/presentar + comparar".
- **Marcas** (punto, línea, área) y **canales** (*C1-l28–l39*): los de **magnitud** para datos
  ordenados y los de **identidad** para nominales. "Los atributos codificados con posición
  dominarán el modelo mental del usuario."
- **Ranking de efectividad** (*C1-l45*): posición en escala común > posición en escala no alineada
  > largo > ángulo > área > profundidad > luminosidad ≈ saturación > curvatura ≈ volumen. Para
  categorías: región espacial > matiz > movimiento > forma. → **Torta/anillo (ángulo/área) es
  menos precisa que barras**; argumento útil si se elige barras.
- **Expresividad** (codificar toda la información del atributo y nada más) y **efectividad** (lo
  más importante en el canal más preciso) (*C1-l40*).
- Criterios de efectividad del canal: precisión, discriminabilidad, separabilidad, **pop-out**,
  agrupamiento (*C1-l41*). El pop-out sirve para destacar la prueba fuera de meta.
- **Mapeo visual** (*C2-l24*): asignar atributos gráficos a variables (Var1→posición,
  Var3→color…). Incluir esta tabla en la narrativa queda muy bien.
- **Color** (*C2-l36–l43*): RGB vs **HSL**; **matiz = identidad** (nominal), **saturación y
  luminosidad = magnitud**; la transparencia interfiere con saturación y luminosidad.
- **Tipografía** (*C2-l45–l54*): sans serif para títulos y textos cortos (dashboard), serif para
  texto impreso largo; evitar fantasía y manuscritas.
- **Gestalt** (*C2-l55–l56*): proximidad, semejanza, cierre, continuidad, figura-fondo, simetría,
  dirección común. → agrupar los 3 KPI juntos (proximidad), mismo color para el mismo sexo
  en todos los gráficos (semejanza).
- **Malas visualizaciones** (*C1-l6–l10*): no respetar la **proporcionalidad de la tinta**; ejes que
  **no parten del origen**.
- **Mapas** (*C3*): coropletas con 3–7 clases y valores normalizados; símbolos escalados por
  área, no por diámetro. Solo aplica si se agrega una vista por país.

---

## 4. Herramienta: Power BI o Tableau

### Power BI (*C4, parte 2*)
- Funciones DAX vistas: lógicas (`IF`, `SWITCH`, `AND`, `OR`, `NOT`, `TRUE`, `FALSE`),
  de agregación (`COUNT`, `COUNTROWS`, `DISTINCTCOUNT`, `COUNTX`, `SUM`, `SUMX`, `AVERAGE`, `MIN`,
  `MAX`) y de filtro (`FILTER`, `CALCULATE`, `ALL`, `LOOKUPVALUE`, `SELECTEDVALUE`).
- Diferencia **columna calculada** (fila a fila) vs **medida** (agregada según el contexto de filtro):
  los KPI deben ser **medidas** para que respondan a los segmentadores.
- Esqueleto de un KPI con meta y semáforo **[complemento]**:
  ```DAX
  KPI_Valor   = DIVIDE( CALCULATE(COUNTROWS(T), T[cumple] = TRUE()), COUNTROWS(T) )
  KPI_Meta    = 0.80
  KPI_Estado  = SWITCH( TRUE(), [KPI_Valor] >= [KPI_Meta], "En meta",
                               [KPI_Valor] >= 0.6, "Alerta", "Fuera de meta" )
  ```
  Visuales útiles: **Tarjeta**, **KPI** (valor + objetivo + tendencia), **Medidor** (gauge),
  formato condicional para el semáforo.

### Tableau (*C6*)
- Dimensiones vs medidas; tarjeta de **Marcas** (color, tamaño, etiqueta, detalle, tooltip).
- Consulta 14: "KPI de ventas → **matriz de símbolos**" (indicador con forma/color según estado).
- Dashboard + **Historia (Story)**, útil para la narrativa de la parte c).

**Criterio de elección:** el que se tenga instalado y se maneje mejor; Power BI Desktop es
gratuito en Windows. Tableau Public también es gratuito, pero publica los datos en la web, lo que
choca con los términos de World Aquatics (§5).

---

## 5. Datos: reales y anonimizados

- La pauta pide **datos reales y anonimizados**. El Capstone ya los tiene.
- **Opción recomendada:** alimentar el dashboard con las **tablas agregadas versionadas**
  (`datos/factores_por_prueba.csv`, `datos/comparacion_wa.csv`, `datos/modelo_pendientes.csv`,
  `datos/factor_por_nivel.csv`). Son estadísticas por prueba y no identifican a nadie: el
  anonimato se cumple por agregación.
- Si se usa `pares_mensual.csv` (nivel nadador): quitar nombre, club, fecha de nacimiento y
  competencia; reemplazar `person_id` por un código correlativo o hash; declararlo en el PDF.
- Recordar la restricción ya documentada: los **términos de World Aquatics prohíben redistribuir**
  los datos crudos. No subir el `.pbix` con datos crudos a ningún lado público.
- Describir en el PDF: fuente (API de rankings de World Aquatics, temporada 2024, 43.914 pares),
  población, período, granularidad, quién produce cada dato y cómo se actualiza.

---

## 6. Encuadre del Capstone como "proceso" (lo más delicado)

> **Actualización 21-oct:** este fue el primer borrador, centrado en el factor de conversión. Se
> reemplazó por el enfoque por federación; los KPI vigentes están en `Fichas_KPI.md` y el contexto
> en `README.md`. Esta sección se conserva como registro de las alternativas consideradas.

La pauta habla de medir **el proceso**. El Capstone es una pregunta de investigación, no una
operación de negocio, así que hay que **definir explícitamente el proceso** (paso 1 de §2.5).
Opciones para iterar:

| Opción | Proceso a monitorear | Usuario / decisión |
|---|---|---|
| **A** | El sistema de **clasificación por marcas mínimas** de World Aquatics: ¿son equivalentes las dos tablas (25 m y 50 m)? | Federación / comité técnico: ajustar marcas mínimas. Entrenador / nadador: elegir en qué piscina intentar la mínima |
| **B** | La **conversión entre piscinas** (calculadoras con factor único) | Entrenadores que convierten marcas |
| **C** | El **pipeline de datos** del Capstone (descarga, emparejamiento, calidad) | El equipo: confiar en la base |

A es la más coherente con la pregunta del Capstone y con la idea de "KPI que dispara acción".

### Candidatos de KPI (borradores para discutir; calcular antes de fijar metas)

| # | Nombre (estructura de §2.8) | Fórmula | Dimensión | Nivel | Fuente |
|---|---|---|---|---|---|
| 1 | Porcentaje de pruebas del Mundial 2026 cuya marca mínima en 25 m resulta **equivalente** a la de 50 m, respecto del total de pruebas | pruebas con brecha dentro de una tolerancia (p. ej. ±0,5 s o dentro del IC) / 24 × 100 | Eficacia / **calidad** de la equivalencia | Propósito | `comparacion_wa.csv` |
| 2 | Brecha media absoluta entre la marca mínima oficial en 50 m y la equivalente según el factor medido, por prueba | mean(\|brecha_s\|) o en % de la marca | **Calidad** (desviación del estándar) | Componente | `comparacion_wa.csv` |
| 3 | Porcentaje de pruebas cuyo intervalo de confianza del factor contiene el factor único (1,0318), respecto de las 24 pruebas | pruebas con IC ∋ 1,0318 / 24 × 100 (hoy 4/24 = 16,7 %) | **Efectividad** del factor único como regla de conversión | Fin / impacto | `factores_por_prueba.csv` |
| 4 *(alt.)* | Balance de equidad: pruebas más fáciles en 25 m menos pruebas más fáciles en 50 m | (n₂₅ − n₅₀) / 24 (hoy (16−8)/24) | Calidad / equidad | Propósito | `comparacion_wa.csv` |
| 5 *(alt., opción C)* | Porcentaje de nadadores del ranking con marca válida en ambas piscinas, respecto del total | pares / nadadores × 100 | Calidad de datos / cobertura | Actividad | `metadatos.md` |
| 6 *(alt.)* | Precisión de la estimación: ancho medio del IC 95 % del factor | mean(ic_alto − ic_bajo) | Calidad de la medición | Actividad | `factores_por_prueba.csv` |

Para cada uno falta: **meta/umbral** y su justificación, **rango** para el semáforo, **línea
base**, **frecuencia** (¿mensual, con el ranking?) y **responsable**.

### Visualizaciones de monitoreo candidatas (ya existen versiones en el EDA)
- Factor por prueba con su IC frente a la línea del factor único (puntos + barras de error).
- **Dumbbell (pesas)**: marca mínima oficial 50 m vs equivalente según el factor medido, por
  prueba, coloreado según "más fácil en 25 m / 50 m".
- Segundos por vuelta extra por estilo y distancia (líneas o barras agrupadas).
- Brecha entre sexos por prueba (barras divergentes).
- Segmentadores: sexo, estilo, distancia.

---

## 7. Narrativa (parte c)

Debe cubrir **diseño** e **interpretación**:
- **Diseño:** usuario y decisión (§3.1); por qué esa jerarquía (§3.2); tabla de mapeo visual
  variable → canal (§3.6); uso del color (matiz para sexo o estado, sin decoración); por qué
  barras/puntos y no tortas (ranking de canales); qué filtros hay y para qué.
- **Interpretación:** cómo leer cada KPI (qué significa subir o bajar, qué valor es bueno), el
  estado actual frente a la meta, qué acción sugiere (p. ej. "las 16 pruebas más fáciles en 25 m
  sugieren revisar la tabla de mínimas de 25 m"), y limitaciones (una temporada, población del
  ranking, curtosis alta → mediana y bootstrap).
- Recurso visto en Tableau: **Story** como soporte de la narrativa.

---

## 8. Estructura sugerida del PDF (≤ 10 páginas)

1. Portada + contexto del Capstone y del proceso a monitorear (1 p.)
2. Diseño de los KPI: los 6 pasos, la ficha y la estructura gramatical de cada uno, metas y
   referencias, justificación con las características de un buen indicador (3 p.)
3. Datos usados: fuente, población, período, anonimización, calidad (1 p.)
4. Dashboard: captura(s) a página completa (2 p.)
5. Narrativa: diseño e interpretación (2 p.)
6. Conclusión / limitaciones / mantenimiento (½–1 p.)

---

## 9. Decisiones pendientes para la siguiente iteración

1. ¿Power BI o Tableau? ¿Cuál está instalado?
2. ¿Qué "proceso" se adopta (A, B o C del §6)?
3. ¿Cuáles 3 KPI (o 4) y con qué metas? Las metas necesitan una justificación (estándar externo,
   tolerancia de cronometraje, percentil histórico…).
4. ¿Tablas agregadas o base a nivel nadador anonimizada? (afecta qué filtros se pueden ofrecer)
5. ¿El PDF se genera con un script, como las entregas anteriores (`reportlab`), o en Word?
6. ¿Entrega individual o con Felipe Leiva? (la pauta no lo dice)
