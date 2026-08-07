from config import Config

NOMBRE = "Google"
ICONO = "google"


def buscar(consulta, limite=None):
    limite = limite or Config.MAX_RESULTS_PER_ENGINE
    resultados = []
    try:
        from googlesearch import search as gsearch

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
        return {"motor": NOMBRE, "ok": False, "error": str(e), "resultados": []}
