# Capstone — Natación: ¿es equivalente la exigencia para clasificar según la piscina?

**Pregunta.** ¿Es constante el factor de conversión entre piscina de 25 y 50 m, o
depende del estilo, la distancia y el sexo? ¿Y coincide con la equivalencia implícita en
las marcas mínimas vigentes de World Aquatics?

Felipe Leiva y Javier Fuentes · Diplomado en Ciencia de Datos Aplicada, UTFSM.

---

## Estado de las entregas

| Entrega | Cuándo | Estado |
|---|---|---|
| Formulación (30%) | lu 7-sep | `Formulacion_Capstone_Leiva_Fuentes.pdf` · entregada |
| Análisis exploratorio (40%) | ma 15-sep | `03_eda_capstone.ipynb` · entregado por este repositorio |
| Presentación oral del avance | ma 22-sep | `Presentacion_avance_Capstone.pdf` · presentada |
| Informe de avance (25%) | **vi 25-sep** | `Informe_Avance_Leiva_Fuentes.pdf` · listo, 7 páginas |

---

## Las tres decisiones que definen el análisis (20-sep)

1. **La base es la descarga mensual.** La API topa en 5.000 filas por consulta, así que
   pedir el año completo cortaba el ranking en las pruebas más pobladas. Pidiendo mes a
   mes: 424.528 nados y **43.914 pares**, contra 30.257 de la descarga anual.
2. **El factor se calcula con la mejor marca del año** de cada nadador
   (`factor_tiempo_s`), porque una marca mínima se cumple con **un** nado. Con la
   mediana del año el factor sube de 1,0318 a 1,0354, y la razón es mecánica: en 50 m la
   mediana de `veces` es 2 y en 25 m es 1, de modo que la mediana castiga sobre todo al
   numerador. La versión con la mediana se mantiene como análisis de sensibilidad.
3. **Los tiempos implausibles no se eliminan.** El filtro por segundos por metro queda
   desactivado y se declara como limitación: el corte superior descartaba sobre todo
   nadadores de 5 a 7 años que probablemente son reales, solo muy lentos. Eso recorta la
   muestra en vez de limpiarla.

## Los resultados

- Un factor único no sirve: con todos juntos da **1,0318**, pero solo **4 de los 24**
  intervalos de confianza por prueba y sexo lo contienen.
- El factor **no es constante**: va de **1,0181** en 100 mariposa femenino a **1,0521**
  en 200 espalda masculino, y sus intervalos de confianza del 95% —[1,0167–1,0195] y
  [1,0504–1,0537]— **no se solapan**. La ventaja es 2,9 veces mayor en una prueba que
  en otra.
- El orden de estilos —mariposa < libre < combinado < pecho < espalda— se repite
  **idéntico en ambos sexos**.
- **Los hombres se benefician más de la piscina corta en las 12 pruebas comparables**,
  entre 0,6 y 1,2 puntos porcentuales, significativo en todas (Mann-Whitney; el mayor de
  los doce valores p es 7,8e-08). Contradice a Iglesias García et al. (2025).
- La equivalencia implícita en las marcas mínimas **captura la tendencia** (correlación
  0,803) pero se desvía hasta 3,66 s, y **16 pruebas resultan más fáciles de clasificar
  en 25 m contra 8 en 50 m**.
- El efecto del nivel del nadador sobre el factor es un **artefacto de selección**:
  definir "élite" por uno de los dos lados del cociente mueve la mediana casi un punto
  porcentual sin cambiar ningún nadador.
- **Primer modelo:** `diferencia_s = β₀ + β₁ · vueltas_extra`, por estilo y sexo. β₁ va
  de 0,98 s por vuelta en libre femenino a 1,86 en espalda masculino, sin que sus
  intervalos se toquen. β₀ = −0,41 s y no incluye el cero: una relación puramente
  proporcional no ajusta.

---

## Cómo correr esto

El entorno se maneja con `uv` desde la raíz del proyecto (`~/diplomado-cdd`), sin
activar el `.venv` a mano. Todos los comandos van desde ahí, en este orden:

```
uv run python capstone/descarga_temporadas.py --femenino    # baja el ranking mensual (unos minutos)
uv run python capstone/descarga_temporadas.py --masculino   # idem, el otro sexo
# 1) el notebook construye datos/pares_mensual.csv
#    (abrir capstone/03_eda_capstone_javier.ipynb en VS Code, kernel .venv, Run All)
uv run python capstone/factor_implicito_wa.py    # marcas mínimas vs. factor medido
uv run python capstone/analisis_avance.py        # factores, intervalos, brecha, modelo
uv run python capstone/figuras_avance.py         # las figuras de la presentación
uv run python capstone/figuras_informe.py        # esquema de virajes y factores con intervalo
uv run python capstone/informe_avance.py         # arma el PDF del informe
```

Los dos scripts de descarga **necesitan el flag** `--femenino` o `--masculino`: sin él
se detienen. Cada uno hace 288 consultas a la API con media pausa entre ellas y cachea
las respuestas, así que una segunda corrida no vuelve a pedir nada.

Requiere **scipy** (`uv add scipy`); los PDF de entrega requieren **reportlab**
(`uv add reportlab`).

## Los datos no están en el repositorio

