"""
Capstone natacion - Paso 1: descarga de datos
=============================================
Baja tiempos de natacion desde la API publica de World Aquatics.

Pregunta del proyecto: el factor de conversion entre piscina de 25 m (SCM)
y de 50 m (LCM), se sostiene igual en todos los estilos y distancias?

Solo usa la biblioteca estandar de Python. No necesita instalar nada.

Uso:
    python descargar.py            # descarga la muestra completa
    python descargar.py --prueba   # smoke test: una sola consulta


NOTA SOBRE LA API (medido el 31-ago-2026)
-----------------------------------------
Esta API NO pagina. Probamos page, pageNumber, pageIndex, offset, start,
skip, from y firstResult: todos se ignoran y siempre devuelve desde el
puesto 1. Lo unico que controla el tamano es `pageSize`, que llega hasta
5.000 (con 10.000 responde 404).

Por eso usamos `timesMode=BEST_TIMES`, que devuelve UN nado por nadador
-su mejor marca del anio- en vez de todos sus nados. Asi los 5.000 que
pedimos son 5.000 nadadores distintos y no 30 nadadores repetidos.
"""

import csv
import json
import os
import sys
import time
import urllib.parse
import urllib.request

# ----------------------------------------------------------------------
# CONFIGURACION - esto es lo unico que conviene tocar
# ----------------------------------------------------------------------

ANIOS = [2024]

# (distancia_en_metros, estilo)
PRUEBAS = [
    (50,  "FREESTYLE"),
    (100, "FREESTYLE"),
    (200, "FREESTYLE"),
    (400, "FREESTYLE"),
    (100, "BACKSTROKE"),
    (200, "BACKSTROKE"),
    (100, "BREASTSTROKE"),
    (200, "BREASTSTROKE"),
    (100, "BUTTERFLY"),
    (200, "BUTTERFLY"),
    (200, "MEDLEY"),
    (400, "MEDLEY"),
]

SEXOS = ["M", "F"]
PISCINAS = ["LCM", "SCM"]      # LCM = 50 m, SCM = 25 m

# Cuantos NADADORES bajar por combinacion. Tope duro de la API: 5000.
MAX_NADADORES = 5000

PAUSA = 0.5                    # segundos entre peticiones

# ----------------------------------------------------------------------

BASE = "https://api.worldaquatics.com/fina/rankings/swimming"
AQUI = os.path.dirname(os.path.abspath(__file__))
DIR_DATOS = os.path.join(AQUI, "datos")
DIR_CACHE = os.path.join(DIR_DATOS, "cache")

COLUMNAS = [
    "anio", "sexo", "piscina", "distancia", "estilo",
    "prueba", "rank", "tiempo", "tiempo_s", "puntos_fina",
    "nombre", "person_id", "fecha_nacimiento", "edad",
    "pais", "pais_codigo", "club",
    "fecha", "competencia", "ciudad",
    "medalla", "record", "result_id", "event_id", "discipline_id",
]


def tiempo_a_segundos(t):
    """'1:53.50' -> 113.5   |   '46.40' -> 46.4   |   '' -> None"""
    if not t:
        return None
    t = str(t).strip()
    if not t or t in ("DNS", "DNF", "DSQ"):
        return None
    try:
        if ":" in t:
            partes = t.split(":")
            if len(partes) == 2:
                m, s = partes
                return round(int(m) * 60 + float(s), 2)
            if len(partes) == 3:
                h, m, s = partes
                return round(int(h) * 3600 + int(m) * 60 + float(s), 2)
            return None
        return round(float(t), 2)
    except ValueError:
        return None


def pedir(params, intentos=3):
    """Hace una peticion a la API. Guarda la respuesta en cache."""
    url = BASE + "?" + urllib.parse.urlencode(params)
    clave = urllib.parse.quote(urllib.parse.urlencode(params), safe="")
    ruta_cache = os.path.join(DIR_CACHE, clave[:180] + ".json")

    if os.path.exists(ruta_cache):
        with open(ruta_cache, encoding="utf-8") as f:
            return json.load(f)

    ultimo_error = None
    for intento in range(intentos):
        try:
            req = urllib.request.Request(
                url, headers={"User-Agent": "Mozilla/5.0", "Accept": "application/json"}
            )
            with urllib.request.urlopen(req, timeout=120) as r:
                datos = json.load(r)
            with open(ruta_cache, "w", encoding="utf-8") as f:
                json.dump(datos, f)
            time.sleep(PAUSA)
            return datos
        except Exception as e:                       # noqa: BLE001
            ultimo_error = e
            time.sleep(2.0 * (intento + 1))
    print("  ! fallo la peticion:", type(ultimo_error).__name__, ultimo_error)
    return None


def bajar_combinacion(anio, sexo, piscina, distancia, estilo, maximo):
    """Devuelve (nados, total_disponible) para una prueba, sexo, piscina y anio.

    Una sola llamada: la API no pagina. `maximo` no puede pasar de 5000.
    Con BEST_TIMES cada fila es un nadador distinto.
    """
    datos = pedir({
        "gender": sexo,
        "distance": distancia,
        "stroke": estilo,
        "poolConfiguration": piscina,
        "year": anio,
        "timesMode": "BEST_TIMES",
        "pageSize": min(maximo, 5000),
    })
    if datos is None:
        return [], 0
    filas = datos.get("swimmingWorldRankings") or []
    total = datos.get("totalRowCount")
    return filas, (total if total is not None else len(filas))


