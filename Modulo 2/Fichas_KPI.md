# Fichas de los KPI — Evaluación 2, Módulo 2

Borrador de trabajo, 21-oct-2026. Sigue los elementos de la Clase 4: los **6 pasos** para
seleccionar indicadores, la **ficha** de diseño (nombre, fórmula, unidades, glosario,
comportamiento histórico), la **comparación con un valor de referencia** y la **estructura
gramatical** del nombre. Las cifras vienen de `datos/kpi_federacion_semestre.csv` y
`datos/kpi_continente_semestre.csv`, y los gráficos están en `04_kpi_federaciones.ipynb`.

**Lo que falta decidir entre los dos está marcado con ⚠.**

**Decidido el 22-oct:** metas por **cuartiles del continente** en los tres KPI (el criterio más
usado en gestión): verde ≥ p75, amarillo entre p25 y p75, rojo < p25. Herramienta: **Tableau**.
La revisión manual de torneos no se hace: queda como limitación declarada en la entrega.

---

## Pasos 1 y 2: proceso, usuario y factores claves de éxito

**Proceso que se monitorea:** la preparación competitiva de una federación nacional de natación
a lo largo de la temporada. Quiénes alcanzan nivel de clasificación, cuántos compiten fuera del
país y con qué resultado.

**Usuario:** el director técnico de una federación **genérica**. La elige en un filtro y ve su
continente como contexto. Chile sirve de ejemplo, no es el usuario.

**Decisión que apoya:** a quién enviar, a qué torneos y con qué presupuesto. Viajar desde
América, Asia u Oceanía cuesta km, horas de vuelo y husos horarios que en Europa casi no existen.

| Factor clave de éxito | KPI | Dimensión (Clase 4, l13) |
|---|---|---|
| Tener nadadores con nivel de clasificación | KPI 1 | Eficacia |
| Darles roce internacional | KPI 2 | Efectividad (participación) |
| Convertir ese roce en resultados | KPI 3 | Calidad |

**Población común.** Nadadores en el ranking mensual de World Aquatics 2024. Para comparar
federaciones solo se usan las que **tienen torneos locales en el ranking** y al menos 30
nadadores en el semestre (ver "sesgo de visibilidad" en `README.md`).

---

## KPI 1 — Eficacia: nadadores con marca mínima

| Elemento | Definición |
|---|---|
| **Nombre** | *Porcentaje de nadadores de la federación que lograron la marca mínima B, respecto de sus nadadores rankeados en el semestre* |
| **Estructura** | Porcentaje de (preposición) · nadadores (variable 1) · que lograron (acción) · la marca mínima B (adjetivo) · respecto de sus nadadores rankeados (variable 2) · en el semestre (complemento) |
| **Fórmula** | nadadores con al menos un nado ≤ mínima B de su prueba y piscina / nadadores rankeados × 100 |
| **Unidad** | % |
| **Glosario** | *Mínima B:* marca de Beijing 2026 (Mundial de 25 m), usada como **torneo genérico**; cada nado se compara con la mínima de su piscina. *Rankeado:* aparece al menos una vez en el ranking mensual |
| **Nivel** | Propósito |
| **Fuente** | Columnas `cumple_B` de `base_dashboard.csv` y `pct_con_minima_B` de las tablas KPI |
| **Frecuencia** | Semestral (mensual posible) |
| **Línea base (2024)** | S1: mediana entre federaciones 2,5 % (p25–p75: 1,3 %–6,8 %); S2: 3,6 % (1,7 %–7,8 %). Por continente, de 4 % (África) a 11 % (Asia, S2) |
| **Meta / rango** | Cuartiles de su continente en el semestre: verde ≥ p75, amarillo p25–p75, rojo < p25. Una meta fija sirve poco porque Europa y Asia parten de niveles distintos |
| **Limitaciones** | Mínimas de 2026 sobre marcas de 2024. ⚠ Agregar las de Doha y París 2024 (50 m) y Budapest 2024 (25 m) |

**Vínculo con el Capstone.** El 26 % de los nados es en piscina de 25 m, pero ahí se logra el
36 % de las mínimas B. Es coherente con que 16 de 24 pruebas sean más fáciles en 25 m, aunque no
lo prueba: los campeonatos de fin de año, con los nadadores en su mejor forma, son en piscina corta.

