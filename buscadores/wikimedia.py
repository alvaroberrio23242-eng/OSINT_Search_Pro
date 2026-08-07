import re
import requests

API_URL = "https://commons.wikimedia.org/w/api.php"

# Wikimedia pide identificar la app que consume la API (política de uso).
HEADERS = {
    "User-Agent": "OSINTSearchPro/1.0 (uso educativo; contacto: no-reply@example.com)"
}

# Licencias que consideramos seguras para reutilizar en un proyecto público.
# Cualquier otra cosa (o ausencia de licencia) se descarta.
LICENCIAS_PERMITIDAS = {
    "cc0", "public domain", "pd", "pd-old", "pd-us",
    "cc by", "cc by 2.0", "cc by 3.0", "cc by 4.0",
    "cc by-sa", "cc by-sa 2.0", "cc by-sa 3.0", "cc by-sa 4.0",
}


def _quitar_html(texto: str) -> str:
    """Wikimedia suele devolver el autor/crédito con markup HTML embebido."""
    if not texto:
        return ""
    return re.sub(r"<[^>]+>", "", texto).strip()


def _licencia_es_segura(licencia_corta: str) -> bool:
    return licencia_corta.strip().lower() in LICENCIAS_PERMITIDAS


def buscar_imagenes(consulta: str, limite: int = 8):
    """
    Busca imágenes en Wikimedia Commons para 'consulta' y devuelve
    metadata de licencia/autor junto a cada resultado, para que la
    decisión de qué descargar sea siempre informada.
    """
    params = {
        "action": "query",
        "format": "json",
        "generator": "search",
        "gsrsearch": consulta,
        "gsrnamespace": 6,  # namespace "File:"
        "gsrlimit": limite,
        "prop": "imageinfo",
        "iiprop": "url|size|mime|extmetadata",
    }

    respuesta = requests.get(API_URL, params=params, headers=HEADERS, timeout=15)
    respuesta.raise_for_status()
    data = respuesta.json()

    paginas = data.get("query", {}).get("pages", {})
    resultados = []

    for pagina in paginas.values():
        infos = pagina.get("imageinfo")
        if not infos:
            continue
        info = infos[0]
        meta = info.get("extmetadata", {})

        licencia_corta = meta.get("LicenseShortName", {}).get("value", "Desconocida")
        autor = _quitar_html(meta.get("Artist", {}).get("value", "")) or "Desconocido"
        titulo = pagina.get("title", "")

        resultados.append({
            "titulo": titulo,
            "url_imagen": info.get("url", ""),
            "url_pagina": "https://commons.wikimedia.org/wiki/" + titulo.replace(" ", "_"),
            "mime": info.get("mime", ""),
            "ancho": info.get("width"),
            "alto": info.get("height"),
            "licencia": licencia_corta,
            "autor": autor,
            "licencia_segura": _licencia_es_segura(licencia_corta),
        })

    # Prioriza las de licencia verificablemente segura primero.
    resultados.sort(key=lambda r: not r["licencia_segura"])
    return resultados
