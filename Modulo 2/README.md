# Módulo 2 — Evaluación 2: dashboard de KPI

Felipe: este es el resumen de lo que trabajé entre el 17 y el 21 de octubre, para que podamos
decidir juntos lo que falta. — Javier

**Entrega: domingo 25-oct-2026, 23:59.** La pauta decía 18-oct; se postergó una semana por la
suspensión de clases por las lluvias. Se sube un PDF de **máximo 10 páginas** con: (a) al menos
3 KPI de eficacia, efectividad o calidad, diseñados con los pasos vistos en clases; (b) un
dashboard en **Power BI o Tableau** con datos reales y anonimizados; (c) una narrativa sobre el
diseño y la interpretación del dashboard.

---

## La idea: contar la temporada desde una federación

En vez de un dashboard sobre el factor de conversión, la propuesta es **"bajar el balón al
suelo"**: contar primero la temporada 2024 y después medir el desempeño de cada federación. Tiene
dos ventajas:

1. **Los KPI tienen a alguien que decide.** El marco de la Clase 4 supone una organización que
   actúa sobre el indicador. Una federación sí decide: a quién enviar, a dónde y con qué
   presupuesto. Un factor de conversión no tiene usuario que actúe sobre él.
2. **Termina en la pregunta del Capstone.** La federación tiene que elegir dónde buscar la marca
   mínima, y la tabla de mínimas no es equivalente entre piscinas (16 de 24 pruebas son más fáciles
   en 25 m). El factor pasa a ser una variable de decisión.

**Arco en tres actos:**
1. **La temporada en el mundo:** cuándo, dónde y quiénes compiten, y en qué torneos.
2. **Rendimiento por federación:** los tres KPI (`Fichas_KPI.md`).
3. **El costo de competir:** km, husos horarios y piscina disponible, que llevan a la pregunta
   del Capstone.

El usuario es el **director técnico de una federación genérica**, que la elige en un filtro y ve
su continente como contexto. Chile es solo un ejemplo.

---

## Qué cambió en los datos

| Cambio | Por qué |
|---|---|
| **Nacionalidad imputada.** El 82 % de los nadadores viene con país "CLB" (inscrito por club). La API sí entregaba el país del club y de la sede, pero `descarga_temporadas.py` los descartaba | Sin esto no hay KPI por federación. Cascada: oficial (18 %) → país del club (61 %) → país donde compite más (21 %). Validación: club = oficial en el 93 % de los casos donde existen ambos |
| **La base v2 recupera 11.578 nados.** 7.782 eran del tope de 5.000 en abril; 3.788, de dos consultas que habían **fallado sin aviso**: 50 libre M de diciembre y 400 libre M de agosto, ambas en 50 m | ⚠ **Afecta al informe del 25-sep**: en 50 libre masculino faltaban las marcas de diciembre. Hay que recalcular esos factores más adelante |
| **Continente** desde el endpoint `/fina/countries` | Agrupar por continente |
| **Coordenadas** de las 221 sedes (Nominatim / OpenStreetMap) | Mapas, km y husos horarios. Atribución: © colaboradores de OpenStreetMap (ODbL) |
| **Clasificación de los 307 torneos** por alcance (mundial, continental, internacional, nacional, regional, escolar-universitario) y categoría (absoluta o juvenil) | KPI 3 y la historia de la temporada. 40 casos dudosos quedan para revisar a mano |

`nadosFull_<sexo>.csv`, la base del informe, **no se tocó**: la v2 se guarda aparte.

---

## Hallazgos que condicionan los KPI

- **Sesgo de visibilidad.** Solo 78 de 207 federaciones (2024-S1) tienen torneos locales en el
  ranking. Las demás aparecen únicamente con sus nadadores de élite compitiendo afuera; México,
  por ejemplo, figura con el 100 % en el exterior y el 60 % con mínima B. Sus porcentajes no son
  comparables, así que los KPI comparativos usan solo federaciones con torneos locales y al menos
  30 nadadores. También es buen material para el Módulo 5.
