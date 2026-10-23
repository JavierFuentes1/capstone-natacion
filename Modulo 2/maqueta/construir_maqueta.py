"""Arma la maqueta del dashboard: Modulo 2/maqueta_dashboard.html.

Junta en una sola página la plantilla (plantilla.html), el mapa base
(countries-110m.json, de world-atlas 2.0.2, licencia ISC; Natural Earth, dominio
público) y los datos agregados que calcula este script desde datos/. La página
no lleva ninguna fila a nivel nadador.

Todo va separado por sexo: "T" (todos), "F" y "M", para el filtro del tablero.
Requiere haber corrido base_federaciones.py. Uso, desde la raíz del repositorio:

    python "Modulo 2/maqueta/construir_maqueta.py"
"""
import json
from pathlib import Path
import numpy as np
import pandas as pd

AQUI = Path(__file__).parent
R = AQUI.parents[1]; D = R / "datos"; OUT = AQUI.parent / "maqueta_dashboard.html"
b = pd.read_csv(D / "base_dashboard.csv", low_memory=False)
paises = pd.read_csv(D / "paises.csv")
nombre = dict(zip(paises.pais_codigo, paises.pais_nombre))
MIN_NAD, MIN_INTL, MIN_FEDS = 30, 10, 5
SEXOS = ["T", "F", "M"]
KPIS = ["pctB", "pctExt", "pctPod"]
ESTILO = {"FREESTYLE": "libre", "BACKSTROKE": "espalda", "BREASTSTROKE": "pecho",
          "BUTTERFLY": "mariposa", "MEDLEY": "combinado"}

kt = pd.read_csv(D / "kpi_federacion_semestre.csv").assign(sexo="T")
ks = pd.read_csv(D / "kpi_federacion_sexo_semestre.csv")
k = pd.concat([kt, ks], ignore_index=True)
e = k[(k.cobertura == "con torneos locales") & (k.nadadores >= MIN_NAD)]
sede = (b.drop_duplicates("id_nadador").groupby("federacion")
          .nivel_imputacion.apply(lambda s: (s == "sede").mean()))

feds = [{
    "sx": r.sexo, "fed": r.federacion, "nombre": nombre.get(r.federacion, r.federacion),
    "cont": r.continente, "sem": r.semestre, "nad": int(r.nadadores),
    "conB": int(r.con_minima_B), "ext": int(r.compitieron_exterior),
    "intl": int(r.compitieron_internacional), "podio": int(r.con_podio_internacional),
    "pctB": round(r.pct_con_minima_B, 4), "pctExt": round(r.pct_exterior, 4),
    "pctPod": None if r.compitieron_internacional < MIN_INTL else round(r.pct_con_podio_internacional, 4),
    "km": None if pd.isna(r.km_mediana_viaje) else int(r.km_mediana_viaje),
    "pctSede": round(float(sede.get(r.federacion, np.nan)), 3),
} for r in e.itertuples()]
F = pd.DataFrame(feds)

# Cuartiles: del continente si tiene >= 5 federaciones comparables; si no, del mundo.
cuart = {}
for (sx, sem), g in F.groupby(["sx", "sem"]):
    for kpi in KPIS:
        mundo = g[g[kpi].notna()][kpi]
        for cont in F.cont.dropna().unique():
            v = g[(g.cont == cont) & g[kpi].notna()][kpi]
            usa = v if len(v) >= MIN_FEDS else mundo
            cuart[f"{sx}|{sem}|{cont}|{kpi}"] = {
                "p25": round(usa.quantile(.25), 4), "p50": round(usa.quantile(.5), 4),
                "p75": round(usa.quantile(.75), 4), "n": int(len(usa)),
                "ref": "continente" if len(v) >= MIN_FEDS else "mundo", "nCont": int(len(v))}

def por_sexo(df, sx):
    return df if sx == "T" else df[df.sexo == sx]

