import json
import mimetypes
import os
from urllib.parse import urlsplit, urlunsplit

import requests

from buscadores.wikimedia import buscar_imagenes
from services.utils import slugify

DIR_DESCARGAS = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static", "descargas")
CATEGORIAS_VALIDAS = {"bandas", "artistas", "grammys", "records"}
TAMANO_MAXIMO_BYTES = 15 * 1024 * 1024  # 15 MB, límite de sanidad
HEADERS = {
    "User-Agent": "OSINTSearchPro/1.0 (uso educativo; contacto: no-reply@example.com)",
    "Referer": "https://commons.wikimedia.org/",
}


def _url_sin_tracking(url: str) -> str:
    """
    La API de Wikimedia agrega parámetros utm_* a las URLs de imagen
    para analítica propia. Pedir la imagen con esos parámetros desde
    un script (no un navegador) suele devolver 403 Forbidden en el
    CDN de upload.wikimedia.org, así que los sacamos antes de descargar.
    """
    partes = urlsplit(url)
    return urlunsplit((partes.scheme, partes.netloc, partes.path, "", ""))


class DescargaError(Exception):
    pass


def buscar_imagenes_para(nombre: str, limite: int = 8):
    """Wrapper delgado sobre el buscador de Wikimedia, pensado para
    que los controllers no dependan directamente de 'buscadores/'."""
    return buscar_imagenes(nombre, limite=limite)


def _ruta_categoria(categoria: str) -> str:
    if categoria not in CATEGORIAS_VALIDAS:
        raise DescargaError(f"Categoría inválida: {categoria}")
    ruta = os.path.join(DIR_DESCARGAS, categoria)
    os.makedirs(ruta, exist_ok=True)
    return ruta


def descargar_imagen(categoria: str, nombre_item: str, resultado: dict, sufijo: int = 1) -> dict:
    """
    Descarga una imagen puntual (uno de los dicts que devuelve
    buscar_imagenes_para) a static/descargas/<categoria>/<slug>-<n>.<ext>
    y guarda un .json con la licencia/autor/fuente al lado, para
    trazabilidad legal antes de usarla en RockQuest.
    """
    if not resultado.get("licencia_segura"):
        raise DescargaError(
            "Esta imagen no tiene una licencia reutilizable verificada "
            f"(licencia detectada: {resultado.get('licencia', 'desconocida')}). "
            "No se descarga automáticamente."
        )

    url = _url_sin_tracking(resultado["url_imagen"])
    carpeta = _ruta_categoria(categoria)
    slug = slugify(nombre_item)

    respuesta = requests.get(url, headers=HEADERS, stream=True, timeout=20)
    respuesta.raise_for_status()

    content_type = respuesta.headers.get("Content-Type", "")
    if not content_type.startswith("image/"):
        raise DescargaError(f"La URL no devolvió una imagen (Content-Type: {content_type})")

    extension = mimetypes.guess_extension(content_type.split(";")[0].strip()) or ".jpg"
    if extension == ".jpe":
        extension = ".jpg"

    nombre_archivo = f"{slug}-{sufijo}{extension}"
    ruta_archivo = os.path.join(carpeta, nombre_archivo)

    total = 0
    with open(ruta_archivo, "wb") as f:
        for chunk in respuesta.iter_content(8192):
            total += len(chunk)
            if total > TAMANO_MAXIMO_BYTES:
                f.close()
                os.remove(ruta_archivo)
                raise DescargaError("La imagen supera el tamaño máximo permitido (15 MB).")
            f.write(chunk)

    metadata = {
        "item": nombre_item,
        "categoria": categoria,
        "archivo": nombre_archivo,
        "fuente": resultado["url_pagina"],
        "licencia": resultado["licencia"],
        "autor": resultado["autor"],
        "titulo_original": resultado["titulo"],
    }
    with open(ruta_archivo + ".json", "w", encoding="utf-8") as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)

    return {
        "ok": True,
        "archivo": nombre_archivo,
        "ruta_relativa": f"static/descargas/{categoria}/{nombre_archivo}",
        "metadata": metadata,
    }


def procesar_item_bulk(categoria: str, nombre_item: str, cantidad: int = 1):
    """
    Busca en Wikimedia y descarga hasta 'cantidad' imágenes con
    licencia segura para un item. Devuelve un reporte por item,
    nunca lanza excepción hacia afuera (se usa en el modo bulk).
    """
    reporte = {"item": nombre_item, "descargadas": [], "omitidas": [], "error": None}
    try:
        candidatas = buscar_imagenes_para(nombre_item, limite=cantidad * 3)
    except requests.RequestException as e:
        reporte["error"] = f"Fallo de red al buscar: {e}"
        return reporte

    if not candidatas:
        reporte["error"] = "Sin resultados en Wikimedia Commons."
        return reporte

    descargadas = 0
    for candidata in candidatas:
        if descargadas >= cantidad:
            break
        if not candidata["licencia_segura"]:
            reporte["omitidas"].append({
                "titulo": candidata["titulo"],
                "motivo": f"licencia no verificada ({candidata['licencia']})",
            })
            continue
        try:
            resultado = descargar_imagen(categoria, nombre_item, candidata, sufijo=descargadas + 1)
            reporte["descargadas"].append(resultado)
            descargadas += 1
        except DescargaError as e:
            reporte["omitidas"].append({"titulo": candidata["titulo"], "motivo": str(e)})
        except requests.RequestException as e:
            reporte["omitidas"].append({"titulo": candidata["titulo"], "motivo": f"error de red: {e}"})

    if descargadas == 0:
        reporte["error"] = "Ninguna candidata tenía licencia reutilizable verificada."

    return reporte
