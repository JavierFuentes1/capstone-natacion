"""
Base del dashboard por federación (Módulo 2, Evaluación 2) y primeros KPI.

Parte de la base mensual v2 (descarga_temporadas.py) y de los complementos
(descarga_complementos.py) y construye:

  1. La federación de cada nadador. El 82% viene con país "CLB" (inscrito por
     club), así que se imputa en cascada y se guarda el nivel usado:
       oficial -> país del participante, si no es CLB ni neutral
       club    -> país del club
       sede    -> país donde compite con más frecuencia
  2. El tipo de cada torneo (alcance y categoría de edad), por reglas sobre el
     nombre más la diversidad de federaciones medida. Se puede corregir a mano
     en datos/torneos_override.csv (columnas: competencia, alcance, categoria).
  3. Si cada nado fue en el exterior, a cuántos km de la ciudad base de la
     federación y con qué diferencia horaria aproximada.
  4. Si cada nado cumple la marca mínima A o B de Beijing 2026, usada como
     "torneo genérico" (las mínimas 2024 se agregan después).

Salidas:
  datos/base_dashboard.csv          un nado por fila, ANONIMIZADO (no se versiona)
  datos/torneos.csv                 clasificación de los 307 torneos
  datos/kpi_federacion_semestre.csv KPI por federación y semestre
  datos/kpi_continente_semestre.csv los mismos KPI por continente
  datos/kpi_*_sexo_semestre.csv     las dos anteriores, separadas por sexo

Uso:  python base_federaciones.py
"""

import re
from pathlib import Path

import numpy as np
import pandas as pd

from factor_implicito_wa import MARCAS, a_segundos

AQUI = Path(__file__).parent
DATOS = AQUI / "datos"

# Códigos que no son una federación: atletas neutrales (rusos y bielorrusos desde
# 2023) y el inscrito por club. Para ellos manda el país del club.
NO_FEDERACION = {"CLB", "NAB", "AIN", "ANA"}

MIN_NADADORES_KPI = 10      # bajo esto un porcentaje por federación es ruido
MIN_FEDERACIONES_INTERNACIONAL = 10   # un meeting cuenta como internacional desde aquí


# ---------------------------------------------------------------------------
# 1. Federación imputada
# ---------------------------------------------------------------------------

def moda(s):
    s = s.dropna()
    return s.mode().iat[0] if len(s) else None


def imputar_federacion(d):
    valido = lambda s: s.where(~s.isin(NO_FEDERACION) & s.notna())
    d = d.assign(_n1=valido(d.pais_codigo), _n2=valido(d.club_pais_codigo))
    g = d.groupby("person_id")
    per = pd.DataFrame({
        "n1": g._n1.agg(moda),
        "n2": g._n2.agg(moda),
        "n3": g.sede_pais_codigo.agg(moda),
    })
    per["federacion"] = per.n1.fillna(per.n2).fillna(per.n3)
    per["nivel_imputacion"] = np.select(
        [per.n1.notna(), per.n2.notna()], ["oficial", "club"], default="sede")

    # Validación: donde hay dos fuentes, ¿coinciden?
    ambos = per.n1.notna() & per.n2.notna()
    solo_club = per.n1.isna() & per.n2.notna()
    print("Federación imputada:")
    print(per.nivel_imputacion.value_counts(normalize=True).round(3).to_string())
    print(f"  oficial = club donde existen ambos:       {(per.n1 == per.n2)[ambos].mean():.1%}")
    print(f"  club = país modal de sede (nivel club):   {(per.n2 == per.n3)[solo_club].mean():.1%}")
    return per[["federacion", "nivel_imputacion"]]


# ---------------------------------------------------------------------------
# 2. Tipo de torneo
# ---------------------------------------------------------------------------

REGLAS_ALCANCE = [   # (alcance, patrón), en orden: gana la primera que calza
    ("mundial", r"Olympic Games|World Aquatics (Swimming )?Championships|World Cup"),
    ("continental", r"European Junior|LEN Championships|CCCAN|CARIFTA|Asian Age Group|"
                    r"SEA Age Group|Africa Aquatics|African Games|CANA Championships|"
                    r"Pan Pacific|Panam|OSA Championships|Nordic|Baltic States|Children of Asia"),
    ("escolar-universitario", r"High[- ]School|Inter-College|BUCS|NCAA|Intercollegiate|"
                              r"Secondary School"),
    ("regional", r"\bQLD\b|\bNSW\b|\bWA Swimming|Ulster|Sectional|R[ée]gion|Kanagawa|"
                 r"West Short|East Short|Catalunya|Catalana|Emilia|Stavropol|Auckland|"
                 r"Western Festival|Division 1|Coupe du Qu[ée]bec|Southern California|"
                 r"Futures|Interclub|Club Championships|Dual Meet|Superleague|"
                 r"Vereinsmeisterschaften|Team Championships|Spanish Cup"),
    ("nacional", r"Trial|Selection|Selectivo|National|Championship|Campeonato|Campionato|"
                 r"Criteria|\bSM\b|\bDM\b|Nacional|Juveniles|Rep[uú]blica|Bikarkeppni|"
                 r"Age Group|Junior Olympic|Hong Kong Games|Festival of Sport"),
]
PATRON_JUVENIL = r"\bAge\b|Junior|\bJr\b|Youth|Juvenil|Giovanili|High[- ]School|Children|" \
                 r"Infantil|Secondary|CARIFTA"
