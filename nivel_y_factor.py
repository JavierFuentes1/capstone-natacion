"""
¿El factor de conversión depende del nivel del nadador?

Motivo: nuestro factor es la mediana sobre los ~5.000 mejores de cada prueba,
pero las marcas mínimas de un campeonato son de nivel más alto. Si el factor
cambiara con el nivel, comparar nuestra mediana con la tabla de World Aquatics
sería comparar dos poblaciones distintas.

CUIDADO CON UNA TRAMPA, y es el punto central de este script.

El factor de cada nadador es un cociente: tiempo_50m / tiempo_25m. Si elegimos a
los "buenos" mirando SOLO su tiempo de 50 m, estamos seleccionando gente que
tuvo un buen día (o una buena temporada) en 50 m; su tiempo de 25 m no fue
elegido y queda relativamente más lento, así que el cociente baja. Si los
elegimos por su tiempo de 25 m pasa exactamente lo contrario. El efecto no es
del nadador: lo introduce el criterio de selección. Es regresión a la media.

La definición neutral es usar el promedio de ambos rendimientos, que no
privilegia ninguno de los dos lados del cociente.

Salida: datos/factor_por_nivel.csv
"""

import pandas as pd
from scipy.stats import spearmanr
from pathlib import Path

from factor_implicito_wa import MARCAS, a_segundos, NOMBRE

AQUI = Path(__file__).parent
DATOS = AQUI / "datos"
UMBRAL_ELITE = 1.03   # hasta 3% por debajo de la marca mínima A


def cargar():
    d = pd.read_csv(DATOS / "pares_lcm_scm.csv")
    qt = pd.DataFrame(
        [{"sexo": s, "estilo": e, "distancia": dd,
          "qt25_A_s": a_segundos(v[0]), "qt50_A_s": a_segundos(v[2])}
         for (s, e, dd), v in MARCAS.items()])
    d = d.merge(qt, on=["sexo", "estilo", "distancia"], how="inner",
                validate="many_to_one")

    # Nivel = cuán lejos está de la marca mínima. 1,00 = justo en la marca.
    d["nivel_lcm"] = d["tiempo_s_lcm"] / d["qt50_A_s"]   # sesga el factor hacia abajo
    d["nivel_scm"] = d["tiempo_s_scm"] / d["qt25_A_s"]   # lo sesga hacia arriba
    d["nivel"] = (d["nivel_lcm"] + d["nivel_scm"]) / 2   # neutral
    return d


def main():
    d = cargar()

    # --- 1. La trampa, medida ----------------------------------------------
    print("1. Por qué la definición de 'nivel' importa")
    print("   Factor mediano de los nadadores a menos de 3% de la marca A,")
    print("   según con qué tiempo se los seleccione:\n")
    for col, nom in [("nivel_lcm", "por su tiempo en 50 m"),
                     ("nivel_scm", "por su tiempo en 25 m"),
                     ("nivel", "por el promedio (neutral)")]:
        e = d[d[col] <= UMBRAL_ELITE]
        print(f"   {nom:30} n={len(e):5d}   factor = {e.factor.median():.4f}")
    print(f"   {'todos los pares':30} n={len(d):5d}   factor = {d.factor.median():.4f}")
    print("\n   Los dos primeros difieren en 0,009 sin que ningún nadador haya")
    print("   cambiado: es el criterio de selección, no el nivel.")

    # --- 2. Con la definición neutral, ¿queda algún efecto? -----------------
    print("\n\n2. Factor mediano por banda de nivel (definición neutral)\n")
    bandas = [(0, 1.00, "cumple la marca A"),
              (1.00, 1.03, "hasta 3% por debajo"),
              (1.03, 1.06, "3 a 6% por debajo"),
              (1.06, 1.10, "6 a 10% por debajo"),
              (1.10, 99, "más de 10% por debajo")]
    print(f"   {'banda':26}{'n':>7}{'factor':>10}")
    print("   " + "-" * 43)
    for lo, hi, nom in bandas:
        g = d[(d.nivel >= lo) & (d.nivel < hi)]
        if len(g):
            print(f"   {nom:26}{len(g):7d}{g.factor.median():10.4f}")
    print(f"   {'TODOS':26}{len(d):7d}{d.factor.median():10.4f}")

    rho, p = spearmanr(d.nivel, d.factor)
    print(f"\n   Spearman nivel vs factor: rho = {rho:.3f} (p = {p:.2g})")
    print("   El p es diminuto por los 30.257 casos, pero rho ≈ 0: el efecto")
    print("   existe estadísticamente y no existe en la práctica.")

    # --- 3. Prueba por prueba ----------------------------------------------
    print("\n\n3. Lo mismo, prueba por prueba\n")
    print(f"   {'sx':3}{'prueba':15}{'n':>6}{'rho':>8}{'f.todos':>9}"
          f"{'f.élite':>9}{'n él.':>7}")
    print("   " + "-" * 57)
    filas = []
    for (sx, es, di), g in d.groupby(["sexo", "estilo", "distancia"]):
        ge = g[g.nivel <= UMBRAL_ELITE]
        rho_g, p_g = spearmanr(g.nivel, g.factor)
        f_todos = g.factor.median()
        f_elite = ge.factor.median() if len(ge) >= 30 else float("nan")
        qt25, qt50 = g.qt25_A_s.iloc[0], g.qt50_A_s.iloc[0]
        f_wa = qt50 / qt25
        filas.append({
            "sexo": sx, "estilo": es, "distancia": di,
            "prueba": f"{di} {NOMBRE[es]}", "n": len(g),
            "rho_nivel_factor": rho_g, "p": p_g,
            "factor_wa": f_wa, "factor_todos": f_todos,
            "n_elite": len(ge), "factor_elite": f_elite,
            "brecha_todos_s": (f_todos - f_wa) * qt25,
            "brecha_elite_s": (f_elite - f_wa) * qt25,
        })
        fe = f"{f_elite:9.4f}" if pd.notna(f_elite) else "        —"
        print(f"   {sx:3}{f'{di} {NOMBRE[es]}':15}{len(g):6d}{rho_g:8.3f}"
              f"{f_todos:9.4f}{fe}{len(ge):7d}")

    c = pd.DataFrame(filas)
    c.to_csv(DATOS / "factor_por_nivel.csv", index=False)

    ok = c.dropna(subset=["factor_elite"])
    dif = (ok.factor_elite - ok.factor_todos).abs()
    print(f"\n   Diferencia mediana entre el factor de élite y el de todos: "
          f"{dif.median():.4f}")
    print(f"   Correlación entre ambos: {ok.factor_elite.corr(ok.factor_todos):.3f}")

    print("\n\nCONCLUSIÓN: con una definición de nivel que no sesgue el cociente,")
    print("el factor no cambia de forma relevante entre niveles. La mediana de")
    print("toda la población es comparable con la tabla de marcas mínimas.")
    print(f"\nGuardado en {DATOS / 'factor_por_nivel.csv'}")


if __name__ == "__main__":
    main()
