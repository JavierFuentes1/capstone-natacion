"""Regenera las figuras del avance sobre la base definitiva (mensual, mejor marca).

Uso, desde ~/diplomado-cdd:  uv run python capstone/figuras_avance.py
Lee   datos/pares_mensual.csv  y  datos/comparacion_wa.csv
Deja  figuras_eda/4-1_histograma_factor.png
      figuras_eda/4-4_lineas_hipotesis.png
      figuras_eda/4-5_barras_brecha_wa.png
"""
import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

AQUI = os.path.dirname(os.path.abspath(__file__))
DATOS, FIGURAS = os.path.join(AQUI, "datos"), os.path.join(AQUI, "figuras_eda")
COLORES = {"FREESTYLE": "#0072B2", "BACKSTROKE": "#D55E00", "BREASTSTROKE": "#009E73",
           "BUTTERFLY": "#CC79A7", "MEDLEY": "#E69F00"}
NOMBRES = {"FREESTYLE": "Libre", "BACKSTROKE": "Espalda", "BREASTSTROKE": "Pecho",
           "BUTTERFLY": "Mariposa", "MEDLEY": "Combinado"}
ORDEN = ["FREESTYLE", "BUTTERFLY", "MEDLEY", "BREASTSTROKE", "BACKSTROKE"]
GRIS = "#6E878D"
plt.rcParams["figure.dpi"] = 110

d = pd.read_csv(os.path.join(DATOS, "pares_mensual.csv"),
                usecols=["sexo", "estilo", "distancia",
                         "factor_tiempo_s", "por_vuelta_tiempo_s"]) \
      .rename(columns={"factor_tiempo_s": "factor",
                       "por_vuelta_tiempo_s": "por_vuelta_s"})

# ---------------------------------------------------------------- 4-1
fig, ax = plt.subplots(figsize=(10, 4.5))
bordes = np.linspace(0.94, 1.13, 80)
alturas = {"M": .97, "F": .87}
lados = {"M": (8, "left"), "F": (-8, "right")}
for sexo, color, nom in [("M", "#0072B2", "Hombres"), ("F", "#E69F00", "Mujeres")]:
    v = d.loc[d["sexo"] == sexo, "factor"]
    ax.hist(v, bins=bordes, alpha=.62, color=color, label=nom, edgecolor="none")
    ax.axvline(v.median(), color=color, linestyle="--", linewidth=1.6)
    dx, ha = lados[sexo]
    ax.annotate(f"mediana {v.median():.3f}".replace(".", ","),
                (v.median(), alturas[sexo]), xycoords=("data", "axes fraction"),
                xytext=(dx, 0), textcoords="offset points", color=color, fontsize=9,
                ha=ha, va="top",
                bbox=dict(boxstyle="round,pad=0.2", facecolor="white", alpha=.75,
                          edgecolor="none"))
ax.axvline(1.0, color=GRIS, linewidth=1)
ax.annotate("igual tiempo en\nambas piscinas", (1.0, .55),
            xycoords=("data", "axes fraction"), xytext=(-10, 0),
            textcoords="offset points", color=GRIS, fontsize=8.5, ha="right")
ax.set_xlabel("Factor de conversión  t(50 m) / t(25 m)   (adimensional)")
ax.set_ylabel("Cantidad de nadadores")
ax.set_title("Casi todos los nadadores son más rápidos en piscina de 25 m,\n"
             "y los hombres ganan más que las mujeres", fontsize=12, loc="left")
ax.legend(frameon=False, loc="center right")
ax.grid(axis="y", alpha=.25)
ax.spines[["top", "right"]].set_visible(False)
ax.xaxis.set_major_formatter(lambda v, _: f"{v:.3f}".replace(".", ","))
plt.tight_layout()
fig.savefig(os.path.join(FIGURAS, "4-1_histograma_factor.png"))
plt.close(fig)