PATRON_ABSOLUTO = r"Senior|Absolut|\bOpen\b"


def clasificar_torneos(d):
    t = (d.groupby("competencia")
           .agg(sede_pais_codigo=("sede_pais_codigo", moda),
                n_nadadores=("person_id", "nunique"),
                n_federaciones=("federacion", "nunique"),
                piscina=("piscina", moda))
           .reset_index())

    def alcance(nombre, n_fed):
        for etiqueta, patron in REGLAS_ALCANCE:
            if re.search(patron, nombre, flags=re.I):
                return etiqueta
        return "internacional"            # meetings abiertos, copas, grand prix

    t["alcance"] = [alcance(n, f) for n, f in zip(t.competencia, t.n_federaciones)]
    juvenil = t.competencia.str.contains(PATRON_JUVENIL, case=False, regex=True)
    absoluto = t.competencia.str.contains(PATRON_ABSOLUTO, case=False, regex=True)
    t["categoria"] = np.where(juvenil & ~absoluto, "juvenil",
                              np.where(juvenil & absoluto, "mixta", "absoluta"))

    # Contraste con lo medido: un "nacional" con muchas federaciones, o un
    # "internacional" casi sin extranjeros, se marca para revisión manual.
    t["revisar"] = (((t.alcance.isin(["nacional", "regional"])) & (t.n_federaciones >= 15))
                    | ((t.alcance == "internacional") & (t.n_federaciones <= 2)))

    override = DATOS / "torneos_override.csv"
    if override.exists():
        o = pd.read_csv(override).set_index("competencia")
        for col in ("alcance", "categoria"):
            if col in o:
                t[col] = t.competencia.map(o[col]).fillna(t[col])
        t.loc[t.competencia.isin(o.index), "revisar"] = False
        print(f"Torneos: {len(o)} correcciones manuales aplicadas")

    # "Internacional" para los KPI se decide por lo medido, no solo por el nombre:
    # un meeting abierto donde compiten casi solo locales (Japan Open: 3 federaciones)
    # inflaba los podios internacionales del anfitrión.
    t["internacional"] = (t.alcance.isin(["mundial", "continental"])
                          | ((t.alcance == "internacional")
                             & (t.n_federaciones >= MIN_FEDERACIONES_INTERNACIONAL)))
    print("Torneos por alcance:", t.alcance.value_counts().to_dict(),
          "| para revisar:", int(t.revisar.sum()))
    return t


# ---------------------------------------------------------------------------
# 3. Distancia y diferencia horaria
# ---------------------------------------------------------------------------

def haversine_km(lat1, lon1, lat2, lon2):
    lat1, lon1, lat2, lon2 = map(np.radians, (lat1, lon1, lat2, lon2))
    a = (np.sin((lat2 - lat1) / 2) ** 2
         + np.cos(lat1) * np.cos(lat2) * np.sin((lon2 - lon1) / 2) ** 2)
    return 6371.0 * 2 * np.arcsin(np.sqrt(a))


def ciudad_base(d, sedes, paises_coord):
    """Origen de cada federación: su sede local más usada; si no tiene, el centro del país."""
    local = d[d.sede_pais_codigo == d.federacion]
    base = (local.groupby(["federacion", "ciudad"]).size().rename("n").reset_index()
                 .sort_values("n", ascending=False).drop_duplicates("federacion")
                 .merge(sedes, left_on=["ciudad", "federacion"],
                        right_on=["ciudad", "sede_pais_codigo"], how="left")
                 [["federacion", "ciudad", "lat", "lon"]]
                 .rename(columns={"ciudad": "ciudad_base", "lat": "lat_base", "lon": "lon_base"}))
    todas = pd.DataFrame({"federacion": d.federacion.dropna().unique()})
    base = todas.merge(base, on="federacion", how="left")
    centro = paises_coord.set_index("pais_codigo")
    sin = base.lat_base.isna()
    base.loc[sin, "lat_base"] = base.loc[sin, "federacion"].map(centro.lat)
    base.loc[sin, "lon_base"] = base.loc[sin, "federacion"].map(centro.lon)
    base["origen"] = np.where(sin, "centro del país", "sede local más usada")
    return base