def normalizar(r, anio, sexo, piscina, distancia, estilo):
    tiempo = r.get("time")
    return {
        "anio": anio,
        "sexo": sexo,
        "piscina": piscina,
        "distancia": distancia,
        "estilo": estilo,
        "prueba": r.get("disciplineName"),
        "rank": r.get("rank"),
        "tiempo": tiempo,
        "tiempo_s": tiempo_a_segundos(tiempo),
        "puntos_fina": r.get("finaPoints"),
        "nombre": r.get("fullName"),
        "person_id": r.get("personId"),
        "fecha_nacimiento": r.get("dateOfBirth"),
        "edad": r.get("athleteResultAge"),
        "pais": r.get("participantCountryName"),
        "pais_codigo": r.get("participantCountryCode"),
        "club": r.get("clubName") or r.get("club"),
        "fecha": r.get("resultDate"),
        "competencia": r.get("eventName"),
        "ciudad": r.get("eventCity"),
        "medalla": r.get("medalTag"),
        "record": r.get("records"),
        "result_id": r.get("resultId"),
        "event_id": r.get("eventId"),
        "discipline_id": r.get("disciplineId"),
    }


def smoke_test():
    print("SMOKE TEST - una sola consulta\n")
    datos = pedir({
        "gender": "M", "distance": 100, "stroke": "FREESTYLE",
        "poolConfiguration": "LCM", "year": 2024,
        "timesMode": "BEST_TIMES", "pageSize": 5,
    })
    if datos is None:
        print("FALLO. No hubo respuesta de la API.")
        return 1

    filas = datos.get("swimmingWorldRankings") or []
    print("Nados en esta respuesta:", len(filas),
          "| nadadores en total:", datos.get("totalRowCount"), "\n")
    if not filas:
        print("La respuesta llego vacia. Avisame y lo revisamos.")
        return 1

    print("Los 5 mejores 100 m libre masculino de 2024, piscina de 50 m:\n")
    for r in filas:
        print("  {:>2}. {:<28} {:<30} {:>8}  ({} s)".format(
            r.get("rank"), (r.get("fullName") or "")[:28],
            (r.get("participantCountryName") or "")[:30],
            r.get("time"), tiempo_a_segundos(r.get("time"))))

    ids = {r.get("personId") for r in filas}
    print("\n  {} filas -> {} nadadores distintos".format(len(filas), len(ids)))
    print("  (con BEST_TIMES tienen que ser iguales: un nado por nadador)")
    print("\nOK, la API responde. Ahora corre:  python descargar.py")
    return 0


def main():
    os.makedirs(DIR_CACHE, exist_ok=True)

    if "--prueba" in sys.argv:
        return smoke_test()

    combinaciones = [
        (a, s, p, d, e)
        for a in ANIOS for s in SEXOS for p in PISCINAS for (d, e) in PRUEBAS
    ]
    print("Voy a bajar {} combinaciones de prueba x sexo x piscina x anio.".format(
        len(combinaciones)))
    print("Hasta {} nadadores por combinacion, una llamada cada una.\n".format(
        MAX_NADADORES))

    todas = []
    total_universo = 0
    alertas = []
    print("{:<6} {:<40} {:>8}  {:>9}  {:>9}".format(
        "", "combinacion", "bajados", "distintos", "existen"))
    print("-" * 78)
    for i, (anio, sexo, piscina, distancia, estilo) in enumerate(combinaciones, 1):
        etiqueta = "{} {} {}m {} {}".format(anio, sexo, distancia, estilo, piscina)
        print("[{:>2}/{}] {:<40}".format(i, len(combinaciones), etiqueta),
              end=" ", flush=True)
        crudas, disponibles = bajar_combinacion(
            anio, sexo, piscina, distancia, estilo, MAX_NADADORES)
        filas = [normalizar(r, anio, sexo, piscina, distancia, estilo) for r in crudas]
        distintos = len({f["person_id"] for f in filas if f["person_id"]})
        todas.extend(filas)
        total_universo += disponibles

        # CONTROL: con BEST_TIMES cada fila debe ser un nadador distinto.
        # Si no lo es, algo se esta duplicando y hay que parar a mirar.
        aviso = ""
        if filas and distintos < len(filas) :
            aviso = "  <-- OJO, hay repetidos"
            alertas.append(etiqueta)
        print("{:>8,}  {:>9,}  {:>9,}{}".format(
            len(filas), distintos, disponibles, aviso))

    salida = os.path.join(DIR_DATOS, "nados.csv")
    with open(salida, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=COLUMNAS)
        w.writeheader()
        w.writerows(todas)

    nadadores = len({r["person_id"] for r in todas if r["person_id"]})
    sin_tiempo = sum(1 for r in todas if r["tiempo_s"] is None)
    print("\n" + "=" * 78)
    print("Listo. Guardado en datos/nados.csv")
    print("")
    print("  Filas bajadas             : {:,}".format(len(todas)))
    print("  Nadadores en el mundo     : {:,}  (nos quedamos con el {:.1%})".format(
        total_universo, len(todas) / total_universo if total_universo else 0))
    print("  Nadadores distintos       : {:,}".format(nadadores))
    print("  Filas sin tiempo valido   : {}".format(sin_tiempo))
    print("")
    if alertas:
        print("  ATENCION: {} combinaciones traian nadadores repetidos.".format(
            len(alertas)))
        print("  Avisale a Claude antes de seguir.")
    else:
        print("  Control OK: ninguna combinacion trae nadadores repetidos.")
    print("")
    print("  Nos quedamos con los mas RAPIDOS de cada prueba, no con una")
    print("  muestra al azar. Eso hay que declararlo como limitacion:")
    print("  los resultados describen a la elite, no a todos los nadadores.")
    print("=" * 78)
    print("\nSiguiente paso: abre 01_exploracion.ipynb en VS Code.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