- **La API entrega solo la mejor marca de cada nadador por mes** (`timesMode=BEST_TIMES`; se
  probaron otros valores y dan error). Participaciones y podios son **cotas inferiores**.
- **Gran Bretaña y China/Hong Kong se dejan como World Aquatics los define.** GBR es una sola
  federación miembro; Inglaterra, Escocia y Gales no tienen código en los datos. Hong Kong,
  Macao y Taipéi Chino son federaciones distintas de China, con cupos propios. Irlanda es el caso
  débil: el 86 % de sus nadadores se imputa por sede.
- **Piscinas en OpenStreetMap (idea para más adelante).** Chile tiene 23.116 "piscinas" en OSM,
  pero solo 21 con largo registrado; Hungría tiene 440. El conteo mide cuánto mapea cada país, no
  su infraestructura. Queda para el Módulo 5: sesgo de cobertura, licencia ODbL y privacidad, porque
  un mapa de piscinas residenciales es un mapa de viviendas.

---

## Archivos

| Archivo | Qué es |
|---|---|
| `Fichas_KPI.md` | **Los 3 KPI** con los pasos de la Clase 4, línea base 2024 y lo que falta decidir (⚠) |
| `../04_kpi_federaciones.ipynb` | Los KPI y sus gráficos en Python: calidad del dato, temporada, mapa de sedes, KPI 1–3, mapas de viajes |
| `Analisis_factibilidad_ideas.md` | Evaluación de todas las ideas (factibilidad, relevancia, aporte, módulo donde rinden más) |
| `Topicos_Evaluacion2.md` | Lo que pide la pauta y los conceptos de las clases 1 a 6 que hay que reflejar en el PDF |
| `../base_federaciones.py` | Construye la base anonimizada, la clasificación de torneos y las tablas KPI |
| `../descarga_complementos.py` | Países, continentes y coordenadas |
| `../datos/kpi_federacion_semestre.csv` | **La tabla para el dashboard**: KPI por federación y semestre, con numeradores, denominadores y columnas de calidad |
| `../datos/torneos.csv` | Clasificación de torneos; los casos con `revisar = True` se corrigen en `datos/torneos_override.csv` |

Las clases, la pauta y el brochure (PDF) **no se suben**: son material del curso y el repositorio
es público.

Para regenerar todo (casi todo sale de la caché local de la API):

```
python descarga_temporadas.py --femenino
python descarga_temporadas.py --masculino
python descarga_complementos.py
python base_federaciones.py
```

---

## Software: Tableau, con Power BI como alternativa

| | Tableau | Power BI |
|---|---|---|
| Líneas de viaje origen → sede | **Nativo** (`MAKEPOINT`, `MAKELINE`, `DISTANCE`) | No nativo: requiere un visual de terceros |
| Tarjetas de KPI con meta y semáforo | Hay que armarlas ("matriz de símbolos", Clase 6) | **Nativas** |
| Licencia | Desktop pago, con licencia gratuita para estudiantes. Tableau Public publica los datos | Desktop gratis en Windows |

La historia depende de mapas y distancias, así que la recomendación es Tableau. Sin licencia,
Power BI sirve con un mapa de burbujas en vez de líneas de viaje.

---

## Lo que falta decidir (⚠) y ruta propuesta

**Decisiones:**
1. ¿Tableau o Power BI?
2. Metas y rangos de cada KPI (sin ellos no hay semáforos). Propuesta: cuartiles del continente.
3. ¿Agregamos el *hit rate* (KPI de efectividad) y las mínimas 2024?
4. Revisar los 40 torneos dudosos; conviene hacerlo entre los dos.

**Ruta hasta el domingo:**

| Día | Qué |
|---|---|
| mié 21 | Revisar el notebook juntos; fijar metas; corregir torneos |
| jue 22 | Maqueta de baja fidelidad del dashboard (2–3 vistas: resumen de KPI, temporada, detalle por federación) |
| vie 23 | Construir el dashboard |
| sáb 24 | PDF: fases de los KPI, datos, capturas, narrativa |
| dom 25 | Margen y entrega |
