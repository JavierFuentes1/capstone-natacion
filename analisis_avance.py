"""Analisis del informe de avance, sobre la base definitiva del proyecto.

DECISIONES DEL EQUIPO (20-sep-2026)
  1. La base es la MENSUAL: 424.528 nados, 43.914 pares (descarga_temporadas.py).
  2. El factor se calcula con la MEJOR MARCA del anio de cada nadador
     (columna factor_tiempo_s), porque las marcas minimas se cumplen con un solo
     nado. La mediana del anio queda como analisis de sensibilidad aparte.
  3. Los tiempos imposibles NO se eliminan: el filtro por segundos por metro
     queda desactivado, como lo dejo Javier. Se declara como limitacion.

Uso, desde ~/diplomado-cdd:   uv run python capstone/analisis_avance.py
Lee   datos/pares_mensual.csv          (no versionado)
Deja  datos/factores_por_prueba.csv    factor e intervalo por prueba
      datos/modelo_pendientes.csv      coeficientes del modelo
      figuras_eda/6-1_modelo_pendientes.png
"""

import os
import numpy as np
import pandas as pd
from scipy import stats
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

AQUI = os.path.dirname(os.path.abspath(__file__))
DATOS = os.path.join(AQUI, "datos")
FIGURAS = os.path.join(AQUI, "figuras_eda")

NOMBRES = {"FREESTYLE": "Libre", "BACKSTROKE": "Espalda", "BREASTSTROKE": "Pecho",
           "BUTTERFLY": "Mariposa", "MEDLEY": "Combinado"}
COLORES = {"FREESTYLE": "#0072B2", "BACKSTROKE": "#D55E00", "BREASTSTROKE": "#009E73",
           "BUTTERFLY": "#CC79A7", "MEDLEY": "#E69F00"}
ORDEN = ["FREESTYLE", "MEDLEY", "BUTTERFLY", "BREASTSTROKE", "BACKSTROKE"]
GRIS = "#6E878D"
Z = 1.96
B = 2000


def titulo(t):
    print("\n" + "=" * 78)
    print(t)
    print("=" * 78)


def cargar():
    cols = ["sexo", "estilo", "distancia", "vueltas_extra",
            "tiempo_s_lcm", "tiempo_s_scm",
            "factor_tiempo_s", "diferencia_tiempo_s", "por_vuelta_tiempo_s",
            "factor_tiempo_mediana"]
    d = pd.read_csv(os.path.join(DATOS, "pares_mensual.csv"), usecols=cols)
    # Nombres cortos, como en la entrega del 15-sep
    return d.rename(columns={"factor_tiempo_s": "factor",
                             "diferencia_tiempo_s": "diferencia_s",
                             "por_vuelta_tiempo_s": "por_vuelta_s"})


def ols(X, y):
    XtX = X.T @ X
    b = np.linalg.solve(XtX, X.T @ y)
    r = y - X @ b
    n, k = X.shape
    se = np.sqrt(np.diag(((r @ r) / (n - k)) * np.linalg.inv(XtX)))
    r2 = 1 - (r @ r) / ((y - y.mean()) ** 2).sum()
    return b, se, r2, n


def ic_bootstrap(x, semilla=0):
    r = np.random.default_rng(semilla)
    x = np.asarray(x)
    m = np.array([np.median(r.choice(x, size=len(x), replace=True)) for _ in range(B)])
    return np.percentile(m, [2.5, 97.5])


