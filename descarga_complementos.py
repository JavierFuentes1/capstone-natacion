"""
Datos complementarios para el dashboard por federación (Módulo 2).

1. Países de World Aquatics con su continente  ->  datos/paises.csv
   Fuente: api.worldaquatics.com/fina/countries (código IOC, nombre, región).

2. Coordenadas de cada sede (ciudad + país) y del centro de cada país
   ->  datos/sedes.csv  y  datos/paises_coord.csv
   Fuente: Nominatim (OpenStreetMap), con una pausa de 1,1 s entre consultas
   como exige su política de uso, y caché en datos/cache_geo/ para no repetirlas.
   Los datos de OpenStreetMap están bajo licencia ODbL: se citan como
   "© colaboradores de OpenStreetMap" donde se usen.

Requiere datos/nadosFull_v2_femenino.csv y datos/nadosFull_v2_masculino.csv
(salida de descarga_temporadas.py). Uso:

    python descarga_complementos.py
"""

import hashlib
import json
import time
import urllib.parse
import urllib.request
from pathlib import Path

import pandas as pd

AQUI = Path(__file__).parent
DATOS = AQUI / "datos"
CACHE_GEO = DATOS / "cache_geo"

UA = {"User-Agent": "capstone-natacion-usm/1.0 (proyecto academico)",
      "Accept": "application/json"}
PAUSA_NOMINATIM = 1.1

# Nombres de World Aquatics que Nominatim no reconoce como país.
ALIAS_PAIS = {
    "GBR": "United Kingdom", "TPE": "Taiwan", "HKG": "Hong Kong", "MAC": "Macao",
    "PUR": "Puerto Rico", "ARU": "Aruba", "CUR": "Curaçao", "ISV": "United States Virgin Islands",
    "GUM": "Guam", "ASA": "American Samoa", "SKN": "Saint Kitts and Nevis", "PLE": "Palestine",
    "GEQ": "Equatorial Guinea", "CGO": "Republic of the Congo", "TLS": "Timor-Leste",
    "NMA": "Northern Mariana Islands", "TAH": "French Polynesia", "VNM": "Vietnam",
}
# Sedes con un nombre que Nominatim no encuentra tal cual.
ALIAS_CIUDAD = {"Fukushima-pref": "Fukushima", "Reykjanesbar": "Reykjanesbær"}


def pedir_json(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60) as r:
        return json.load(r)


def paises():
    datos = pedir_json("https://api.worldaquatics.com/fina/countries")
    df = pd.DataFrame([{
        "pais_codigo": p["Code"],
        "pais_nombre": p["Name"],
        "continente": p["RegionName"] or None,
    } for p in datos])
    df.to_csv(DATOS / "paises.csv", index=False, encoding="utf-8")
    print(f"paises.csv: {len(df)} países, {df.continente.isna().sum()} sin continente "
          "(neutrales, refugiados, territorios)")
    return df


def geocodificar(params):
    """Una consulta a Nominatim, cacheada. Devuelve (lat, lon) o (None, None)."""
    url = "https://nominatim.openstreetmap.org/search?" + urllib.parse.urlencode(
        {**params, "format": "json", "limit": 1})
    ruta = CACHE_GEO / (hashlib.sha256(url.encode()).hexdigest() + ".json")
    if ruta.exists():
        res = json.loads(ruta.read_text(encoding="utf-8"))
    else:
        try:
            res = pedir_json(url)
        except Exception as e:                              # noqa: BLE001
            print("  ! fallo", params, type(e).__name__)
            return None, None
        ruta.write_text(json.dumps(res), encoding="utf-8")
        time.sleep(PAUSA_NOMINATIM)
    if not res:
        return None, None
    return float(res[0]["lat"]), float(res[0]["lon"])


def main():
    CACHE_GEO.mkdir(parents=True, exist_ok=True)
    tabla_paises = paises()
    nombre = dict(zip(tabla_paises.pais_codigo, tabla_paises.pais_nombre))
    nombre.update(ALIAS_PAIS)

    nados = pd.concat([pd.read_csv(DATOS / f"nadosFull_v2_{s}.csv",
                                   usecols=["ciudad", "sede_pais_codigo"])
                       for s in ("femenino", "masculino")])
    sedes = nados.drop_duplicates().dropna().sort_values(["sede_pais_codigo", "ciudad"])

    filas = []
    for ciudad, cod in sedes.itertuples(index=False):
        pais = nombre.get(cod, cod)
        busca = ALIAS_CIUDAD.get(ciudad, ciudad)
        lat, lon = geocodificar({"city": busca, "country": pais})
        if lat is None:                       # nombres raros: probar texto libre
            lat, lon = geocodificar({"q": f"{busca}, {pais}"})
        filas.append({"ciudad": ciudad, "sede_pais_codigo": cod, "lat": lat, "lon": lon})
    df = pd.DataFrame(filas)
    df.to_csv(DATOS / "sedes.csv", index=False, encoding="utf-8")
    print(f"sedes.csv: {len(df)} sedes, {df.lat.isna().sum()} sin coordenadas")

    # Centro de cada país: origen de respaldo para las federaciones sin sede propia.
    filas = []
    for cod, pais in nombre.items():
        lat, lon = geocodificar({"country": pais})
        if lat is None and cod in ALIAS_PAIS:    # territorios: no son "country" en OSM
            lat, lon = geocodificar({"q": pais})
        filas.append({"pais_codigo": cod, "lat": lat, "lon": lon})
    df = pd.DataFrame(filas)
    df.to_csv(DATOS / "paises_coord.csv", index=False, encoding="utf-8")
    print(f"paises_coord.csv: {len(df)} países, {df.lat.isna().sum()} sin coordenadas")


if __name__ == "__main__":
    main()
