"""
Sonda 2: como se pide mas de 1000 filas?

Descubrimos que el parametro `page` lo ignora la API: todas las paginas
devuelven lo mismo. Esta sonda prueba dos caminos:

  A) subir pageSize y ver hasta donde llega
  B) probar otros nombres para el parametro de pagina

No usa cache, para que ninguna respuesta vieja contamine la prueba.

Uso:   python probar_paginacion.py
"""

import json
import os
import time
import urllib.parse
import urllib.request

BASE = "https://api.worldaquatics.com/fina/rankings/swimming"

FIJOS = {
    "gender": "M", "distance": 100, "stroke": "FREESTYLE",
    "poolConfiguration": "LCM", "year": 2024, "timesMode": "BEST_TIMES",
}


def pedir(extra):
    params = dict(FIJOS)
    params.update(extra)
    url = BASE + "?" + urllib.parse.urlencode(params)
    try:
        req = urllib.request.Request(
            url, headers={"User-Agent": "Mozilla/5.0", "Accept": "application/json"})
        with urllib.request.urlopen(req, timeout=90) as r:
            datos = json.load(r)
        time.sleep(0.5)
        return datos
    except Exception as e:                       # noqa: BLE001
        return {"__error__": "{}: {}".format(type(e).__name__, e)}


def resumen(datos):
    """Devuelve (n_filas, primer_rank, ultimo_rank, primer_nombre, total)."""
    if "__error__" in datos:
        return None
    filas = datos.get("swimmingWorldRankings") or []
    if not filas:
        return (0, None, None, None, datos.get("totalRowCount"))
    return (len(filas), filas[0].get("rank"), filas[-1].get("rank"),
            filas[0].get("fullName"), datos.get("totalRowCount"))


print("=" * 70)
print("A) HASTA DONDE LLEGA pageSize")
print("=" * 70)
print("{:>9}  {:>8}  {:>12}  {:>12}".format("pageSize", "filas", "rank 1o", "rank ultimo"))
print("-" * 70)
mejor_tam = 1000
for tam in [1000, 2000, 5000, 10000, 25000]:
    d = pedir({"pageSize": tam})
    if "__error__" in d:
        print("{:>9}  {}".format(tam, d["__error__"][:52]))
        continue
    r = resumen(d)
    print("{:>9}  {:>8}  {:>12}  {:>12}".format(tam, r[0], r[1], r[2]))
    if r[0] > mejor_tam:
        mejor_tam = r[0]

print("\n  totalRowCount de esta prueba:", resumen(pedir({"pageSize": 10}))[4])
print("  filas maximas conseguidas en UNA llamada:", mejor_tam)

print("\n" + "=" * 70)
print("B) QUE PARAMETRO MUEVE LA PAGINA")
print("=" * 70)
print("Si funciona, el 'rank 1o' tiene que ser 101, no 1.\n")
print("{:<14}  {:>7}  {:>9}  {}".format("parametro", "filas", "rank 1o", "primer nombre"))
print("-" * 70)

base = resumen(pedir({"pageSize": 100}))
print("{:<14}  {:>7}  {:>9}  {}   <- referencia".format(
    "(ninguno)", base[0], base[1], base[3]))

for nombre in ["page", "pageNumber", "pageIndex", "offset", "start",
               "skip", "from", "firstResult"]:
    d = pedir({"pageSize": 100, nombre: 1 if nombre in
               ("page", "pageNumber", "pageIndex") else 100})
    if "__error__" in d:
        print("{:<14}  {}".format(nombre, d["__error__"][:48]))
        continue
    r = resumen(d)
    marca = "  <-- FUNCIONA" if r and r[1] not in (None, base[1]) else ""
    print("{:<14}  {:>7}  {:>9}  {}{}".format(
        nombre, r[0], r[1], (r[3] or "")[:24], marca))

print("\n" + "=" * 70)
print("Mandale esta salida a Claude.")
print("=" * 70)