def main():
    d = cargar()

    titulo("1. LA BASE")
    print(f"Pares                        : {len(d):,}")
    print(f"Factor mediano (mejor marca) : {d['factor'].median():.4f}")
    print(f"Factor mediano (mediana anio): {d['factor_tiempo_mediana'].median():.4f}"
          "   <- solo como referencia de sensibilidad")
    al_reves = (d["diferencia_s"] < 0).sum()
    print(f"Pares con la piscina de 50 m mas rapida: {al_reves:,} "
          f"({al_reves / len(d):.1%})")

    titulo("2. FACTOR POR PRUEBA, CON INTERVALO DEL 95% (bootstrap, B=2000)")
    filas = []
    for (sx, es, di), g in d.groupby(["sexo", "estilo", "distancia"]):
        bajo, alto = ic_bootstrap(g["factor"].values)
        filas.append({"sexo": sx, "estilo": es, "distancia": di, "n": len(g),
                      "factor": g["factor"].median(), "ic_bajo": bajo, "ic_alto": alto,
                      "dif_mediana_s": g["diferencia_s"].median(),
                      "por_vuelta_s": g["por_vuelta_s"].median()})
    f = pd.DataFrame(filas).sort_values("factor").reset_index(drop=True)
    f["ancho"] = f["ic_alto"] - f["ic_bajo"]
    f["prueba"] = (f["distancia"].astype(str) + " " + f["estilo"].map(NOMBRES) + " "
                   + f["sexo"].map({"M": "hombres", "F": "mujeres"}))
    print(f[["prueba", "n", "factor", "ic_bajo", "ic_alto", "ancho",
             "por_vuelta_s"]].to_string(index=False,
                                        float_format=lambda v: f"{v:.4f}"))
    a, b_ = f.iloc[0], f.iloc[-1]
    print(f"\nMenor: {a.prueba}  {a.factor:.4f}  [{a.ic_bajo:.4f}, {a.ic_alto:.4f}]")
    print(f"Mayor: {b_.prueba}  {b_.factor:.4f}  [{b_.ic_bajo:.4f}, {b_.ic_alto:.4f}]")
    print(f"Se solapan los extremos: {a.ic_alto >= b_.ic_bajo}")
    print(f"Razon entre ventajas: {(b_.factor - 1) / (a.factor - 1):.1f} veces")
    f.drop(columns="prueba").to_csv(os.path.join(DATOS, "factores_por_prueba.csv"),
                                    index=False)

    titulo("3. FACTOR POR ESTILO Y SEXO")
    piv = (d.groupby(["sexo", "estilo"])["factor"].median().unstack()[ORDEN]
             .rename(columns=NOMBRES).round(4))
    print(piv.to_string())
    por_estilo = d.groupby("estilo")["factor"].median()
    print(f"\nMayor: {NOMBRES[por_estilo.idxmax()]} ({por_estilo.max():.4f})  ·  "
          f"menor: {NOMBRES[por_estilo.idxmin()]} ({por_estilo.min():.4f})  ·  "
          f"razon {(por_estilo.max()-1)/(por_estilo.min()-1):.1f} veces")

    titulo("4. LA VENTAJA CRECE CON LA DISTANCIA?")
    filas = []
    for (sx, es), g in d.groupby(["sexo", "estilo"]):
        m = g.groupby("distancia")[["factor", "por_vuelta_s"]].median().sort_index()
        if len(m) < 2:
            continue
        filas.append({"sexo": sx, "estilo": NOMBRES[es], "distancias": len(m),
                      "factor_crece": bool(m["factor"].is_monotonic_increasing),
                      "por_vuelta_crece": bool(m["por_vuelta_s"].is_monotonic_increasing)})
    mono = pd.DataFrame(filas)
    print(mono.to_string(index=False))
    print(f"\nEl factor crece en {mono.factor_crece.sum()} de {len(mono)} casos.")
    print(f"Los segundos por vuelta crecen en {mono.por_vuelta_crece.sum()} de {len(mono)}.")
    r, pr = stats.pearsonr(d["factor"], d["distancia"])
    rho, pp = stats.spearmanr(d["factor"], d["distancia"])
    print(f"\nfactor vs distancia:  Pearson {r:+.3f} (p={pr:.1e})  ·  "
          f"Spearman {rho:+.3f} (p={pp:.1e})")

    titulo("5. BRECHA ENTRE SEXOS (Mann-Whitney, prueba por prueba)")
    filas = []
    for (es, di), g in d.groupby(["estilo", "distancia"]):
        m, w = g[g.sexo == "M"]["factor"], g[g.sexo == "F"]["factor"]
        if len(m) < 30 or len(w) < 30:
            continue
        u, p = stats.mannwhitneyu(m, w)
        filas.append({"prueba": f"{di} {NOMBRES[es]}", "n_M": len(m), "n_F": len(w),
                      "factor_M": m.median(), "factor_F": w.median(),
                      "diferencia": m.median() - w.median(), "p": p})
    br = pd.DataFrame(filas).sort_values("diferencia", ascending=False)
    print(br.assign(p=br["p"].map(lambda v: f"{v:.1e}")).to_string(
        index=False, float_format=lambda v: f"{v:.4f}"))
    print(f"\nHombres con mayor factor: {(br.diferencia > 0).sum()} de {len(br)}")
    print(f"Significativas al 5%    : {(br.p < 0.05).sum()} de {len(br)}")
    print(f"El mayor de los {len(br)} valores p: {br.p.max():.1e}")
    print(f"Diferencias: de {br.diferencia.min():.4f} a {br.diferencia.max():.4f}")

    titulo("6. EL EFECTO DEL NIVEL ES UN ARTEFACTO DE SELECCION?")
    g = d.groupby(["sexo", "estilo", "distancia"])
    d["pct_lcm"] = g["tiempo_s_lcm"].rank(pct=True)
    d["pct_scm"] = g["tiempo_s_scm"].rank(pct=True)
    d["pct_neutral"] = (d["pct_lcm"] + d["pct_scm"]) / 2
    for col, nom in [("pct_lcm", "nivel por su tiempo en 50 m"),
                     ("pct_scm", "nivel por su tiempo en 25 m"),
                     ("pct_neutral", "nivel por el promedio (neutral)")]:
        rho, p = stats.spearmanr(d["factor"], d[col])
        print(f"  {nom:36} rho = {rho:+.3f}  (p = {p:.1e})")
    print("\nFactor mediano del 10% mas rapido, segun como se lo elija:")
    for col, nom in [("pct_lcm", "por su tiempo en 50 m"),
                     ("pct_scm", "por su tiempo en 25 m"),
                     ("pct_neutral", "por el promedio (neutral)")]:
        e = d[d[col] <= 0.10]
        print(f"  {nom:28} n = {len(e):6,}   factor = {e['factor'].median():.4f}")
    print(f"  {'todos los pares':28} n = {len(d):6,}   factor = {d['factor'].median():.4f}")

    titulo("7. EL PRIMER MODELO:  diferencia_s = b0 + b1 * vueltas_extra")
    filas = []
    for (sx, es), g in d.groupby(["sexo", "estilo"]):
        X = np.column_stack([np.ones(len(g)), g["vueltas_extra"].values])
        b, se, r2, n = ols(X, g["diferencia_s"].values)
        filas.append({"sexo": sx, "estilo": es, "n": n,
                      "b1": b[1], "b1_lo": b[1] - Z*se[1], "b1_hi": b[1] + Z*se[1],
                      "b0": b[0], "b0_lo": b[0] - Z*se[0], "b0_hi": b[0] + Z*se[0],
                      "r2": r2})
    tab = pd.DataFrame(filas)
    print(f"{'sexo':5}{'estilo':11}{'n':>7}{'b1 (s/vuelta)':>15}{'IC 95%':>20}"
          f"{'b0 (s)':>9}{'IC 95%':>19}{'R2':>7}")
    for _, x in tab.sort_values("b1").iterrows():
        print(f"{x.sexo:5}{NOMBRES[x.estilo]:11}{x.n:>7,}{x.b1:>15.4f}"
              f"   [{x.b1_lo:>5.3f}, {x.b1_hi:>5.3f}]{x.b0:>9.3f}"
              f"   [{x.b0_lo:>5.2f}, {x.b0_hi:>5.2f}]{x.r2:>7.3f}")

    X = np.column_stack([np.ones(len(d)), d["vueltas_extra"].values])
    b, se, r2, n = ols(X, d["diferencia_s"].values)
    print(f"\nModelo global (n = {n:,}, R2 = {r2:.3f})")
    print(f"   b1 = {b[1]:.4f} s por vuelta   IC 95% [{b[1]-Z*se[1]:.4f}, {b[1]+Z*se[1]:.4f}]")
    print(f"   b0 = {b[0]:.4f} s              IC 95% [{b[0]-Z*se[0]:.4f}, {b[0]+Z*se[0]:.4f}]")

    for sx in ["M", "F"]:
        g = d[d["sexo"] == sx]
        v = g["vueltas_extra"].values
        cols, nom = [np.ones(len(g)), v], ["intercepto", "vueltas_extra"]
        for es in ORDEN[1:]:
            dm = (g["estilo"] == es).astype(float).values
            cols += [dm, dm * v]
            nom += [f"d_{NOMBRES[es]}", f"v x {NOMBRES[es]}"]
        b, se, r2, n = ols(np.column_stack(cols), g["diferencia_s"].values)
        print(f"\nCon interaccion · {'hombres' if sx=='M' else 'mujeres'} "
              f"(n = {n:,}, R2 = {r2:.3f}, base: Libre)")
        for nm, bb, ss in zip(nom, b, se):
            est = "  *" if abs(bb/ss) > Z else "   "
            print(f"   {nm:18}{bb:>9.4f}  IC 95% [{bb-Z*ss:>7.3f}, {bb+Z*ss:>7.3f}]{est}")

    tab.to_csv(os.path.join(DATOS, "modelo_pendientes.csv"), index=False)

    # ---- figura de pendientes ----
    fig, ax = plt.subplots(figsize=(9.6, 5.0))
    etiquetas, posiciones, y = [], [], 0
    for estilo in ORDEN:
        for sexo, relleno in [("M", True), ("F", False)]:
            x = tab[(tab.estilo == estilo) & (tab.sexo == sexo)].iloc[0]
            c = COLORES[estilo]
            ax.plot([x.b1_lo, x.b1_hi], [y, y], color=c, linewidth=2.6,
                    solid_capstyle="round", alpha=.9)
            ax.plot([x.b1], [y], marker="o", markersize=9, color=c,
                    markerfacecolor=c if relleno else "white", markeredgewidth=1.8, zorder=3)
            ax.annotate(f"{x.b1:.2f}".replace(".", ","), (x.b1_hi, y), xytext=(8, 0),
                        textcoords="offset points", va="center", fontsize=9, color="#333333")
            etiquetas.append(f"{NOMBRES[estilo]} · {'hombres' if sexo=='M' else 'mujeres'}")
            posiciones.append(y); y += 1
        y += 0.6
    ax.set_yticks(posiciones); ax.set_yticklabels(etiquetas, fontsize=10)
    ax.invert_yaxis()
    ax.set_xlabel("Segundos ganados por cada vuelta extra  "
                  "(pendiente $\\beta_1$, con su intervalo de 95%)")
    lo_, hi_ = tab.b1.min(), tab.b1.max()
    ax.set_title(f"Cada vuelta extra vale entre {lo_:.1f} y {hi_:.1f} segundos según el estilo\n"
                 "Los intervalos de libre y de espalda ni se rozan: "
                 "la diferencia entre estilos no es ruido".replace(".", ","),
                 fontsize=12.5, loc="left")
    ax.grid(axis="x", alpha=.25)
    ax.spines[["top", "right", "left"]].set_visible(False)
    ax.tick_params(axis="y", length=0)
    ax.set_xlim(tab.b1_lo.min() - 0.12, tab.b1_hi.max() + 0.22)
    ax.xaxis.set_major_formatter(lambda v, _: f"{v:.1f}".replace(".", ","))
    ax.annotate("● hombres    ○ mujeres", (0.995, 0.965), xycoords="axes fraction",
                ha="right", va="top", fontsize=9.5, color=GRIS)
    plt.tight_layout()
    fig.savefig(os.path.join(FIGURAS, "6-1_modelo_pendientes.png"), dpi=160)
    print("\nFigura guardada en figuras_eda/6-1_modelo_pendientes.png")


if __name__ == "__main__":
    main()
