"""
Búsqueda y descarga de imágenes con licencia reutilizable desde la API
pública de Wikimedia Commons. Solo se aceptan licencias CC0, CC-BY y
dominio público.
"""
import os
import re
import requests

API_URL = "https://commons.wikimedia.org/w/api.php"
LICENCIAS_PERMITIDAS = ("cc0", "cc-by", "public domain", "pd")
TIMEOUT = 8


def _licencia_permitida(nombre_licencia):
    if not nombre_licencia:
        return False
    n = nombre_licencia.lower()
    return any(l in n for l in LICENCIAS_PERMITIDAS)


def buscar_imagenes(consulta, limite=6):
    """Busca en Wikimedia Commons y devuelve metadatos de imágenes con
    licencia libre. No descarga los archivos todavía."""
    params = {
        "action": "query",
        "format": "json",
        "generator": "search",
        "gsrsearch": f"{consulta} filetype:bitmap",
        "gsrnamespace": 6,  # namespace de archivos
        "gsrlimit": limite * 3,  # pedimos de más porque filtramos por licencia
        "prop": "imageinfo",
        "iiprop": "url|extmetadata|size",
        "iiurlwidth": 800,
    }
    headers = {"User-Agent": "EduPackBuilder/1.0 (proyecto educativo sin fines comerciales)"}

    try:
        resp = requests.get(API_URL, params=params, headers=headers, timeout=TIMEOUT)
        resp.raise_for_status()
        data = resp.json()
    except Exception:
        return []

    pages = data.get("query", {}).get("pages", {})
    resultados = []

    for _, pagina in pages.items():
        info_list = pagina.get("imageinfo")
        if not info_list:
            continue
        info = info_list[0]
        meta = info.get("extmetadata", {})

        licencia = meta.get("LicenseShortName", {}).get("value", "")
        if not _licencia_permitida(licencia):
            continue

        autor_html = meta.get("Artist", {}).get("value", "Autor no especificado")
        autor = re.sub("<[^<]+?>", "", autor_html).strip() or "Autor no especificado"

        url_imagen = info.get("thumburl") or info.get("url")
        if not url_imagen:
            continue

        titulo = pagina.get("title", "").replace("File:", "").replace("Archivo:", "")

        resultados.append({
            "titulo": titulo,
            "url": url_imagen,
            "url_original": info.get("url"),
            "licencia": licencia,
            "autor": autor,
            "fuente": info.get("descriptionurl", ""),
        })

        if len(resultados) >= limite:
            break

    return resultados


def descargar_imagenes(lista_imagenes, carpeta_destino):
    """Descarga a disco las imágenes ya filtradas por licencia.
    Devuelve la lista de imágenes con el campo 'archivo_local' agregado
    (solo para las que se lograron descargar)."""
    os.makedirs(carpeta_destino, exist_ok=True)
    headers = {"User-Agent": "EduPackBuilder/1.0 (proyecto educativo sin fines comerciales)"}

    descargadas = []
    for i, img in enumerate(lista_imagenes, start=1):
        try:
            resp = requests.get(img["url"], headers=headers, timeout=TIMEOUT, stream=True)
            resp.raise_for_status()
            ext = os.path.splitext(img["url"])[1].split("?")[0] or ".jpg"
            if len(ext) > 5:
                ext = ".jpg"
            nombre_archivo = f"imagen_{i:02d}{ext}"
            ruta = os.path.join(carpeta_destino, nombre_archivo)
            with open(ruta, "wb") as f:
                for chunk in resp.iter_content(8192):
                    f.write(chunk)
            img["archivo_local"] = nombre_archivo
            descargadas.append(img)
        except Exception:
            continue

    return descargadas
