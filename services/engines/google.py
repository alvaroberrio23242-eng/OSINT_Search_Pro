import time

import requests

from config import Config

NOMBRE = "Google"
ICONO = "google"

_API_URL = "https://www.googleapis.com/customsearch/v1"


def _buscar_api(consulta, limite):
    """Usa la Google Custom Search JSON API (requiere Config.GOOGLE_API_KEY y
    Config.GOOGLE_CSE_ID). Gratis hasta 100 consultas/día. No es scraping:
    no la bloquea Google aunque el servidor esté en un datacenter."""
    resultados = []
    # La API solo devuelve hasta 10 resultados por página (parámetro start
    # para paginar); pedimos las páginas necesarias hasta llegar al límite.
    restante = limite
    inicio = 1
    while restante > 0 and inicio <= 91:  # la API no pagina más allá de 100
        r = requests.get(
            _API_URL,
            params={
                "key": Config.GOOGLE_API_KEY,
                "cx": Config.GOOGLE_CSE_ID,
                "q": consulta,
                "num": min(restante, 10),
                "start": inicio,
            },
            timeout=Config.HTTP_TIMEOUT,
        )
        r.raise_for_status()
        data = r.json()
        items = data.get("items") or []
        for it in items:
            resultados.append(
                {
                    "titulo": it.get("title", ""),
                    "descripcion": it.get("snippet", ""),
                    "url": it.get("link", ""),
                    "motor": NOMBRE,
                }
            )
        if not items:
            break
        inicio += len(items)
        restante = limite - len(resultados)

    return {"motor": NOMBRE, "ok": True, "error": None, "resultados": resultados[:limite]}


def _buscar_scraping(consulta, limite):
    """Fallback con la librería googlesearch-python (scraping). Es lo que
    había antes: Google suele bloquear (429) las IPs de hosting en la nube."""
    try:
        from googlesearch import search as gsearch
    except ImportError as e:
        return {"motor": NOMBRE, "ok": False, "error": f"Librería no instalada: {e}", "resultados": []}

    ultimo_error = None
    for intento in range(2):
        try:
            resultados = []
            for item in gsearch(consulta, num_results=limite, advanced=True):
                resultados.append(
                    {
                        "titulo": getattr(item, "title", "") or item.url,
                        "descripcion": getattr(item, "description", "") or "",
                        "url": item.url,
                        "motor": NOMBRE,
                    }
                )
            return {"motor": NOMBRE, "ok": True, "error": None, "resultados": resultados}
        except Exception as e:
            ultimo_error = e
            msg = str(e)
            if "429" in msg or "Too Many Requests" in msg:
                time.sleep(1.2)
                continue
            break

    error_final = str(ultimo_error) if ultimo_error else "Error desconocido"
    if "429" in error_final:
        error_final = (
            "Google bloqueó temporalmente las búsquedas desde este servidor (429). "
            "Es un límite anti-bot de Google, no un error del código."
        )
    return {"motor": NOMBRE, "ok": False, "error": error_final, "resultados": []}


def buscar(consulta, limite=None):
    limite = limite or Config.MAX_RESULTS_PER_ENGINE

    if Config.GOOGLE_API_KEY and Config.GOOGLE_CSE_ID:
        try:
            return _buscar_api(consulta, limite)
        except Exception as e:
            resultado_scraping = _buscar_scraping(consulta, limite)
            if not resultado_scraping.get("resultados"):
                resultado_scraping["error"] = f"API falló ({e}) y el scraping tampoco trajo nada."
            return resultado_scraping

    return _buscar_scraping(consulta, limite)
