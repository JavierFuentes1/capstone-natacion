"""
Sonda: cuanto hay que bajar para tener suficientes NADADORES distintos?

Bajar los N tiempos mas rapidos de una prueba no es lo mismo que bajar N
nadadores: los mejores compiten muchas veces al anio. Este script mide,
para dos pruebas, cuantos nadadores distintos vas juntando a medida que
bajas mas profundo en el ranking.

Tambien compara el modo ALL_TIMES (todos los nados) con BEST_TIMES
(el mejor de cada nadador), que seria el atajo si funciona.

Uso:   python probar_profundidad.py
"""

import importlib.util
import os

AQUI = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("d", os.path.join(AQUI, "descargar.py"))
d = importlib.util.module_from_spec(spec)
spec.loader.exec_module(d)

CASOS = [
    ("M", 100, "FREESTYLE",    "LCM", "100 libre masculino, piscina 50 m"),
    ("F", 200, "BREASTSTROKE", "SCM", "200 pecho femenino, piscina 25 m"),
]
CORTES = [600, 1200, 2400, 4000]
TOPE = max(CORTES)


def main():
    os.makedirs(d.DIR_CACHE, exist_ok=True)

    for sexo, dist, estilo, piscina, etiqueta in CASOS:
        print("\n" + "=" * 64)
        print(etiqueta, "- 2024")
        print("=" * 64)

        # --- modo BEST_TIMES: un nado por nadador ---
        best = d.pedir({
            "gender": sexo, "distance": dist, "stroke": estilo,
            "poolConfiguration": piscina, "year": 2024,
            "timesMode": "BEST_TIMES", "pageSize": 1000, "page": 0,
        })
        if best:
            filas_b = best.get("swimmingWorldRankings") or []
            ids_b = {f.get("personId") for f in filas_b if f.get("personId")}
            print("\n  BEST_TIMES : {} filas, {} nadadores distintos, totalRowCount={}".format(
                len(filas_b), len(ids_b), best.get("totalRowCount")))
        else:
            print("\n  BEST_TIMES : fallo la consulta")

        # --- modo ALL_TIMES: bajar por paginas y contar nadadores ---
        print("\n  ALL_TIMES - nadadores distintos segun cuanto bajes:\n")
        print("    {:>8}  {:>10}  {:>12}".format("nados", "nadadores", "nados/nadador"))
        print("    " + "-" * 36)

        vistos = set()
        nados = 0
        pagina = 0
        total_api = None
        while nados < TOPE:
            r = d.pedir({
                "gender": sexo, "distance": dist, "stroke": estilo,
                "poolConfiguration": piscina, "year": 2024,
                "timesMode": "ALL_TIMES", "pageSize": d.TAM_PAGINA, "page": pagina,
            })
            if r is None:
                break
            if total_api is None:
                total_api = r.get("totalRowCount")
            lote = r.get("swimmingWorldRankings") or []
            if not lote:
                break
            for f in lote:
                if f.get("personId"):
                    vistos.add(f["personId"])
            nados += len(lote)
            for corte in CORTES:
                if nados - len(lote) < corte <= nados:
                    print("    {:>8,}  {:>10,}  {:>12.1f}".format(
                        nados, len(vistos), nados / max(len(vistos), 1)))
            if len(lote) < d.TAM_PAGINA:
                print("    {:>8,}  {:>10,}  {:>12.1f}   <- se acabo".format(
                    nados, len(vistos), nados / max(len(vistos), 1)))
                break
            pagina += 1

        print("\n  Nados que existen en total: {:,}".format(total_api or 0))

    print("\n" + "=" * 64)
    print("Mandale esta tabla a Claude para decidir cuanto bajar.")
    print("=" * 64)


if __name__ == "__main__":
    main()
