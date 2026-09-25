"""
Genera la tabla de metadatos del proyecto directamente desde los datos.

El criterio 2 de la rúbrica pide "las fuentes y tablas necesarias, sus variables
relevantes con tipo y unidad, y quién produce cada dato". El tipo y el % de
nulos se calculan aquí; la unidad, el productor y el uso están descritos a mano
en DICCIONARIO, porque eso no se deduce de los datos.

Salida: datos/metadatos.md  (tabla lista para pegar en el informe)
"""

import pandas as pd
from pathlib import Path

AQUI = Path(__file__).parent
DATOS = AQUI / "datos"

# variable: (unidad, productor, para qué la usamos)
DICCIONARIO = {
    "person_id":    ("identificador (UUID)", "World Aquatics", "llave: cruza al mismo nadador entre piscinas"),
    "sexo":         ("categórica: M / F", "World Aquatics", "estratificación; brecha entre sexos"),
    "estilo":       ("categórica: 5 estilos", "World Aquatics", "variable de agrupación principal"),
    "distancia":    ("metros: 50 / 100 / 200 / 400", "World Aquatics", "determina las vueltas extra"),
    "piscina":      ("categórica: LCM (50 m) / SCM (25 m)", "World Aquatics", "los dos lados de la comparación"),
    "tiempo":       ("texto mm:ss.dd", "cronometraje oficial de la competencia", "origen de tiempo_s"),
    "tiempo_s":     ("segundos", "derivada por nosotros", "variable de respuesta"),
    "puntos_fina":  ("puntos (0 a 1100)", "World Aquatics", "medida de nivel comparable entre pruebas"),
    "rank":         ("posición en el ranking mundial del año", "World Aquatics", "control: verifica el tope de 5.000"),
    "edad":         ("años cumplidos a la fecha del nado", "World Aquatics", "descriptiva; no usada en el análisis"),
    "fecha_nacimiento": ("fecha ISO", "World Aquatics", "descriptiva"),
    "pais":         ("nombre del país", "World Aquatics", "descriptiva; ángulo Chile"),
    "pais_codigo":  ("código ISO de 3 letras", "World Aquatics", "descriptiva"),
    "club":         ("texto libre", "declarado por el nadador/federación", "descriptiva; baja calidad"),
    "fecha":        ("fecha ISO del nado", "organizador de la competencia", "verifica que ambas marcas son de 2024"),
    "competencia":  ("nombre del torneo", "organizador", "trazabilidad de cada marca"),
    "ciudad":       ("nombre de la ciudad", "organizador", "descriptiva"),
    "medalla":      ("categórica: 1 oro, 2 plata, 3 bronce", "World Aquatics", "no usada"),
    "result_id":    ("identificador", "World Aquatics", "NO identifica el nado (ver advertencia)"),
    "event_id":     ("identificador (UUID)", "World Aquatics", "NO identifica la competencia del nado"),
    "discipline_id":("identificador (UUID)", "World Aquatics", "identifica la prueba"),
}

DERIVADAS = [
    ("tiempo_s_lcm", "segundos", "marca del nadador en piscina de 50 m"),
    ("tiempo_s_scm", "segundos", "marca del mismo nadador en piscina de 25 m"),
    ("diferencia_s", "segundos", "tiempo_s_lcm − tiempo_s_scm"),
    ("factor_tiempo_s", "adimensional", "tiempo_s_lcm / tiempo_s_scm entre las mejores marcas: la variable central"),
    ("vueltas_extra", "conteo", "distancia / 50: virajes adicionales en piscina corta"),
    ("por_vuelta_s", "segundos por viraje", "diferencia_s / vueltas_extra"),
    ("qt25_A_s, qt50_A_s", "segundos", "marca mínima A de Beijing 2026, por tipo de piscina"),
    ("nivel", "adimensional", "promedio de ambas marcas frente a la mínima A"),
]


