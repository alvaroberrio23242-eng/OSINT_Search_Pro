from config import Config

NOMBRE = "DuckDuckGo"
ICONO = "duckduckgo"


def buscar(consulta, limite=None):
    limite = limite or Config.MAX_RESULTS_PER_ENGINE
    resultados = []
    try:
        from ddgs import DDGS

        with DDGS() as ddgs:
            respuesta = ddgs.text(consulta, max_results=limite)
            for r in respuesta:
                resultados.append(
                    {
                        "titulo": r.get("title", ""),
                        "descripcion": r.get("body", ""),
                        "url": r.get("href", ""),
                        "motor": NOMBRE,
                    }
                )
    except Exception as e:
        return {"motor": NOMBRE, "ok": False, "error": str(e), "resultados": []}

    return {"motor": NOMBRE, "ok": True, "error": None, "resultados": resultados}
