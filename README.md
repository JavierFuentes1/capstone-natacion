# Capstone — Natación: ¿es equivalente la exigencia para clasificar según la piscina?

**Pregunta.** ¿Es constante el factor de conversión entre piscina de 25 y 50 m, o
depende del estilo, la distancia y el sexo? ¿Y coincide con la equivalencia implícita
en las marcas mínimas vigentes de World Aquatics?

Felipe Leiva y Javier Fuentes · Diplomado en Ciencia de Datos Aplicada, UTFSM.

## Estado

| Entrega | Cuándo | Estado |
|---|---|---|
| Formulación (30%) | lu 7-sep | `Formulacion_Capstone_Leiva_Fuentes.pdf`, lista |
| Análisis exploratorio (40%) | lu 15-sep | `03_eda_capstone.ipynb`, ejecutado; falta agregarle los intervalos de confianza |
| Presentación oral del avance | ma 22-sep | Por armar |
| Informe de avance (25%) | vi 25-sep | Por escribir. Entra la regresión `diferencia_s ~ vueltas_extra` |

## Los resultados hasta ahora

- El factor **no es constante**: va de 1,0145 (100 mariposa femenino) a 1,0521
  (200 espalda masculino). El orden de estilos —mariposa < libre < combinado < pecho
  < espalda— se repite idéntico en ambos sexos.
- **Los hombres se benefician más de la piscina corta que las mujeres en las 12
  pruebas comparables**, entre 0,6 y 1,2 puntos porcentuales, significativo en todas.
  Contradice a Iglesias García et al. (2025).
- La equivalencia implícita en las marcas mínimas **captura la tendencia**
  (correlación 0,767) pero se desvía en un subconjunto de pruebas: hasta 3,66 s en
  400 combinado femenino, y 13 pruebas salen más baratas en 25 m contra 11 en 50 m.
- El efecto del nivel del nadador sobre el factor es un **artefacto de selección**:
  definir "élite" por uno de los dos tiempos mueve la mediana casi un punto
  porcentual sin cambiar ningún nadador.

## Cómo correr esto

El entorno se maneja con `uv` desde la raíz del proyecto (`~/diplomado-cdd`), no
activando el `.venv` a mano. Todos los comandos van desde ahí:

```
uv run python capstone/descargar.py --prueba     # verifica que la API responda
uv run python capstone/descargar.py              # baja la muestra (unos minutos)
uv run python capstone/factor_implicito_wa.py    # marcas mínimas vs. factor medido
uv run python capstone/formulacion.py            # regenera el PDF de la formulación
```

El notebook se abre en VS Code eligiendo el kernel `.venv`. Requiere **scipy**
(`uv add scipy`); `formulacion.py` requiere **reportlab** (`uv add reportlab`).

## Los datos no están en el repositorio

Los términos de uso de World Aquatics prohíben redistribuir los datos crudos, así que
`datos/nados.csv`, `datos/pares_lcm_scm.csv` y `datos/cache/` están en `.gitignore`.
Se regeneran corriendo `descargar.py` y luego el notebook. Sí están versionados los
agregados: `factores_por_prueba.csv`, `comparacion_wa.csv`, `factor_por_nivel.csv` y
`metadatos.md`, que son estadísticas por prueba y no contienen marcas individuales.

## Qué hay en cada archivo

| Archivo | Qué es |
|---|---|
| `Formulacion_Capstone_Leiva_Fuentes.pdf` | La entrega del 7-sep. 3 páginas |
| `formulacion.py` | Genera ese PDF con reportlab. **El texto se edita acá, no en el PDF** |
| `03_eda_capstone.ipynb` | La entrega del 15-sep. 69 celdas, una sección por criterio de la rúbrica |
| `figuras_eda/` | Las 5 figuras del EDA. Son las salidas inline del notebook, no hay `savefig` |
| `descargar.py` | Baja los tiempos de la API: 48 consultas, con caché y pausa entre peticiones |
| `factor_implicito_wa.py` | Marcas mínimas de Beijing 2026 transcritas + comparación con el factor medido |
| `nivel_y_factor.py` | El chequeo del sesgo de selección por nivel |
| `metadatos.py` | Genera el diccionario de las 25 variables |
| `01_exploracion.ipynb` | La exploración original. El EDA la reemplaza como entregable |
| `02_explorando.ipynb` | Cuaderno didáctico de pandas, no es entregable |
| `Presentacion_idea_Capstone.pptx` | Las 3 láminas del 3-sep, ya presentadas |

## Dos cuidados al editar

1. **El PDF no se edita, se genera.** Cualquier cambio hecho sobre el PDF se pierde
   la próxima vez que corra `formulacion.py`. El texto vive en los strings del script.
   Nada de subíndices Unicode (t₅₀): Helvetica los dibuja como cuadrados negros.
2. **Al re-ejecutar el notebook**, no usar el backend `Agg` de matplotlib: borra las
   imágenes inline del `.ipynb`. Y después de re-ejecutarlo hay que volver a extraer
   los PNG de `figuras_eda/` desde las salidas, o quedan desfasados.