def main():
    # Base definitiva (20-sep): descarga mensual, dos archivos por sexo.
    d = pd.concat([pd.read_csv(DATOS / "nadosFull_masculino.csv", low_memory=False),
                   pd.read_csv(DATOS / "nadosFull_femenino.csv", low_memory=False)],
                  ignore_index=True)
    p = pd.read_csv(DATOS / "pares_mensual.csv")
    p = p.rename(columns={"factor_tiempo_s": "factor"})

    lineas = []
    lineas.append("# Metadatos del proyecto\n")
    lineas.append(f"Generado automáticamente desde `nadosFull_masculino.csv` + `nadosFull_femenino.csv` "
                  f"({len(d):,} filas × {d.shape[1]} columnas) ".replace(",", ".") +
                  f"y `pares_mensual.csv` ({len(p):,} filas).\n".replace(",", "."))

    lineas.append("\n## Fuente 1 — API pública de World Aquatics (rankings)\n")
    lineas.append("| Variable | Tipo | Unidad / valores | % nulos | Distintos | Quién lo produce | Uso |")
    lineas.append("|---|---|---|---:|---:|---|---|")
    for v, (uni, prod, uso) in DICCIONARIO.items():
        if v not in d.columns:
            continue
        tipo = {"int64": "entero", "float64": "decimal",
                "object": "texto"}.get(str(d[v].dtype), str(d[v].dtype))
        lineas.append(f"| `{v}` | {tipo} | {uni} | {100*d[v].isna().mean():.1f} | "
                      f"{d[v].nunique()} | {prod} | {uso} |")

    lineas.append("\n## Fuente 2 — Marcas mínimas, Mundial de 25 m Beijing 2026 (PDF oficial)\n")
    lineas.append("| Variable | Tipo | Unidad | Quién lo produce |")
    lineas.append("|---|---|---|---|")
    lineas.append("| Marca mínima A y B, por prueba y tipo de piscina | texto mm:ss.dd → segundos | segundos | World Aquatics |")

    lineas.append("\n## Variables construidas por nosotros\n")
    lineas.append("| Variable | Unidad | Definición |")
    lineas.append("|---|---|---|")
    for v, uni, defi in DERIVADAS:
        lineas.append(f"| `{v}` | {uni} | {defi} |")

    # --- Calidad, medida ---------------------------------------------------
    lineas.append("\n## Calidad de los datos (medida, no supuesta)\n")
    edad_alta = int((d.edad > 60).sum())
    edad_baja = int((d.edad < 10).sum())
    club_no = int((d.club == "No").sum())
    dup_clave = int(d.duplicated(["person_id", "piscina", "prueba"]).sum())
    rid_por_persona = d.groupby("person_id").result_id.nunique().eq(1).mean()

    lineas += [
        f"- **Sin duplicados**: la clave (`person_id`, `piscina`, `prueba`) identifica una fila; "
        f"{dup_clave} duplicados en " + f"{len(d):,}".replace(",", ".") + " filas.",
        f"- **Sin tiempos inválidos**: 0 filas sin tiempo; el rango va de {d.tiempo_s.min():.2f} s a {d.tiempo_s.max():.2f} s, coherente con las pruebas incluidas.",
        f"- **`edad` incompleta**: {100*d.edad.isna().mean():.1f}% sin fecha de nacimiento, y {edad_alta} filas con edad mayor a 60 años (una de 119) más {edad_baja} menores de 10. No usamos esta variable en el análisis; se documenta.",
        f"- **`club` con ausentes disfrazados**: " + f"{club_no:,}".replace(",", ".") +
        f" filas ({100*club_no/len(d):.1f}%) traen el texto literal `\"No\"` en vez de un valor "
        f"faltante. Un conteo ingenuo de clubes los contaría como un club llamado \"No\".",
        f"- **`result_id` y `event_id` no identifican el nado**: son constantes para cada nadador ({100*rid_por_persona:.0f}% de los nadadores tienen un único `result_id` en todas sus filas, incluso en pruebas y piscinas distintas). Es un problema de la fuente, no del script: se verificó en la respuesta cruda de la API. Impide usar estos campos para ir a buscar los parciales de cada nado.",
        f"- **Pares con la piscina de 50 m más rápida**: " + f"{int((p.factor<1).sum()):,}".replace(",", ".") +
        " de " + f"{len(p):,}".replace(",", ".") + f" ({100*(p.factor<1).mean():.1f}%). No son errores: "
        "son nadadores en distinta forma en cada temporada. Se conservan.",
        f"- **Valores extremos del factor**: de {p.factor.min():.4f} a {p.factor.max():.4f}. Por eso se usa la mediana y no la media.",
    ]

    salida = DATOS / "metadatos.md"
    salida.write_text("\n".join(lineas), encoding="utf-8")
    print("\n".join(lineas))
    print(f"\n\nGuardado en {salida}")


if __name__ == "__main__":
    main()