# ---------------------------------------------------------------------------
# 4. Marcas mínimas (Beijing 2026 como torneo genérico)
# ---------------------------------------------------------------------------

def tabla_minimas():
    filas = []
    for (sexo, estilo, dist), (a25, b25, a50, b50) in MARCAS.items():
        filas.append((sexo, estilo, dist, "SCM", a_segundos(a25), a_segundos(b25)))
        filas.append((sexo, estilo, dist, "LCM", a_segundos(a50), a_segundos(b50)))
    return pd.DataFrame(filas, columns=["sexo", "estilo", "distancia", "piscina",
                                        "minima_A_s", "minima_B_s"])


# ---------------------------------------------------------------------------
# 5. KPI
# ---------------------------------------------------------------------------

def kpis(b, por):
    """KPI por `por` (federación o continente) y semestre, a nivel de nadador."""
    g = b.groupby(por + ["semestre"])
    nad = g.id_nadador.nunique().rename("nadadores")
    con_a = b[b.cumple_A].groupby(por + ["semestre"]).id_nadador.nunique().rename("con_minima_A")
    con_b = b[b.cumple_B].groupby(por + ["semestre"]).id_nadador.nunique().rename("con_minima_B")
    ext = b[b.exterior].groupby(por + ["semestre"]).id_nadador.nunique().rename("compitieron_exterior")
    # KPI 3 sobre torneos internacionales ABSOLUTOS: los de grupos de edad (Asian Age
    # Group, CARIFTA) reparten medallas por categoría y un nadador junta muchas.
    intl = b[b.torneo_internacional & (b.torneo_categoria != "juvenil")]
    en_intl = intl.groupby(por + ["semestre"]).id_nadador.nunique().rename("compitieron_internacional")
    con_podio = intl[intl.medalla.isin([1, 2, 3])]
    podiadores = (con_podio.groupby(por + ["semestre"]).id_nadador.nunique()
                  .rename("con_podio_internacional"))
    # Un mismo nado puede repetirse si el nadador tuvo dos registros en la ventana:
    # el podio se cuenta una vez por nadador, prueba, piscina y torneo.
    podios = (con_podio.drop_duplicates(["id_nadador", "estilo", "distancia", "piscina", "competencia"])
              .groupby(por + ["semestre"]).size().rename("podios_internacionales"))
    km = (b[b.exterior].drop_duplicates(["id_nadador", "competencia"])
          .groupby(por + ["semestre"]).km_desde_base.median().rename("km_mediana_viaje"))
    k = pd.concat([nad, con_a, con_b, ext, en_intl, podiadores, podios, km], axis=1).fillna(
        {"con_minima_A": 0, "con_minima_B": 0, "compitieron_exterior": 0,
         "compitieron_internacional": 0, "con_podio_internacional": 0,
         "podios_internacionales": 0}).reset_index()
    k["pct_con_minima_B"] = k.con_minima_B / k.nadadores
    k["pct_exterior"] = k.compitieron_exterior / k.nadadores
    k["pct_con_podio_internacional"] = (k.con_podio_internacional
                                        / k.compitieron_internacional.replace(0, np.nan))
    k["muestra_suficiente"] = k.nadadores >= MIN_NADADORES_KPI
    return k


