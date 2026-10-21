# Ideas para el Módulo 2 y siguientes: factibilidad, relevancia y aporte

17-oct-2026 · Base: ranking mensual de World Aquatics 2024 (424.528 nados, 71.514 nadadores),
caché cruda de la API (`datos/cache/`, 575 respuestas) y pruebas en vivo hechas hoy contra la
API de World Aquatics y contra Overpass (OpenStreetMap).

> **Estado al 21-oct:** ya implementado lo recomendado en §5, "cambios al código de descarga":
> puntos 1, 2, 3, 5 y 6 (la geocodificación quedó dentro de `descarga_complementos.py`). Los KPI se
> redefinieron al probarlos con los datos; la versión vigente está en `Fichas_KPI.md`. Siguen
> pendientes las temporadas 2023 y 2025, las mínimas 2024, el hit rate, los clusters (#9) y las
> piscinas de OSM (#8).

---

## 0. Lo que se verificó hoy y cambia el panorama

| Verificación | Resultado | Consecuencia |
|---|---|---|
| País del nadador | **82 %** viene como `CLB` ("Club"), no solo rusos | Sin arreglo no hay KPI por federación |
| Campos ocultos en la caché | La API entrega `clubCountryCode`, `clubName`, `eventCountryCode`, `pool`, `tags`, y `descarga_temporadas.py` los descarta | Se recuperan **sin volver a descargar**: basta agregarlos a `normalizar()` y re-ejecutar, porque `pedir()` lee de la caché |
| Imputación de nacionalidad en cascada | Oficial 18,0 % → país del club 60,9 % → país modal donde compite 21,1 % | Cobertura ~100 %, con una bandera de confianza por nivel |
| Validación de la imputación | Club = oficial en 92 %; país modal = club en 91 % | Defendible; se declara el error esperado |
| Endpoint `/fina/countries` | 246 países con UUID y **continente** (`RegionName`) | La agrupación por continente es directa |
| Filtro `countryId` de la API | Funciona, pero solo filtra por nacionalidad **oficial** (3 chilenos en 100 libre, ignora los inscritos por club) | No sirve para descargar por federación; la imputación es el camino |
| Truncamiento del ranking mensual | 4 de 576 consultas superan el tope de 5.000, todas de **abril en 50 m**; cobertura del 98,2 % | Arreglo barato: partir abril en dos quincenas |
| `timesMode` | Solo existe `BEST_TIMES`; `ALL_TIMES` y variantes dan error | **Se observa la mejor marca de cada nadador por mes, no todos sus nados.** Limita las ideas de participación y de desgaste (§3) |
| Sedes | 83 países sede, ninguna fila sin sede; 307 competencias, 221 ciudades | Mapa de sedes y distancias factibles |
| Grandes eventos presentes | Mundial 25 m Budapest (883 nadadores), Doha (847), París (726) | El hit rate es factible |
| Piscinas en OSM, Chile | 23.116 `leisure=swimming_pool`; **160** con `sport=swimming`, **21** con `length`, 34 centros deportivos de natación | El conteo bruto mide piscinas de casa y esfuerzo de mapeo, no infraestructura |
| Piscinas en OSM, Hungría | 8.596 piscinas; 359 con `sport=swimming`, **440** con `length`, 240 centros | La calidad de etiquetado varía 20× entre países: el sesgo es del mapeo, no de la realidad |

---

## 1. Evaluación por idea

Escala: **Alta / Media / Baja**. "Esfuerzo" en días-persona aproximados.

| # | Idea | Factibilidad | Esfuerzo | Relevancia para la Ev. 2 (M2) | Aporte a la investigación | Módulo donde rinde más |
|---|---|---|---|---|---|---|
| 1 | Storytelling de la temporada (sedes, nacionalidades, edades, tipo de torneo) | **Alta** | 1–1,5 | **Alta**: es la narrativa que pide la parte c) | Media: contexto y sesgos de la muestra | M2 |
| 2 | Nacionalidad imputada y continente | **Alta** | 0,5 | Alta: habilita todo lo "por federación" | **Alta**: corrige el 82 % de la base | M2 → M5 |
| 3 | Clasificables potenciales por federación (Beijing 2026 como torneo genérico + mínimas 2024) | **Alta** | 0,5–1 | **Alta**: KPI de eficacia natural | **Alta**: conecta con la brecha 25/50 m del Capstone | M2 |
| 4 | Hit rate (con mínima → nadó el campeonato) | Media | 0,5 | Alta: KPI de efectividad | Media | M2 |
| 5 | Participación en el exterior (cota mínima por federación) | Media | 0,5 | Alta: KPI operativo con meta | Media | M2 |
| 6 | Podios mensuales, semestrales y anuales | Media | 1 (requiere el #1) | Media-alta: KPI de calidad | Baja-media | M2 |
| 7 | Km y horas de viaje (desgaste); costo como escenario hipotético | Media-alta | 1 | **Alta**: historia humana, mapa de flujos (Clase 3) | Media; alta si se testea el desgaste (§3) | M2 → M3 |
| 8 | Piscinas por federación (OSM) | **Baja** tal como está; media con proxies | 2–4 | Baja para esta entrega | Media | **M5** (gobernanza), M3 |
| 9 | Clusters de federaciones por especialización (estilo, distancia, piscina) | **Alta** con los datos actuales | 1–2 | Media (una vista del dashboard) | **Alta**: pregunta nueva y propia | **M3** (no supervisado) |

---

## 2. Detalle por idea

### 2.1 Storytelling de la temporada (#1)
- **Datos:** `eventCountryCode` y `eventCity` (sede), fecha (calendario), edad, pool (tipo de
  piscina), nacionalidad imputada (#2).
- **Tipo de torneo:** la API no lo entrega de forma legible. El campo `tags` (valores 16, 32, 36,
  20, 18…) podría codificarlo; hay que verificarlo. Si no, se clasifican los 307 nombres con reglas
  (`Age`, `Junior`, `Youth`, `National`, `Trials`, `World`, `Cup`, `Open`, `BUCS`…) y una revisión
  manual de lo que quede. Es un día de trabajo, una sola vez.
- **Historia en tres actos:** (1) la temporada en el mundo: cuándo y dónde se compite y quiénes;
  (2) el rendimiento de cada federación (KPI); (3) el costo de competir: distancias, viajes y
  piscina disponible, que lleva a la pregunta del Capstone.
- **Hallazgos ya visibles:** la mediana de edad es 16 años, así que el ranking es mayoritariamente
  juvenil; abril, noviembre y diciembre concentran los nados; un país puede casi no existir en el
  ranking si sus torneos no se reportan a World Aquatics (Chile: un solo torneo en 2024).

### 2.2 Nacionalidad y continente (#2)
- La cascada oficial → club → país modal de competencia ya está medida (§0). La bandera de nivel
  permite mostrar en el dashboard "con nacionalidad imputada".
- Casos especiales: neutrales (`NAB`/`AIN`, rusos y bielorrusos), equipo de refugiados y el 21 %
  imputado por sede, que sesga hacia el país anfitrión. Un extranjero que vive y compite en
  Australia queda como australiano: es justamente lo que mide "federación de facto".
- **Aporte a M5:** ejemplo concreto de dato faltante disfrazado, imputación con error conocido
  y decisión documentada. Sale casi gratis.

### 2.3 Clasificables por federación (#3)
- **KPI:** porcentaje de nadadores de la federación con marca mínima A o B, respecto de sus
  nadadores rankeados, por semestre (o mes).
- **Mínimas:** Beijing 2026 como "torneo genérico" (ya transcritas, coherente con el informe) y,
  como contraste temporal correcto, las de **Doha 2024 / París 2024 (50 m)** y **Budapest 2024
  (25 m)**. Hay que transcribirlas de los PDF oficiales (≈ 3 tablas × 2 sexos × 12 pruebas).
- **Puente con el Capstone:** se puede desglosar "clasificables en 25 m vs en 50 m". Como 16
  pruebas son más fáciles en 25 m, una federación con acceso solo a piscina corta queda favorecida
  en esas pruebas. Ese es el gancho narrativo hacia la pregunta del proyecto.

### 2.4 Hit rate (#4)
- **KPI:** porcentaje de nadadores con mínima que nadaron el campeonato, respecto de los que la
  lograron.
- **Limitación fuerte:** como solo se ve la mejor marca del mes, un nadador que fue al Mundial de
  diciembre pero nadó más rápido en otro torneo ese mismo mes no aparece en el Mundial. El hit rate
  queda **subestimado**. Mitigación: consultar el ranking acotado a las fechas exactas del
  campeonato (Budapest: 10–15 dic), lo que deja solo los nados de esos días. Son ~24 consultas por
  evento.
- Además, el cupo por país (máx. 2 por prueba con marca A) hace que no todo clasificable pueda ir.
  Eso es parte de la interpretación, no un error.

### 2.5 Participación en el exterior (#5)
- **KPI:** cantidad de nadadores de la federación con al menos un nado fuera de su país en el
  semestre, frente a una cota mínima definida como meta.
- Es una **cota inferior** (mejor marca por mes). Se declara así y el KPI sigue siendo útil para
  comparar federaciones, porque el sesgo afecta a todas por igual.

### 2.6 Podios (#6)
- `medalla` existe (≈ 9.500 oros, platas y bronces), pero incluye torneos por edad. Solo tiene
  sentido después de clasificar torneos (#1): "podios en torneos internacionales / continentales".
- La misma cota inferior: un podio en un torneo donde el nadador no hizo su mejor marca del mes no
  se ve.

### 2.7 Kilómetros, horas de viaje y desgaste (#7)
- **Datos nuevos:** geocodificar 221 ciudades sede (Nominatim, una vez, con caché) y un punto de
  origen por federación (capital o centro de masa de sus sedes "locales"). Distancia ortodrómica
  (haversine), horas de vuelo estimadas (≈ km/800 + escalas) y **diferencia horaria** (librería
  `timezonefinder`, offline).
- **Costo:** escenario explícito (USD por km de vuelo + noches × tarifa), presentado como
  hipotético con parámetros visibles. No se presenta como dato.
- **El desgaste como hipótesis testeable:** "¿la mejor marca del mes se logra menos lejos de
  casa?" o "¿los puntos FINA bajan con los husos horarios cruzados?". Es interesante, pero hay dos
  sesgos que lo vuelven débil para causalidad:
  1. Solo vemos la mejor marca del mes (selección).
  2. Los torneos lejanos suelen ser los objetivos de la temporada, donde el nadador llega afinado:
     el efecto esperado va en **contra** del desgaste.
  → Para M2 se usa como **descriptivo** (km y husos por federación y continente). El test queda
  para M3, con diseño dentro del nadador y declarando los sesgos.
- La visualización ideal es un **mapa de flujos** origen → sede (Clase 3, mapas de líneas).

### 2.8 Piscinas por federación con OSM (#8)
- **El problema confirmado:** `leisure=swimming_pool` mezcla piscinas residenciales, de hotel y
  deportivas. El etiquetado útil (`sport=swimming`, `length`, `access`) es voluntario y desigual
  entre países (Chile 21 con largo, Hungría 440). Un conteo bruto correlacionaría con **cuánto
  mapea la comunidad OSM local**, no con la infraestructura.
- **Proxies viables:**
  1. **Geometría:** de los polígonos se puede derivar el largo (rectángulo mínimo orientado) y
     filtrar los que miden ~25 o ~50 m con proporción ~2:1, más `sport=swimming` o un centro
     deportivo contenedor. Validar contra un país con censo conocido. Es pesado: millones de
     polígonos en Europa y EE. UU.
  2. **Infraestructura revelada, con nuestros propios datos:** número de sedes y ciudades
     distintas por país y **proporción de nados en 50 m vs 25 m por federación**. No mide
     piscinas, sino **uso** de piscinas, pero es la variable que importa para el Capstone y sale
     gratis.
- **La correlación con la calidad es ecológica** (a nivel país), con confusores obvios: población,
  PIB y clima. Hay que normalizar por población (World Bank API, CC BY 4.0) y no interpretar
  causalmente. Con ~200 federaciones el N es chico.
- **Valor para M5, que es alto:**
  - **Sesgo de cobertura** de datos colaborativos.
  - **Licencia ODbL:** obliga a atribuir y, si se publica una base derivada, a compartirla bajo la
    misma licencia.
  - **Privacidad:** un mapa de piscinas residenciales es un mapa de viviendas. Agregarlo por país
    lo mitiga.
  - **Calidad y gobernanza de metadatos:** etiquetas voluntarias sin esquema obligatorio.

### 2.9 Clusters de federaciones (#9)
- **Pregunta:** ¿existen federaciones especializadas en ciertos estilos, distancias o piscinas?
- **Variables por federación:** proporción de nadadores por estilo, distancia y piscina; puntos
  FINA medios relativos por estilo; nadadores en el top-N; edad mediana. Mínimo de nadadores por
  federación (p. ej. ≥ 30) para que las proporciones no sean ruido.
- **Cuidado:** los datos son composicionales (las proporciones suman 1); conviene usar la
  transformación log-ratio (CLR) o trabajar con los puntos FINA relativos. Y la composición del
  ranking refleja en parte qué pruebas se nadan en los torneos reportados, no solo
  especialización.
- **Factible hoy** con la base actual más la nacionalidad imputada. Es materia directa de **M3**
  (k-means o jerárquico, silueta, interpretación). La infraestructura (#8) entra después como
  variable explicativa de los clusters.

---

## 3. Limitación transversal: la API entrega la mejor marca del mes

Se confirmó que `timesMode` solo acepta `BEST_TIMES`. Todo lo que cuente **participaciones,
podios o presencia en torneos** es una **cota inferior**. Se declara en el PDF y en el dashboard
(nota al pie de cada KPI afectado). Consultar ventanas más cortas (por semana o por las fechas de
un torneo) reduce el sesgo donde importa, a cambio de más consultas.

---

## 4. Relevancia para el Capstone y para el diplomado

| Módulo | Qué aporta este trabajo |
|---|---|
| **M2 (ahora)** | Storytelling (#1), KPI con una organización real detrás (federación: decide a quién enviar, a dónde y con qué presupuesto), mapas de sedes y de flujos |
| **M3 Machine Learning** | Clusters de federaciones (#9), test del desgaste por viaje (#7), regresión regularizada ya prevista en el informe |
| **M4 Deep Learning / LLM** | Clasificación de los nombres de torneos con un LLM o embeddings (#1), si la revisión manual queda corta |
| **M5 Gobernanza, ética, regulación** | Imputación de nacionalidad (#2), términos de uso de World Aquatics, datos de **menores de edad** (mediana de 16 años: nombre + fecha de nacimiento = dato personal sensible), ODbL y sesgo de cobertura de OSM (#8) |

**El hilo que une todo con la pregunta del Capstone:** una federación decide dónde mandar a sus
nadadores a buscar la mínima. Eso depende de la distancia, del costo y de la piscina disponible,
y la tabla de mínimas no es equivalente entre piscinas (16 pruebas son más fáciles en 25 m). El
factor de conversión deja de ser una curiosidad técnica y pasa a ser una variable de decisión.

---

## 5. Recomendación de alcance

**Para la Evaluación 2 (25-oct, 8 días):** #2 → #1 → #3 → #5 → #7 (km y husos; costo como
escenario) y, si alcanza, #4 y #6. Tres KPI candidatos:
1. **Eficacia:** % de nadadores de la federación con mínima (A/B, Beijing como genérico).
2. **Efectividad:** hit rate (con la mitigación de fechas exactas) o, si no alcanza, % de
   clasificables que compiten en el exterior.
3. **Calidad:** podios internacionales por nadador que compitió en el exterior.
   Alternativa: km recorridos por mínima lograda (eficiencia).

**Para después:** #9 en M3, #8 en M5 (con la versión de "infraestructura revelada" ya en el
dashboard de M2 como adelanto).

**Cambios al código de descarga** (todo reproducible y casi sin consultas nuevas):
1. `normalizar()`: agregar `clubCountryCode`, `clubName` real (hoy `club` mezcla `"Yes"` y el
   nombre), `eventCountryCode`, `pool`, `tags`. Re-ejecutar: cero consultas nuevas.
2. Partir abril en dos quincenas: 48 consultas nuevas (12 pruebas × 2 sexos × 2 quincenas, solo en 50 m).
3. Descargar `/fina/countries` una vez (continente y nombre normalizado).
4. Opcional, para tendencias: temporadas 2023 y 2025, con 576 consultas cada una (unos 10 minutos
   por sexo con la pausa actual).
5. Nuevo `geocodificar_sedes.py` con caché (221 ciudades).
6. Tabla `torneos.csv` con el tipo de torneo (reglas + revisión manual).
