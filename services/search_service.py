import time
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

from config import Config
from services.demo_data import generar_resultados_demo
from services.engines import duckduckgo, google, bing, brave, yandex, startpage, mojeek

MOTORES = {
    "duckduckgo": duckduckgo,
    "google": google,
    "bing": bing,
    "brave": brave,
    "yandex": yandex,
    "startpage": startpage,
    "mojeek": mojeek,
}

_cache = {}
_cache_lock = threading.Lock()


def _cache_key(consulta, motores, limite):
    return (consulta.strip().lower(), tuple(sorted(motores)), limite)


def _get_cache(key):
    with _cache_lock:
        entry = _cache.get(key)
        if not entry:
            return None
        resultado, expira = entry
        if time.time() > expira:
            del _cache[key]
            return None
        return resultado


def _set_cache(key, resultado):
    with _cache_lock:
        _cache[key] = (resultado, time.time() + Config.SEARCH_CACHE_TTL)


def motores_disponibles():
    return [
        {"id": key, "nombre": mod.NOMBRE, "icono": mod.ICONO} for key, mod in MOTORES.items()
    ]


def _con_fallback_demo(resultado, consulta, limite):
    """Si el motor falló (bloqueo/librería faltante) o no trajo nada real,
    rellena con resultados de muestra marcados con demo=True, para que el
    demo del portafolio nunca se vea vacío. El error original se conserva
    en 'error_original' por si la UI quiere mostrarlo igual."""
    if resultado.get("resultados"):
        return resultado

    demo = generar_resultados_demo(consulta, resultado.get("motor", "?"), limite)
    return {
        **resultado,
        "ok": True,
        "demo": True,
        "error_original": resultado.get("error"),
        "resultados": demo,
    }


def realizar_busqueda(consulta, motores=None, limite=None):
    """Ejecuta la consulta en los motores solicitados en paralelo.

    motores: lista de ids ('duckduckgo', 'google', ...). Si es None, usa todos.
    """
    if not motores:
        motores = list(MOTORES.keys())
    motores = [m for m in motores if m in MOTORES]

    key = _cache_key(consulta, motores, limite)
    cacheado = _get_cache(key)
    if cacheado is not None:
        return cacheado

    salida = []
    with ThreadPoolExecutor(max_workers=max(len(motores), 1)) as ex:
        futuros = {ex.submit(MOTORES[m].buscar, consulta, limite): m for m in motores}
        for fut in as_completed(futuros):
            try:
                salida.append(fut.result())
            except Exception as e:
                salida.append(
                    {"motor": futuros[fut], "ok": False, "error": str(e), "resultados": []}
                )

    salida = [_con_fallback_demo(r, consulta, limite) for r in salida]

    orden = {m: i for i, m in enumerate(motores)}
    nombre_a_id = {MOTORES[m].NOMBRE: m for m in motores}
    salida.sort(key=lambda r: orden.get(nombre_a_id.get(r["motor"], ""), 99))

    _set_cache(key, salida)
    return salida