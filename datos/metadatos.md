# Metadatos del proyecto

Generado automáticamente desde `nadosFull_masculino.csv` + `nadosFull_femenino.csv` (424.528 filas × 25 columnas) y `pares_mensual.csv` (43.914 filas).


## Fuente 1 — API pública de World Aquatics (rankings)

| Variable | Tipo | Unidad / valores | % nulos | Distintos | Quién lo produce | Uso |
|---|---|---|---:|---:|---|---|
| `person_id` | texto | identificador (UUID) | 0.0 | 71514 | World Aquatics | llave: cruza al mismo nadador entre piscinas |
| `sexo` | texto | categórica: M / F | 0.0 | 2 | World Aquatics | estratificación; brecha entre sexos |
| `estilo` | texto | categórica: 5 estilos | 0.0 | 5 | World Aquatics | variable de agrupación principal |
| `distancia` | entero | metros: 50 / 100 / 200 / 400 | 0.0 | 4 | World Aquatics | determina las vueltas extra |
| `piscina` | texto | categórica: LCM (50 m) / SCM (25 m) | 0.0 | 2 | World Aquatics | los dos lados de la comparación |
| `tiempo` | texto | texto mm:ss.dd | 0.0 | 31360 | cronometraje oficial de la competencia | origen de tiempo_s |
| `tiempo_s` | decimal | segundos | 0.0 | 31360 | derivada por nosotros | variable de respuesta |
| `puntos_fina` | decimal | puntos (0 a 1100) | 0.0 | 1020 | World Aquatics | medida de nivel comparable entre pruebas |
| `rank` | entero | posición en el ranking mundial del año | 0.0 | 4988 | World Aquatics | control: verifica el tope de 5.000 |
| `edad` | decimal | años cumplidos a la fecha del nado | 6.4 | 70 | World Aquatics | descriptiva; no usada en el análisis |
| `fecha_nacimiento` | texto | fecha ISO | 6.4 | 7793 | World Aquatics | descriptiva |
| `pais` | texto | nombre del país | 0.0 | 215 | World Aquatics | descriptiva; ángulo Chile |
| `pais_codigo` | texto | código ISO de 3 letras | 0.0 | 213 | World Aquatics | descriptiva |
| `club` | texto | texto libre | 0.0 | 9346 | declarado por el nadador/federación | descriptiva; baja calidad |
| `fecha` | texto | fecha ISO del nado | 0.0 | 281 | organizador de la competencia | verifica que ambas marcas son de 2024 |
| `competencia` | texto | nombre del torneo | 0.0 | 307 | organizador | trazabilidad de cada marca |
| `ciudad` | texto | nombre de la ciudad | 0.0 | 221 | organizador | descriptiva |
| `medalla` | decimal | categórica: 1 oro, 2 plata, 3 bronce | 93.3 | 3 | World Aquatics | no usada |
| `result_id` | texto | identificador | 0.0 | 71514 | World Aquatics | NO identifica el nado (ver advertencia) |
| `event_id` | texto | identificador (UUID) | 0.0 | 310 | World Aquatics | NO identifica la competencia del nado |
| `discipline_id` | texto | identificador (UUID) | 0.0 | 24 | World Aquatics | identifica la prueba |

## Fuente 2 — Marcas mínimas, Mundial de 25 m Beijing 2026 (PDF oficial)

| Variable | Tipo | Unidad | Quién lo produce |
|---|---|---|---|
| Marca mínima A y B, por prueba y tipo de piscina | texto mm:ss.dd → segundos | segundos | World Aquatics |

## Variables construidas por nosotros

| Variable | Unidad | Definición |
|---|---|---|
| `tiempo_s_lcm` | segundos | marca del nadador en piscina de 50 m |
| `tiempo_s_scm` | segundos | marca del mismo nadador en piscina de 25 m |
| `diferencia_s` | segundos | tiempo_s_lcm − tiempo_s_scm |
| `factor_tiempo_s` | adimensional | tiempo_s_lcm / tiempo_s_scm entre las mejores marcas: la variable central |
| `vueltas_extra` | conteo | distancia / 50: virajes adicionales en piscina corta |
| `por_vuelta_s` | segundos por viraje | diferencia_s / vueltas_extra |
| `qt25_A_s, qt50_A_s` | segundos | marca mínima A de Beijing 2026, por tipo de piscina |
| `nivel` | adimensional | promedio de ambas marcas frente a la mínima A |

## Calidad de los datos (medida, no supuesta)

- **Sin duplicados**: la clave (`person_id`, `piscina`, `prueba`) identifica una fila; 115456 duplicados en 424.528 filas.
- **Sin tiempos inválidos**: 0 filas sin tiempo; el rango va de 19.90 s a 584.93 s, coherente con las pruebas incluidas.
- **`edad` incompleta**: 6.4% sin fecha de nacimiento, y 62 filas con edad mayor a 60 años (una de 119) más 2948 menores de 10. No usamos esta variable en el análisis; se documenta.
- **`club` con ausentes disfrazados**: 77.083 filas (18.2%) traen el texto literal `"No"` en vez de un valor faltante. Un conteo ingenuo de clubes los contaría como un club llamado "No".
- **`result_id` y `event_id` no identifican el nado**: son constantes para cada nadador (100% de los nadadores tienen un único `result_id` en todas sus filas, incluso en pruebas y piscinas distintas). Es un problema de la fuente, no del script: se verificó en la respuesta cruda de la API. Impide usar estos campos para ir a buscar los parciales de cada nado.
- **Pares con la piscina de 50 m más rápida**: 5.950 de 43.914 (13.5%). No son errores: son nadadores en distinta forma en cada temporada. Se conservan.
- **Valores extremos del factor**: de 0.3146 a 1.5056. Por eso se usa la mediana y no la media.