comparables = set(F.fed)
flujos, sedes, mes_mundo, mes_fed, piscina, km_cont, h_cont, totales = [], [], {}, {}, {}, {}, {}, {}
meses = sorted(b.mes.unique())
for sx in SEXOS:
    bs = por_sexo(b, sx)
    v = bs[bs.exterior & bs.sede_lat.notna()].drop_duplicates(["id_nadador", "competencia"])
    fl = (v[v.federacion.isin(comparables)].groupby(["federacion", "semestre", "ciudad", "sede_pais_codigo"])
            .agg(n=("id_nadador", "nunique"), km=("km_desde_base", "first"), h=("husos_aprox", "first"),
                 lat=("sede_lat", "first"), lon=("sede_lon", "first")).reset_index())
    flujos += [{"sx": sx, "fed": r.federacion, "sem": r.semestre, "ciudad": r.ciudad, "pais": r.sede_pais_codigo,
                "n": int(r.n), "km": int(r.km), "h": int(r.h), "lat": round(r.lat, 3), "lon": round(r.lon, 3)}
               for r in fl.itertuples()]
    s = (bs[bs.sede_lat.notna()].groupby(["semestre", "ciudad", "sede_pais_codigo"])
           .agg(n=("id_nadador", "nunique"), torneos=("competencia", "nunique"),
                feds=("federacion", "nunique"), lat=("sede_lat", "first"), lon=("sede_lon", "first"))
           .reset_index())
    sedes += [{"sx": sx, "sem": r.semestre, "ciudad": r.ciudad, "pais": r.sede_pais_codigo, "n": int(r.n),
               "torneos": int(r.torneos), "feds": int(r.feds), "lat": round(r.lat, 3), "lon": round(r.lon, 3)}
              for r in s.itertuples()]
    m = bs.groupby(["mes", "piscina"]).size().unstack(fill_value=0).reindex(meses, fill_value=0)
    mes_mundo[sx] = {p: [int(x) for x in m[p]] for p in ["LCM", "SCM"]}
    mf = (bs[bs.federacion.isin(comparables)].groupby(["federacion", "mes", "piscina"]).size()
            .unstack(fill_value=0).reindex(columns=["LCM", "SCM"], fill_value=0))
    mes_fed[sx] = {}
    for f in mf.index.get_level_values(0).unique():
        t = mf.loc[f].reindex(meses, fill_value=0)
        mes_fed[sx][f] = {p: [int(x) for x in t[p]] for p in ["LCM", "SCM"]}
    cumple = bs[bs.cumple_B].drop_duplicates(["id_nadador", "estilo", "distancia", "piscina"])
    pz = (bs.groupby("federacion").agg(nad=("id_nadador", "nunique"), p25=("piscina", lambda q: (q == "SCM").mean()),
                                       cont=("continente", "first"))
            .join(cumple.groupby("federacion").agg(min25=("piscina", lambda q: (q == "SCM").mean()),
                                                   nmin=("id_nadador", "nunique")))
            .query("nad >= @MIN_NAD and nmin >= 5").dropna())
    piscina[sx] = [{"fed": f, "cont": r.cont, "nad": int(r.nad), "p25": round(r.p25, 3),
                    "min25": round(r.min25, 3), "nmin": int(r.nmin)} for f, r in pz.iterrows()]
    vb = bs[bs.exterior].drop_duplicates(["id_nadador", "competencia"])
    km_cont[sx] = {c: {q: int(g.km_desde_base.quantile(x)) for q, x in
                       [("p10", .1), ("p25", .25), ("p50", .5), ("p75", .75), ("p90", .9)]}
                   for c, g in vb.groupby("continente")}
    h_cont[sx] = {c: round(float(g.husos_aprox.median()), 1) for c, g in vb.groupby("continente")}
    totales[sx] = {"nados": int(len(bs)), "nadadores": int(bs.id_nadador.nunique()),
                   "federaciones": int(bs.federacion.nunique()), "sedes": int(bs.ciudad.nunique())}

# Pruebas: ¿se logran más mínimas en 25 m de lo que se nada en 25 m? Y la brecha del informe.
b["prueba"] = b.distancia.astype(str) + " " + b.estilo
cu = b[b.cumple_B].drop_duplicates(["id_nadador", "prueba", "piscina"])
cm = pd.read_csv(D / "comparacion_wa.csv")
brecha = {(r.sexo, f"{r.distancia} {r.estilo}"): round(r.brecha_s, 2) for r in cm.itertuples()}
pruebas = []
for p, g in b.groupby("prueba"):
    dist, est = p.split(" ")
    fila = {"prueba": f"{dist} {ESTILO[est]}", "dist": int(dist), "est": ESTILO[est]}
    for sx in ["F", "M"]:
        gs, ms = g[g.sexo == sx], cu[(cu.prueba == p) & (cu.sexo == sx)]
        n25, m25 = (gs.piscina == "SCM").mean(), (ms.piscina == "SCM").mean()
        fila[sx] = {"ratio": round(m25 / n25, 3), "n25": round(n25, 3), "m25": round(m25, 3),
                    "nB": int(ms.id_nadador.nunique()), "brecha": brecha.get((sx, p))}
    pruebas.append(fila)
x = pd.DataFrame([{"r": f[s]["ratio"], "g": f[s]["brecha"]} for f in pruebas for s in ["F", "M"]])
corr = {"spearman": round(x.r.corr(x.g, method="spearman"), 2), "pearson": round(x.r.corr(x.g), 2)}

tor = pd.read_csv(D / "torneos.csv")
alcance = tor.groupby("alcance").agg(torneos=("competencia", "size"), part=("n_nadadores", "sum")).reset_index()
bases = {}
for f, r in b[b.federacion.isin(comparables)].groupby("federacion").agg(
        ciudad=("ciudad_base", "first"), lat=("lat_base", "first"), lon=("lon_base", "first")).iterrows():
    bases[f] = {"ciudad": r.ciudad if isinstance(r.ciudad, str) else "centro del país",
                "lat": round(r.lat, 3), "lon": round(r.lon, 3)}

datos = {"feds": feds, "cuartiles": cuart, "flujos": flujos, "bases": bases, "sedes": sedes,
         "mesMundo": mes_mundo, "mesFed": mes_fed, "meses": meses, "piscina": piscina,
         "kmCont": km_cont, "husosCont": h_cont, "pruebas": pruebas, "corr": corr,
         "alcance": alcance.to_dict("records"), "totales": totales,
         "param": {"torneos": int(len(tor)), "revisar": int(tor.revisar.sum()),
                   "minNad": MIN_NAD, "minIntl": MIN_INTL, "minFeds": MIN_FEDS}}
def incrustar(texto):
    return texto.replace("</", "<\\/")      # que ningún dato cierre el <script>


plantilla = (AQUI / "plantilla.html").read_text(encoding="utf-8")
pagina = (plantilla
          .replace("__DATOS__", incrustar(json.dumps(datos, ensure_ascii=False, separators=(",", ":"))))
          .replace("__MUNDO__", incrustar((AQUI / "countries-110m.json").read_text(encoding="utf-8"))))
OUT.write_text(pagina, encoding="utf-8")
print(f"{OUT.name}: {OUT.stat().st_size/1024:.0f} KB · feds {len(feds)} · flujos {len(flujos)} · "
      f"sedes {len(sedes)} · Spearman {corr['spearman']}")
