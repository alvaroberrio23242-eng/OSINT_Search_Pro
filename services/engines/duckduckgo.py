import time

from config import Config

NOMBRE = "DuckDuckGo"
ICONO = "duckduckgo"

# Si el backend "duckduckgo" está bloqueado (frecuente en IPs de hosting como
# Railway/Render), ddgs permite pedirle los mismos resultados a otros
# proveedores sin cambiar la librería.
_BACKENDS = ["duckduckgo", "bing", "brave"]


def buscar(consulta, limite=None):
    limite = limite or Config.MAX_RESULTS_PER_ENGINE
    try:
        from ddgs import DDGS
    except ImportError as e:
        return {"motor": NOMBRE, "ok": False, "error": f"Librería no instalada: {e}", "resultados": []}

    ultimo_error = None
    for backend in _BACKENDS:
        try:
            with DDGS() as ddgs:
                respuesta = list(ddgs.text(consulta, max_results=limite, backend=backend))
            resultados = [
                {
                    "titulo": r.get("title", ""),
                    "descripcion": r.get("body", ""),
                    "url": r.get("href", ""),
                    "motor": NOMBRE,
                }
                for r in respuesta
            ]
            if resultados:
                return {"motor": NOMBRE, "ok": True, "error": None, "resultados": resultados}
        except Exception as e:
            ultimo_error = e
            time.sleep(0.4)
            continue

    if ultimo_error:
        return {"motor": NOMBRE, "ok": False, "error": str(ultimo_error), "resultados": []}
    return {"motor": NOMBRE, "ok": True, "error": None, "resultados": []}
