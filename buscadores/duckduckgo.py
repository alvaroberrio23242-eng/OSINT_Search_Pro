from ddgs import DDGS


def buscar(consulta, limite=10):
    resultados = []

    with DDGS() as ddgs:
        respuesta = ddgs.text(consulta, max_results=limite)

        for r in respuesta:
            resultados.append({
                "titulo": r.get("title", ""),
                "descripcion": r.get("body", ""),
                "url": r.get("href", "")
            })

    return resultados