# ---------------------------------------------------------------- 4-4
fig, ejes = plt.subplots(1, 2, figsize=(12, 5), sharey=True)
for ax, sexo, tit in zip(ejes, ["M", "F"], ["Hombres", "Mujeres"]):
    g = d[d["sexo"] == sexo]
    for estilo in ORDEN:
        s = g[g["estilo"] == estilo].groupby("distancia")["por_vuelta_s"].median()
        if s.empty:
            continue
        ax.plot(s.index, s.values, marker="o", markersize=7, linewidth=2,
                color=COLORES[estilo], label=NOMBRES[estilo])
        ax.annotate(NOMBRES[estilo], (s.index[-1], s.values[-1]), xytext=(6, 0),
                    textcoords="offset points", color=COLORES[estilo], fontsize=9,
                    va="center")
    ax.set_title(tit, fontsize=11, loc="left")
    ax.set_xlabel("Distancia de la prueba (m)")
    ax.set_xticks([50, 100, 200, 400])
    ax.grid(alpha=.25)
    ax.spines[["top", "right"]].set_visible(False)
    ax.set_xlim(30, 520)
ejes[0].set_ylabel("Segundos ganados por vuelta extra (s, mediana)")
ejes[0].yaxis.set_major_formatter(lambda v, _: f"{v:.1f}".replace(".", ","))
fig.suptitle("Si una vuelta valiera siempre lo mismo, estas líneas serían planas "
             "y estarían juntas", fontsize=13, x=0.01, ha="left")
plt.tight_layout()
fig.savefig(os.path.join(FIGURAS, "4-4_lineas_hipotesis.png"))
plt.close(fig)

# ---------------------------------------------------------------- 4-5
comp = pd.read_csv(os.path.join(DATOS, "comparacion_wa.csv"))
comp["etiqueta"] = comp["prueba"] + " · " + comp["sexo"].map({"M": "hombres", "F": "mujeres"})
comp = comp.sort_values("brecha_s")
AZUL, NAR = "#0072B2", "#D55E00"
fig, ax = plt.subplots(figsize=(9.5, 8))
ax.barh(comp["etiqueta"], comp["brecha_s"],
        color=np.where(comp["brecha_s"] >= 0, NAR, AZUL), height=.72)
ax.axvline(0, color=GRIS, linewidth=1)
for y, v in enumerate(comp["brecha_s"]):
    ax.annotate(f"{v:+.2f}".replace(".", ","), (v, y),
                xytext=(7 if v >= 0 else -7, 0), textcoords="offset points",
                va="center", ha="left" if v >= 0 else "right",
                fontsize=8.5, color="#333333")
ax.set_xlabel("Segundos de más que regala la mínima oficial  (medido − exigido)")
ax.set_title("Dónde la tabla oficial se desvía de la equivalencia real\n"
             "Naranjo: la mínima es más fácil de cumplir en 25 m · Azul: en 50 m",
             fontsize=12, loc="left")
ax.set_xlim(comp["brecha_s"].min() - 1.1, comp["brecha_s"].max() + 1.1)
ax.grid(axis="x", alpha=.25)
ax.spines[["top", "right", "left"]].set_visible(False)
ax.tick_params(axis="y", length=0, labelsize=9)
ax.xaxis.set_major_formatter(lambda v, _: f"{v:.0f}".replace(".", ","))
plt.tight_layout()
fig.savefig(os.path.join(FIGURAS, "4-5_barras_brecha_wa.png"))
plt.close(fig)

print("Tres figuras regeneradas sobre la base mensual con la mejor marca.")
print(f"\nComparacion con World Aquatics:")
print(f"  mas faciles en 25 m : {(comp.brecha_s>0).sum()}")
print(f"  mas faciles en 50 m : {(comp.brecha_s<0).sum()}")
print(f"  brecha |mediana|    : {comp.brecha_s.abs().median():.2f} s")
print(f"  brecha < 0,3 s      : {(comp.brecha_s.abs()<0.3).sum()} de {len(comp)}")
print(f"  correlacion         : {comp[['factor_wa_A','factor_real']].corr().iloc[0,1]:.3f}")
print(f"  extremos            :")
print(comp.sort_values('brecha_s').iloc[[-1,-2,0]][['etiqueta','brecha_s']].to_string(index=False))
