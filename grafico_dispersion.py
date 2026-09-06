"""Diagrama de caja del factor de conversion, por estilo.

El factor no es un numero unico por prueba: es una distribucion. Esta figura
muestra cuanta dispersion hay detras de cada mediana, con la tecnica de la
clase 2 (boxplot).

Bigotes en los percentiles 5 y 95, para que la lectura sea exacta y facil de
explicar: la caja contiene la mitad central de los nadadores y los bigotes,
el 90% central.

Uso:  uv run python capstone/grafico_dispersion.py
Salida: figura_dispersion.png
"""
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path

AQUI = Path(__file__).parent

AZUL = "#2a78d6"
SUP = "#fcfcfb"
TINTA = "#0b0b0b"
SEC = "#52514e"
MUDO = "#898781"
GRID = "#e1e0d9"

NOMBRE = {"FREESTYLE": "Libre", "BUTTERFLY": "Mariposa", "MEDLEY": "Combinado",
          "BREASTSTROKE": "Pecho", "BACKSTROKE": "Espalda"}

d = pd.read_csv(AQUI / "datos" / "pares_lcm_scm.csv")
d["pct"] = (d["factor"] - 1) * 100

orden = d.groupby("estilo").pct.median().sort_values().index.tolist()
datos = [d.loc[d.estilo == e, "pct"].values for e in orden]
etiquetas = [NOMBRE[e] for e in orden]

fig, eje = plt.subplots(figsize=(7.2, 3.9))
fig.patch.set_facecolor(SUP)
eje.set_facecolor(SUP)

caja = eje.boxplot(datos, vert=False, whis=(5, 95), showfliers=False,
                   widths=0.62, patch_artist=True, tick_labels=etiquetas)
for c in caja["boxes"]:
    c.set(facecolor=AZUL, alpha=0.75, edgecolor=AZUL, linewidth=1.2)
for c in caja["medians"]:
    c.set(color=SUP, linewidth=2.2)
for c in caja["whiskers"] + caja["caps"]:
    c.set(color=MUDO, linewidth=1.3)

# la mediana, escrita, a la derecha de cada caja
for i, e in enumerate(orden, start=1):
    m = d.loc[d.estilo == e, "pct"].median()
    n = (d.estilo == e).sum()
    eje.annotate(f"{m:.1f}%   n = {n:,}".replace(",", "."),
                 (9.6, i), fontsize=15, color=SEC, va="center")

eje.axvline(0, color="#c3c2b7", lw=1)
eje.set_xlim(-4.5, 14.5)
eje.set_xticks([-4, -2, 0, 2, 4, 6, 8])
eje.set_xlabel("% más lento en piscina de 50 m que en la de 25 m",
               fontsize=15.5, color=SEC, labelpad=8)
eje.grid(axis="x", color=GRID, lw=0.8)
eje.set_axisbelow(True)
for lado in ("top", "right", "left"):
    eje.spines[lado].set_visible(False)
eje.spines["bottom"].set_color("#c3c2b7")
eje.tick_params(axis="x", colors=MUDO, labelsize=15, length=0)
eje.tick_params(axis="y", labelsize=17, colors=TINTA, length=0)

fig.text(0.012, 0.955,
         "La caja es la mitad central; los bigotes, los percentiles 5 y 95",
         fontsize=13.5, color=SEC, ha="left")

fig.tight_layout(rect=[0, 0, 1, 0.905])
fig.savefig(AQUI / "figura_dispersion.png", dpi=220, facecolor=SUP)
print("ok:", AQUI / "figura_dispersion.png")
