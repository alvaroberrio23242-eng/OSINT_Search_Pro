from bs4 import BeautifulSoup
from config import Config
from services.http_utils import safe_get

NOMBRE = "Brave Search"
ICONO = "brave"


def buscar(consulta, limite=None):
    limite = limite or Config.MAX_RESULTS_PER_ENGINE
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