Los términos de uso de World Aquatics prohíben redistribuir sus contenidos, así que
`datos/nadosFull_femenino.csv`, `datos/nadosFull_masculino.csv`, `datos/nados.csv`,
`datos/pares_mensual.csv`, `datos/pares_lcm_scm.csv` y `datos/cache/` están en
`.gitignore`. Se regeneran con los comandos de arriba.

Sí están versionados los **agregados**, que son estadísticas por prueba y no contienen
marcas individuales: `factores_por_prueba.csv`, `comparacion_wa.csv`,
`factor_por_nivel.csv`, `modelo_pendientes.csv` y `metadatos.md`.

---

## Qué hay en cada archivo

### El flujo principal

| Orden | Archivo | Qué hace |
|---|---|---|
| 1 | `descarga_temporadas.py` | Baja el ranking mensual de la API (288 consultas por sexo, con caché) → `datos/nadosFull_<sexo>.csv` |
| 2 | `03_eda_capstone_javier.ipynb` | El análisis exploratorio sobre la base mensual. Construye y guarda `datos/pares_mensual.csv` |
| 3 | `factor_implicito_wa.py` | Marcas mínimas de Beijing 2026, factor implícito de la federación y su brecha → `datos/comparacion_wa.csv` |
| 4 | `analisis_avance.py` | Factor por prueba con intervalo por bootstrap, factor por estilo y sexo, brecha entre sexos, sesgo de selección y el modelo → `datos/factores_por_prueba.csv`, `datos/modelo_pendientes.csv`, figura del modelo |
| 5 | `figuras_avance.py` | Regenera las figuras 4-1, 4-4 y 4-5 sobre la base definitiva |
| 6 | `figuras_informe.py` | Las dos figuras agregadas al informe tras la presentación: el esquema de virajes (1-1) y los 24 factores con su intervalo frente al factor global (4-0). Solo lee tablas versionadas |
| 7 | `informe_avance.py` | Arma `Informe_Avance_Leiva_Fuentes.pdf` con las figuras de `figuras_eda/` |

### Los datos versionados

| Archivo | Qué es |
|---|---|
| `datos/factores_por_prueba.csv` | Factor mediano por prueba con su intervalo del 95% y el ancho |
| `datos/comparacion_wa.csv` | Marcas mínimas oficiales, factor implícito y brecha, por prueba |
| `datos/modelo_pendientes.csv` | β₀ y β₁ con sus intervalos, por estilo y sexo |
| `datos/factor_por_nivel.csv` | El chequeo del sesgo de selección con una segunda definición de nivel |
| `datos/metadatos.md` | Diccionario de las 25 variables del archivo crudo |

### Respaldo de lo que se afirma en el texto

| Archivo | Qué es |
|---|---|
| `nivel_y_factor.py` | Repite el chequeo del sesgo de selección definiendo el nivel por la marca mínima en vez del percentil |
| `metadatos.py` | Genera el diccionario de variables |
| `probar_paginacion.py` | Sonda: documenta que `page` se ignora y que `pageSize` topa en 5.000 |
| `probar_profundidad.py` | Sonda: cuántos nadadores distintos hay a cada profundidad del ranking |
| `modelo_avance.py` | El mismo modelo sobre la base **anual**, como contraste |
| `descargar.py` | La descarga anual original. Se conserva porque genera `nados.csv`, que usa el notebook de la entrega |

### Entregas y material de trabajo

| Archivo | Qué es |
|---|---|
| `03_eda_capstone.ipynb` | **La entrega del 15-sep**, sobre la base anual. Se conserva tal como se evaluó |
| `Presentacion_avance_Capstone.pptx` / `.pdf` | Las 8 láminas del martes 22 |
| `Guion_presentacion_avance.pdf` | Guion cronometrado, reparto y preguntas probables |
| `Informe_Avance_Leiva_Fuentes.pdf` · `informe_avance.py` | **El informe del viernes 25** y su generador. El texto se edita en el script |
| `Entrega_EDA_Leiva_Fuentes.pdf` | El PDF con el link a este repositorio, subido el 15-sep |
| `Formulacion_Capstone_Leiva_Fuentes.pdf` · `formulacion.py` | La entrega del 7-sep y su generador |
| `entrega_eda.py` | Genera el PDF de la entrega del EDA |
| `figuras_eda/` | Las figuras, salidas del notebook, de `figuras_avance.py`, `analisis_avance.py` y `figuras_informe.py` |
| `01_exploracion.ipynb` · `02_explorando.ipynb` | Cuadernos de trabajo previos, no son entregables |
| `Presentacion_idea_Capstone.pptx` · `Guion_presentacion_Capstone.pdf` | La presentación del 3-sep |

---

## Tres cuidados al editar

1. **Los PDF no se editan, se generan.** El texto vive en los strings de `formulacion.py`,
   `entrega_eda.py` e `informe_avance.py`. Nada de subíndices Unicode: Helvetica los
   dibuja como cuadrados. La β y el signo menos del informe salen de la fuente Symbol,
   que los visores comunes traen; si en un visor liviano no aparecen, es el visor.
2. **Al re-ejecutar un notebook**, no usar el backend `Agg` de matplotlib: borra las
   imágenes inline del `.ipynb`.
3. **Antes de creer un número, correr el notebook de cero.** Un notebook guarda salidas,
   no promesas: si los contadores de las celdas no van `[1] [2] [3]…` sin saltos, lo que
   se está leyendo puede venir de una versión anterior del código.