---

## KPI 2 — Efectividad: participación en el exterior

| Elemento | Definición |
|---|---|
| **Nombre** | *Porcentaje de nadadores de la federación que compitieron fuera de su país, respecto de sus nadadores rankeados en el semestre* |
| **Fórmula** | nadadores con al menos un nado con sede ≠ federación / nadadores rankeados × 100 |
| **Unidad** | % |
| **Glosario** | *Exterior:* país de la sede distinto de la federación imputada |
| **Nivel** | Componente |
| **Métricas de apoyo** | km medianos por viaje y husos horarios cruzados (aprox. por longitud) desde la **ciudad base** de la federación, que es su sede local más usada o, si no tiene, el centro del país |
| **Línea base (2024)** | S1: mediana 13,4 % (8,1 %–22,1 %); S2: 11,1 % (4,8 %–14,9 %). Km medianos por viaje: Europa ~600, resto 3.400–4.900 |
| **Meta / rango** | Cuartiles de su continente, igual que el KPI 1. Se lee como **nivel de exposición internacional**, no como "más es mejor": cada punto es costo en km y husos horarios, que el dashboard muestra al lado |
| **Limitaciones** | **Cota inferior:** la API entrega solo la mejor marca de cada nadador por mes, así que un viaje en que no hizo su mejor marca no se ve. Los nadadores imputados por sede quedan casi siempre como "locales" (1 % en el exterior) |

**Alternativa de efectividad (pendiente):** el *hit rate*, porcentaje de nadadores con mínima que
efectivamente nadaron el campeonato. Requiere bajar los resultados de Doha, París y Budapest en
sus fechas exactas (unas 72 consultas). ⚠ ¿Lo agregamos o reemplaza al KPI 2?

---

## KPI 3 — Calidad: podios internacionales

| Elemento | Definición |
|---|---|
| **Nombre** | *Porcentaje de nadadores de la federación que obtuvieron al menos un podio en torneos internacionales absolutos, respecto de los que compitieron en ellos en el semestre* |
| **Fórmula** | nadadores con medalla 1, 2 o 3 en torneo internacional absoluto / nadadores que compitieron en torneos internacionales absolutos × 100 |
| **Unidad** | % |
| **Glosario** | *Torneo internacional:* mundial, continental o meeting con **≥ 10 federaciones** (medido en los datos). *Absoluto:* se excluyen los internacionales por grupos de edad (Asian Age Group, CARIFTA) |
| **Nivel** | Producto / resultado |
| **Línea base (2024)** | S1: mediana 12,8 % (8,8 %–22,3 %), 62 federaciones; S2: 15,4 % (2,7 %–29,1 %), 39 federaciones. Solo federaciones con ≥ 10 nadadores en torneos internacionales |
| **Meta / rango** | Cuartiles de su continente, igual que el KPI 1 |
| **Historia de la definición** | Empezó como "podios por nadador" y no servía: Japón daba 1,2 por los podios del Japan Open (3 federaciones) y del Asian Age Group (medallas por categoría de edad). Con el umbral de 10 federaciones, la exclusión de torneos por edad y el paso a "% con al menos un podio", queda acotado entre 0 y 1 |
| **Limitaciones** | Depende de la clasificación de torneos, hecha por reglas sobre el nombre más el umbral de 10 federaciones. 40 casos quedaron marcados como dudosos en `datos/torneos.csv` y **no se revisan a mano**: se declara como limitación en la entrega |

---

## Pasos 5 y 6: medir, analizar, estandarizar

- **Medir y analizar:** `base_federaciones.py` recalcula todo desde la base. El notebook muestra
  rankings por federación, comparación por continente y mapas de sedes y de viajes.
- **Estandarizar:** `datos/kpi_federacion_semestre.csv` trae, por fila, numeradores,
  denominadores, porcentajes y dos columnas de calidad del dato (`cobertura`,
  `muestra_suficiente`). Es la tabla que se carga en Power BI o Tableau.
- **Indicador de calidad del dato (propuesto):** % de nadadores de la federación imputados por
  sede. Irlanda (86 %), Bolivia (83 %) y Australia (80 %) son los más altos. Se podría mostrar
  junto a cada KPI como advertencia.
