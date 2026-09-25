"""Figuras nuevas del informe de avance (propuesta del 24-sep).

Uso, desde ~/diplomado-cdd:  uv run python capstone/figuras_informe.py
Lee   datos/factores_por_prueba.csv   (versionado; lo genera analisis_avance.py)
      datos/pares_mensual.csv         (opcional: solo para recalcular el factor global)
Deja  figuras_eda/1-1_esquema_virajes.png   el viraje, para la seccion de contexto
      figuras_eda/4-0_factores_ic.png       los 24 factores con su intervalo del 95%
"""
import os
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrowPatch

AQUI = os.path.dirname(os.path.abspath(__file__))
DATOS, FIGURAS = os.path.join(AQUI, "datos"), os.path.join(AQUI, "figuras_eda")
NOMBRES = {"FREESTYLE": "Libre", "BACKSTROKE": "Espalda", "BREASTSTROKE": "Pecho",
           "BUTTERFLY": "Mariposa", "MEDLEY": "Combinado"}
AZUL, NARANJA = "#0072B2", "#E69F00"      # hombres, mujeres: los mismos del histograma
GRIS, TINTA, AGUA = "#6E878D", "#222222", "#DCEBF3"
SUB = "#0A3D5C"                            # fase bajo el agua tras la pared
coma = lambda v, d=4: f"{v:.{d}f}".replace(".", ",")


# ------------------------------------------------------------- 1-1 esquema
# 100 m en cada piscina. Arriba, vista cenital del recorrido; abajo, los mismos
# 100 m "desenrollados": cada pared da un impulso y una fase bajo el agua de hasta
# 15 m (el limite reglamentario en libre, espalda y mariposa).
BAJO_AGUA = 15

fig = plt.figure(figsize=(10, 4.4))
gs = fig.add_gridspec(2, 2, width_ratios=[1, 2.1], height_ratios=[1, 1],
                      wspace=0.08, hspace=0.55)

filas = [("Piscina de 50 m", 50, [50]), ("Piscina de 25 m", 25, [25, 50, 75])]
for i, (nombre, largo, paredes) in enumerate(filas):
    # --- vista cenital, a escala: la piscina de 25 m mide la mitad
    ax = fig.add_subplot(gs[i, 0])
    ax.add_patch(Rectangle((0, 0), largo, 10, facecolor=AGUA, edgecolor=GRIS, lw=1))
    vueltas = 100 // largo
    # cada largo va en su propia altura, para que los virajes no se dibujen encima
    ys = [8.8 - k * 7.6 / (vueltas - 1) for k in range(vueltas)]
    for k in range(vueltas):
        x0, x1 = (0, largo) if k % 2 == 0 else (largo, 0)
        ax.add_patch(FancyArrowPatch((x0 + (1.5 if k % 2 == 0 else -1.5), ys[k]),
                                     (x1 + (-1.5 if k % 2 == 0 else 1.5), ys[k]),
                                     arrowstyle="-|>", mutation_scale=9,
                                     color=TINTA, lw=1.2))
    for k in range(vueltas - 1):
        x, ym = (largo if k % 2 == 0 else 0), (ys[k] + ys[k + 1]) / 2
        ax.plot([x], [ym], marker="o", ms=9, color=SUB, zorder=3)
        ax.annotate(str(k + 1), (x, ym), ha="center", va="center", fontsize=7,
                    color="white", fontweight="bold", zorder=4)
    ax.set_xlim(-2, 52); ax.set_ylim(-1, 11)
    ax.set_aspect("equal"); ax.axis("off")
    ax.set_title(f"{nombre}: {vueltas} largos, {vueltas - 1} "
                 f"viraje{'s' if vueltas > 2 else ''}", fontsize=10, loc="left",
                 color=TINTA)

    # --- los 100 m desenrollados
    ax = fig.add_subplot(gs[i, 1])
    ax.add_patch(Rectangle((0, 0), 100, 1, facecolor=AGUA, edgecolor="none"))
    for x in [0] + paredes:
        ax.add_patch(Rectangle((x, 0), BAJO_AGUA, 1, facecolor=SUB, edgecolor="white",
                               lw=1.5))
    for x in paredes:
        ax.plot([x, x], [-0.2, 1.2], color=TINTA, lw=1.6)
    superficie = 100 - BAJO_AGUA * (len(paredes) + 1)
    ax.annotate(f"hasta {BAJO_AGUA * (len(paredes) + 1)} m con impulso de pared  ·  "
                f"al menos {superficie} m nadando en superficie",
                (100, 1.4), ha="right", va="bottom", fontsize=9, color=TINTA)
    ax.set_xlim(0, 100); ax.set_ylim(-0.3, 2.0)
    ax.set_yticks([])
    ax.spines[["top", "right", "left"]].set_visible(False)
    ax.set_xticks([0, 25, 50, 75, 100])
    ax.tick_params(axis="x", labelsize=9, colors=GRIS)
    if i == 1:
        ax.set_xlabel("Distancia recorrida en una prueba de 100 m (m)", fontsize=9.5)

