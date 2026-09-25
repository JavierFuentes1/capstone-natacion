"""Primer modelo del informe de avance: la diferencia entre piscinas explicada
por las vueltas extra, estimada por estilo y sexo.

    diferencia_s = b0 + b1 * vueltas_extra + e

b1 es la ventaja por vuelta de ese estilo; b0 dice si hay algo mas en juego
ademas de las vueltas. Se estima con minimos cuadrados y numpy, sin statsmodels,
para no agregar dependencias: la formula cerrada de la regresion simple y de la
multiple con dummies es la misma que se vio en las clases 4 y 5.

Uso, desde ~/diplomado-cdd:   uv run python capstone/modelo_avance.py
Lee   datos/pares_lcm_scm.csv  (no versionado; lo genera 03_eda_capstone.ipynb)
Deja  figuras_eda/6-1_modelo_pendientes.png  y  datos/modelo_pendientes.csv
"""

import os
import numpy as np
import pandas as pd
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
Z = 1.96          # normal al 95%; con n > 1.500 por celda la t es indistinguible


def ols(X, y):
    """Devuelve (coeficientes, errores estandar, R2, n)."""
    XtX = X.T @ X
    b = np.linalg.solve(XtX, X.T @ y)
    r = y - X @ b
    n, k = X.shape
    s2 = (r @ r) / (n - k)
    se = np.sqrt(np.diag(s2 * np.linalg.inv(XtX)))
    r2 = 1 - (r @ r) / ((y - y.mean()) ** 2).sum()
    return b, se, r2, n


def por_estilo_y_sexo(d):
    filas = []
    for (sexo, estilo), g in d.groupby(["sexo", "estilo"]):
        X = np.column_stack([np.ones(len(g)), g["vueltas_extra"].values])
        b, se, r2, n = ols(X, g["diferencia_s"].values)
        filas.append({
            "sexo": sexo, "estilo": estilo, "n": n,
            "distancias": g["distancia"].nunique(),
            "b1": b[1], "b1_lo": b[1] - Z * se[1], "b1_hi": b[1] + Z * se[1],
            "b0": b[0], "b0_lo": b[0] - Z * se[0], "b0_hi": b[0] + Z * se[0],
            "r2": r2,
        })
    return pd.DataFrame(filas)


def con_interaccion(d, sexo):
    """Modelo multiple con dummies de estilo e interaccion, como en la clase 4.
    Categoria base: Libre."""
    g = d[d["sexo"] == sexo]
    v = g["vueltas_extra"].values
    cols, nombres = [np.ones(len(g)), v], ["intercepto", "vueltas_extra"]
    for estilo in ORDEN[1:]:
        dm = (g["estilo"] == estilo).astype(float).values
        cols += [dm, dm * v]
        nombres += [f"d_{NOMBRES[estilo]}", f"v x {NOMBRES[estilo]}"]
    b, se, r2, n = ols(np.column_stack(cols), g["diferencia_s"].values)
    return nombres, b, se, r2, n


