"""Figura: exigencia oficial de World Aquatics vs. factor medido.

Lee datos/comparacion_wa.csv (lo produce factor_implicito_wa.py) y dibuja, por
prueba y sexo, cuanto mas lento se nada en piscina de 50 m segun cada fuente.

Uso:
    uv run python capstone/grafico_comparacion.py            # version con titulo
    uv run python capstone/grafico_comparacion.py --lamina   # sin titulo, para la ppt
"""
import sys
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

from pathlib import Path

AQUI = Path(__file__).parent
RUTA = AQUI / "datos" / "comparacion_wa.csv"
SALIDA = AQUI / "figura_comparacion.png"
SALIDA_LAMINA = AQUI / "figura_lamina.png"

LAMINA = "--lamina" in sys.argv

MEDIDO = "#2a78d6"      # categorical slot 1
OFICIAL = "#eb6834"     # categorical slot 2
SUP = "#fcfcfb"
TINTA = "#0b0b0b"
SEC = "#52514e"
MUDO = "#898781"
GRID = "#e1e0d9"

NOMBRE = {"FREESTYLE": "Libre", "BACKSTROKE": "Espalda", "BREASTSTROKE": "Pecho",
          "BUTTERFLY": "Mariposa", "MEDLEY": "Combinado"}

d = pd.read_csv(RUTA)
d["etiqueta"] = d["distancia"].astype(str) + " " + d["estilo"].map(NOMBRE)
# a porcentaje: cuanto mas lento se nada en piscina de 50 m
d["pct_medido"] = (d["factor_real"] - 1) * 100
d["pct_oficial"] = (d["factor_wa_A"] - 1) * 100

# mismo orden en ambos paneles: por el factor medido promedio de la prueba
orden = (d.groupby("etiqueta").pct_medido.mean()
          .sort_values().index.tolist())

alto = 4.75 if LAMINA else 5.8
fig, ejes = plt.subplots(1, 2, figsize=(11.5, alto), sharex=True, sharey=True)
fig.patch.set_facecolor(SUP)

for eje, sexo, titulo in zip(ejes, ["F", "M"], ["Mujeres", "Hombres"]):
    g = d[d.sexo == sexo].set_index("etiqueta").reindex(orden)
    y = range(len(orden))
    eje.set_facecolor(SUP)

    for yy, (_, f) in zip(y, g.iterrows()):
        eje.plot([f.pct_oficial, f.pct_medido], [yy, yy],
                 color=MUDO, lw=1.4, zorder=1, solid_capstyle="round")
    eje.scatter(g.pct_oficial, y, s=95, color=OFICIAL, zorder=3,
                edgecolors=SUP, linewidths=1.6)
    eje.scatter(g.pct_medido, y, s=95, color=MEDIDO, zorder=3,
                edgecolors=SUP, linewidths=1.6)

    eje.set_yticks(list(y))
    eje.set_yticklabels(orden, fontsize=11, color=TINTA)
    eje.set_title(titulo, fontsize=12.5, color=TINTA, fontweight="bold",
                  loc="left", pad=9)
    eje.grid(axis="x", color=GRID, lw=0.8)
    eje.set_axisbelow(True)
    for lado in ("top", "right", "left"):
        eje.spines[lado].set_visible(False)
    eje.spines["bottom"].set_color("#c3c2b7")
    eje.tick_params(axis="x", colors=MUDO, labelsize=10, length=0)
    eje.tick_params(axis="y", length=0)
    eje.set_xlim(-0.35, 6.9)
    eje.set_ylim(-0.7, len(orden) - 0.3)

# una sola etiqueta del eje x para los dos paneles
fig.text(0.5, 0.105 if LAMINA else 0.088,
         "% más lento en piscina de 50 m que en la de 25 m",
         fontsize=11, color=SEC, ha="center")

if not LAMINA:
    fig.suptitle("La equivalencia oficial no coincide con lo que hacen los nadadores",
                 fontsize=14.5, color=TINTA, fontweight="bold", x=0.008,
                 ha="left", y=0.988)
    fig.text(0.008, 0.930,
             "En naranja, cuánto más lenta supone World Aquatics que es la piscina "
             "de 50 m, al pedir una marca distinta en cada una.",
             fontsize=10.5, color=SEC, ha="left")
    fig.text(0.008, 0.893,
             "En azul, cuánto más lento nadan de verdad los 30.257 que compitieron "
             "en ambas durante 2024.",
             fontsize=10.5, color=SEC, ha="left")

leyenda = [Line2D([], [], marker="o", ls="", ms=9, mfc=OFICIAL, mec=SUP,
                  label="Exigencia oficial (World Aquatics)"),
           Line2D([], [], marker="o", ls="", ms=9, mfc=MEDIDO, mec=SUP,
                  label="Factor medido (2024)")]
fig.legend(handles=leyenda, loc="lower left", bbox_to_anchor=(0.008, -0.004),
           ncol=2, frameon=False, fontsize=10.5, labelcolor=TINTA,
           handletextpad=0.5, columnspacing=1.8)

fig.tight_layout(rect=[0, 0.135, 1, 0.985 if LAMINA else 0.862])
fig.savefig(SALIDA_LAMINA if LAMINA else SALIDA, dpi=220, facecolor=SUP)
print("ok:", SALIDA_LAMINA if LAMINA else SALIDA)