def main():
    d = pd.concat([pd.read_csv(DATOS / f"nadosFull_v2_{s}.csv", low_memory=False)
                   for s in ("femenino", "masculino")], ignore_index=True)
    sin_id = d.person_id.isna()
    if sin_id.any():         # 1 nado en 2024: no se puede cruzar con el resto del nadador
        print(f"Se descartan {sin_id.sum()} nados sin person_id")
        d = d[~sin_id]
    print(f"Base v2: {len(d):,} nados, {d.person_id.nunique():,} nadadores")

    d = d.merge(imputar_federacion(d), left_on="person_id", right_index=True, how="left")

    paises = pd.read_csv(DATOS / "paises.csv")
    continente = dict(zip(paises.pais_codigo, paises.continente))
    d["continente"] = d.federacion.map(continente)
    d["sede_continente"] = d.sede_pais_codigo.map(continente)

    torneos = clasificar_torneos(d)
    torneos.to_csv(DATOS / "torneos.csv", index=False, encoding="utf-8")
    d = d.merge(torneos[["competencia", "alcance", "categoria", "internacional"]]
                .rename(columns={"alcance": "torneo_alcance", "categoria": "torneo_categoria",
                                 "internacional": "torneo_internacional"}),
                on="competencia", how="left")

    sedes = pd.read_csv(DATOS / "sedes.csv")
    base = ciudad_base(d, sedes, pd.read_csv(DATOS / "paises_coord.csv"))
    d = (d.merge(sedes, on=["ciudad", "sede_pais_codigo"], how="left")
          .rename(columns={"lat": "sede_lat", "lon": "sede_lon"})
          .merge(base, on="federacion", how="left"))
    d["exterior"] = d.sede_pais_codigo != d.federacion
    d["km_desde_base"] = haversine_km(d.lat_base, d.lon_base, d.sede_lat, d.sede_lon).round(0)
    # Aproximación por longitud (15° = 1 hora). No considera husos políticos ni horario de verano.
    dlon = (d.sede_lon - d.lon_base + 180) % 360 - 180
    d["husos_aprox"] = (dlon.abs() / 15).round(0)

    d = d.merge(tabla_minimas(), on=["sexo", "estilo", "distancia", "piscina"], how="left")
    d["cumple_A"] = d.tiempo_s <= d.minima_A_s
    d["cumple_B"] = d.tiempo_s <= d.minima_B_s

    fecha = pd.to_datetime(d.fecha)
    d["mes"] = fecha.dt.to_period("M").astype(str)
    d["semestre"] = fecha.dt.year.astype(str) + "-S" + np.where(fecha.dt.month <= 6, "1", "2")

    # Anonimización: fuera nombre, fecha de nacimiento, club y los identificadores de
    # la fuente. El id es un correlativo sin relación con el person_id de World Aquatics.
    ids = {p: i for i, p in enumerate(d.person_id.drop_duplicates().sample(frac=1, random_state=7), 1)}
    d["id_nadador"] = d.person_id.map(ids)
    columnas = ["id_nadador", "sexo", "edad", "federacion", "nivel_imputacion", "continente",
                "estilo", "distancia", "piscina", "tiempo_s", "puntos_fina", "rank",
                "fecha", "mes", "semestre", "competencia", "ciudad", "sede_pais_codigo",
                "sede_continente", "sede_lat", "sede_lon", "torneo_alcance", "torneo_categoria",
                "torneo_internacional", "medalla", "exterior", "ciudad_base", "origen",
                "lat_base", "lon_base",
                "km_desde_base", "husos_aprox", "minima_A_s", "minima_B_s", "cumple_A", "cumple_B"]
    b = d[columnas]
    b.to_csv(DATOS / "base_dashboard.csv", index=False, encoding="utf-8")
    print(f"base_dashboard.csv: {len(b):,} filas, {b.id_nadador.nunique():,} nadadores, "
          f"{b.federacion.nunique()} federaciones")

    # Sesgo de visibilidad: si los torneos nacionales de una federación no llegan
    # al ranking, solo se ven sus nadadores de élite cuando compiten afuera, y sus
    # porcentajes salen inflados (México, Israel o Colombia: 100% en el exterior).
    # Los KPI de estas federaciones no son comparables con los del resto. La
    # cobertura es de la federación: vale igual para mujeres y hombres.
    locales = (b[~b.exterior].groupby(["federacion", "semestre"]).competencia.nunique()
               .rename("torneos_locales_en_ranking"))

    def con_cobertura(k):
        k = k.merge(locales, on=["federacion", "semestre"], how="left").fillna(
            {"torneos_locales_en_ranking": 0})
        k["cobertura"] = np.where(k.torneos_locales_en_ranking > 0,
                                  "con torneos locales", "solo vista en el exterior")
        return k

    con_cobertura(kpis(b, ["federacion", "continente"])).to_csv(
        DATOS / "kpi_federacion_semestre.csv", index=False, encoding="utf-8")
    kc = kpis(b, ["continente"])
    kc.to_csv(DATOS / "kpi_continente_semestre.csv", index=False, encoding="utf-8")
    # Las mismas tablas por sexo, para el filtro del dashboard.
    con_cobertura(kpis(b, ["federacion", "continente", "sexo"])).to_csv(
        DATOS / "kpi_federacion_sexo_semestre.csv", index=False, encoding="utf-8")
    kpis(b, ["continente", "sexo"]).to_csv(
        DATOS / "kpi_continente_sexo_semestre.csv", index=False, encoding="utf-8")
    print("\nKPI por continente:")
    print(kc.round(3).to_string(index=False))


if __name__ == "__main__":
    main()
