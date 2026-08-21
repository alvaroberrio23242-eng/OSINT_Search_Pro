import requests
from bs4 import BeautifulSoup

from config import Config
from services.http_utils import safe_get

NOMBRE = "Brave Search"
ICONO = "brave"

_API_URL = "https://api.search.brave.com/res/v1/web/search"


def _buscar_api(consulta, limite):
    """Usa la API oficial de Brave Search (requiere Config.BRAVE_API_KEY).
    No es scraping: no la bloquean las IPs de hosting en la nube, y devuelve
    resultados reales."""
    headers = {
        "Accept": "application/json",
        "X-Subscription-Token": Config.BRAVE_API_KEY,
    }
    r = requests.get(
        _API_URL,
        params={"q": consulta, "count": min(limite, 20)},
        headers=headers,
        timeout=Config.HTTP_TIMEOUT,
    )
    r.raise_for_status()
    data = r.json()
    items = (data.get("web") or {}).get("results") or []
    resultados = [
        {
            "titulo": it.get("title", ""),
            "descripcion": it.get("description", ""),
            "url": it.get("url", ""),
            "motor": NOMBRE,
        }
        for it in items[:limite]
    ]
    return {"motor": NOMBRE, "ok": True, "error": None, "resultados": resultados}


def _buscar_scraping(consulta, limite):
    """Fallback por scraping HTML cuando no hay API key configurada. Es lo
    que había antes: funciona en local, pero motores como Brave/Google/Bing
    suelen bloquear las IPs de datacenter (Render, Railway...)."""
    resultados = []
    try:
        r = safe_get("https://search.brave.com/search", params={"q": consulta})
        soup = BeautifulSoup(r.text, "html.parser")
        items = soup.select("div.snippet")[:limite]
        for it in items:
            a = it.find("a", href=True)
            title_el = it.find(["span", "div"], class_="snippet-title") or (a if a else None)
            desc_el = it.find(class_="snippet-description")
            if a and a.get("href", "").startswith("http"):
                resultados.append(
                    {
                        "titulo": (title_el.get_text(strip=True) if title_el else a.get_text(strip=True)) or a["href"],
                        "descripcion": desc_el.get_text(strip=True) if desc_el else "",
                        "url": a["href"],
                        "motor": NOMBRE,
                    }
                )
        return {"motor": NOMBRE, "ok": True, "error": None, "resultados": resultados[:limite]}
    except Exception as e:
        return {"motor": NOMBRE, "ok": False, "error": str(e), "resultados": []}


def buscar(consulta, limite=None):
    limite = limite or Config.MAX_RESULTS_PER_ENGINE

    if Config.BRAVE_API_KEY:
        try:
            return _buscar_api(consulta, limite)
        except Exception as e:
            # Si la API falla (clave inválida, cuota agotada, etc.) caemos al
            # scraping en vez de dejar el motor completamente muerto.
            resultado_scraping = _buscar_scraping(consulta, limite)
            if not resultado_scraping.get("resultados"):
                resultado_scraping["error"] = f"API falló ({e}) y el scraping tampoco trajo nada."
            return resultado_scraping

    return _buscar_scraping(consulta, limite)