def figura(tab, salida):
    fig, ax = plt.subplots(figsize=(9.6, 5.0))
    etiquetas, posiciones = [], []
    y = 0
    for estilo in ORDEN:
        for sexo, marca, relleno in [("M", "o", True), ("F", "o", False)]:
            f = tab[(tab.estilo == estilo) & (tab.sexo == sexo)].iloc[0]
            color = COLORES[estilo]
            ax.plot([f.b1_lo, f.b1_hi], [y, y], color=color, linewidth=2.6,
                    solid_capstyle="round", alpha=.9)
            ax.plot([f.b1], [y], marker=marca, markersize=9, color=color,
                    markerfacecolor=color if relleno else "white",
                    markeredgewidth=1.8, zorder=3)
            ax.annotate(f"{f.b1:.2f}".replace(".", ","), (f.b1_hi, y), xytext=(8, 0),
                        textcoords="offset points", va="center", fontsize=9,
                        color="#333333")
            etiquetas.append(f"{NOMBRES[estilo]} · {'hombres' if sexo == 'M' else 'mujeres'}")
            posiciones.append(y)
            y += 1
        y += 0.6

    ax.set_yticks(posiciones)
    ax.set_yticklabels(etiquetas, fontsize=10)
    ax.invert_yaxis()
    ax.set_xlabel("Segundos ganados por cada vuelta extra  (pendiente $\\beta_1$, con su intervalo de 95%)")
    ax.xaxis.set_major_formatter(lambda v, _: f"{v:.1f}".replace(".", ","))
    ax.set_title("Cada vuelta extra vale entre 0,9 y 2,0 segundos según el estilo\n"
                 "Los intervalos de libre y de espalda ni se rozan: la diferencia entre estilos no es ruido",
                 fontsize=12.5, loc="left")
    ax.grid(axis="x", alpha=.25)
    ax.spines[["top", "right", "left"]].set_visible(False)
    ax.tick_params(axis="y", length=0)
    ax.set_xlim(0.75, 2.22)
    ax.annotate("● hombres    ○ mujeres", (0.995, 0.965), xycoords="axes fraction",
                ha="right", va="top", fontsize=9.5, color=GRIS)
    plt.tight_layout()
    fig.savefig(salida, dpi=160)
    print("Figura guardada en", salida)


def main():
    d = pd.read_csv(os.path.join(DATOS, "pares_lcm_scm.csv"),
                    usecols=["sexo", "estilo", "distancia", "diferencia_s",
                             "factor", "vueltas_extra"])
    print(f"Pares: {len(d):,}   ·   factor mediano global: {d['factor'].median():.4f}\n")

    tab = por_estilo_y_sexo(d)
    print("diferencia_s ~ vueltas_extra, por estilo y sexo")
    print(f"{'sexo':5}{'estilo':11}{'n':>7}{'b1 (s/vuelta)':>15}{'IC 95%':>20}"
          f"{'b0 (s)':>9}{'IC 95%':>19}{'R2':>7}{'dist':>6}")
    for _, f in tab.iterrows():
        print(f"{f.sexo:5}{NOMBRES[f.estilo]:11}{f.n:>7,}{f.b1:>15.4f}"
              f"   [{f.b1_lo:>5.3f}, {f.b1_hi:>5.3f}]{f.b0:>9.3f}"
              f"   [{f.b0_lo:>5.2f}, {f.b0_hi:>5.2f}]{f.r2:>7.3f}{f.distancias:>6}")

    X = np.column_stack([np.ones(len(d)), d["vueltas_extra"].values])
    b, se, r2, n = ols(X, d["diferencia_s"].values)
    print(f"\nModelo global sobre las 24 pruebas juntas  (n = {n:,}, R2 = {r2:.3f})")
    print(f"   b1 = {b[1]:.4f} s por vuelta extra   IC 95% [{b[1]-Z*se[1]:.4f}, {b[1]+Z*se[1]:.4f}]")
    print(f"   b0 = {b[0]:.4f} s                    IC 95% [{b[0]-Z*se[0]:.4f}, {b[0]+Z*se[0]:.4f}]")
    print("   b0 distinto de cero: las vueltas extra no explican toda la diferencia.")

    for sexo in ["M", "F"]:
        nombres, b, se, r2, n = con_interaccion(d, sexo)
        print(f"\nModelo con interaccion vueltas_extra x estilo · "
              f"{'hombres' if sexo == 'M' else 'mujeres'}  (n = {n:,}, R2 = {r2:.3f}, base: Libre)")
        for nm, bb, ss in zip(nombres, b, se):
            estrella = "  *" if abs(bb / ss) > 1.96 else "   "
            print(f"   {nm:18}{bb:>9.4f}   IC 95% [{bb-Z*ss:>7.3f}, {bb+Z*ss:>7.3f}]"
                  f"   t = {bb/ss:>7.1f}{estrella}")

    os.makedirs(FIGURAS, exist_ok=True)
    tab.to_csv(os.path.join(DATOS, "modelo_pendientes.csv"), index=False)
    figura(tab, os.path.join(FIGURAS, "6-1_modelo_pendientes.png"))


if __name__ == "__main__":
    main()