fig.suptitle("La piscina de 25 m obliga a dos virajes más en 100 m, y cada pared da "
             "un tramo más rápido que nadar", fontsize=12, x=0.01, y=1.04, ha="left",
             color=TINTA)
# Leyenda propia, bajo el titulo: con los parches reales en vez de caracteres
leyenda = [Rectangle((0, 0), 1, 1, facecolor=SUB),
           Rectangle((0, 0), 1, 1, facecolor=AGUA),
           plt.Line2D([], [], color=TINTA, lw=1.6)]
fig.legend(leyenda, ["salida o viraje: impulso y fase bajo el agua (máx. 15 m)",
                     "nado en superficie", "pared"],
           loc="upper left", bbox_to_anchor=(0.01, 0.985), ncol=3, frameon=False,
           fontsize=8.5, handlelength=1.4, labelcolor=GRIS)
fig.savefig(os.path.join(FIGURAS, "1-1_esquema_virajes.png"), dpi=200,
            bbox_inches="tight")
plt.close(fig)


# ------------------------------------------------------------- 4-0 factores con IC
f = pd.read_csv(os.path.join(DATOS, "factores_por_prueba.csv"))
ruta_pares = os.path.join(DATOS, "pares_mensual.csv")
if os.path.exists(ruta_pares):
    GLOBAL = pd.read_csv(ruta_pares, usecols=["factor_tiempo_s"])["factor_tiempo_s"].median()
else:
    GLOBAL = 1.0318   # mediana de los 43.914 pares, impresa por analisis_avance.py

f["prueba"] = f["distancia"].astype(str) + " " + f["estilo"].map(NOMBRES)
orden = f.groupby("prueba")["factor"].mean().sort_values().index.tolist()
y = {p: i for i, p in enumerate(orden)}
contienen = ((f["ic_bajo"] <= GLOBAL) & (f["ic_alto"] >= GLOBAL)).sum()

fig, ax = plt.subplots(figsize=(9.2, 6.0))
ax.axvline(GLOBAL, color=GRIS, lw=1.3, ls="--", zorder=1)
ax.annotate(f"factor único, todos juntos: {coma(GLOBAL)}", (GLOBAL, len(orden) - 0.35),
            xytext=(6, 0), textcoords="offset points", fontsize=9, color=GRIS,
            va="center")
for sexo, color, nom, dy in [("M", AZUL, "Hombres", 0.17), ("F", NARANJA, "Mujeres", -0.17)]:
    g = f[f["sexo"] == sexo]
    yy = g["prueba"].map(y) + dy
    ax.hlines(yy, g["ic_bajo"], g["ic_alto"], color=color, lw=2.4, zorder=2)
    ax.plot(g["factor"], yy, "o", ms=6.5, color=color, zorder=3, label=nom,
            markeredgecolor="white", markeredgewidth=0.8)
# Solo los dos extremos llevan su numero: son los que cita el texto
for (sx, p), dy_txt in [(("F", "100 Mariposa"), -5), (("M", "200 Espalda"), 0)]:
    x = f[(f["sexo"] == sx) & (f["prueba"] == p)].iloc[0]
    ax.annotate(f"{coma(x['factor'])}  [{coma(x['ic_bajo'])}–{coma(x['ic_alto'])}]",
                (x["ic_alto"], y[p] + (0.17 if sx == "M" else -0.17)), xytext=(8, dy_txt),
                textcoords="offset points", ha="left", va="center", fontsize=8.5,
                color=TINTA)

ax.set_yticks(range(len(orden))); ax.set_yticklabels(orden, fontsize=10)
ax.set_ylim(-0.7, len(orden) - 0.1)
ax.set_xlabel("Factor de conversión  t(50 m) / t(25 m)  (adimensional; "
              "mediana e intervalo del 95% por bootstrap)", fontsize=9.5)
ax.xaxis.set_major_formatter(lambda v, _: coma(v, 2))
ax.set_xlim(1.006, 1.064)
ax.grid(axis="x", alpha=.25)
ax.spines[["top", "right", "left"]].set_visible(False)
ax.tick_params(axis="y", length=0)
ax.legend(frameon=False, loc="lower right", fontsize=9.5)
ax.set_title(f"Un factor único no representa a las pruebas: solo {contienen} de los 24 "
             f"intervalos lo contienen\ny en las 12 pruebas el de los hombres queda a la "
             f"derecha del de las mujeres", fontsize=12, loc="left", color=TINTA)
plt.tight_layout()
fig.savefig(os.path.join(FIGURAS, "4-0_factores_ic.png"), dpi=200)
plt.close(fig)
print(f"Listo. Intervalos que contienen el factor global: {contienen} de {len(f)}")
