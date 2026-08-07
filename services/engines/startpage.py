from bs4 import BeautifulSoup
from config import Config
from services.http_utils import safe_get

NOMBRE = "Startpage"
ICONO = "startpage"


def buscar(consulta, limite=None):
    limite = limite or Config.MAX_RESULTS_PER_ENGINE
    resultados = []
    try:
        r = safe_get("https://www.startpage.com/sp/search", params={"query": consulta})
        soup = BeautifulSoup(r.text, "html.parser")
        items = soup.select("div.w-gl__result")[:limite]
        for it in items:
            a = it.find("a", class_="w-gl__result-title") or it.find("a", href=True)
            desc = it.find("p", class_="w-gl__description")
            if a and a.get("href", "").startswith("http"):
                resultados.append(
                    {
                        "titulo": a.get_text(strip=True) or a["href"],
                        "descripcion": desc.get_text(strip=True) if desc else "",
                        "url": a["href"],
                        "motor": NOMBRE,
                    }
                )
        return {"motor": NOMBRE, "ok": True, "error": None, "resultados": resultados}
    except Exception as e:
        return {"motor": NOMBRE, "ok": False, "error": str(e), "resultados": []}
