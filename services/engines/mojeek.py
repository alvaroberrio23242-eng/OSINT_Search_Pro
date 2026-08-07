from bs4 import BeautifulSoup
from config import Config
from services.http_utils import safe_get

NOMBRE = "Mojeek"
ICONO = "mojeek"


def buscar(consulta, limite=None):
    limite = limite or Config.MAX_RESULTS_PER_ENGINE
    resultados = []
    try:
        r = safe_get("https://www.mojeek.com/search", params={"q": consulta})
        soup = BeautifulSoup(r.text, "html.parser")
        items = soup.select("ul.results-standard > li")[:limite]
        for it in items:
            a = it.find("a", class_="ob") or it.find("h2").find("a") if it.find("h2") else None
            desc = it.find("p", class_="s")
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
