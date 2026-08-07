from bs4 import BeautifulSoup
from config import Config
from services.http_utils import safe_get

NOMBRE = "Bing"
ICONO = "bing"


def buscar(consulta, limite=None):
    limite = limite or Config.MAX_RESULTS_PER_ENGINE
    resultados = []
    try:
        r = safe_get("https://www.bing.com/search", params={"q": consulta, "count": limite})
        soup = BeautifulSoup(r.text, "html.parser")
        items = soup.select("li.b_algo")[:limite]
        for it in items:
            h2 = it.find("h2")
            a = h2.find("a") if h2 else None
            desc = it.find("p") or it.find("div", class_="b_caption")
            if a and a.get("href"):
                resultados.append(
                    {
                        "titulo": a.get_text(strip=True),
                        "descripcion": desc.get_text(strip=True) if desc else "",
                        "url": a["href"],
                        "motor": NOMBRE,
                    }
                )
        return {"motor": NOMBRE, "ok": True, "error": None, "resultados": resultados}
    except Exception as e:
        return {"motor": NOMBRE, "ok": False, "error": str(e), "resultados": []}
