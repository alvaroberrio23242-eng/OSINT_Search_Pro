"""
Empaqueta la guía, la trivia y las imágenes descargadas en un único
archivo ZIP, incluyendo un archivo de créditos con la atribución legal
de cada imagen.
"""
import os
import zipfile


def render_creditos(imagenes):
    lineas = [
        "CRÉDITOS DE IMÁGENES",
        "=====================",
        "",
        "Todas las imágenes provienen de Wikimedia Commons y se distribuyen",
        "bajo licencias libres (CC0, CC-BY o dominio público).",
        "",
    ]
    for img in imagenes:
        lineas.append(f"- {img.get('archivo_local', img['titulo'])}")
        lineas.append(f"  Título: {img['titulo']}")
        lineas.append(f"  Autor: {img['autor']}")
        lineas.append(f"  Licencia: {img['licencia']}")
        lineas.append(f"  Fuente: {img.get('fuente', '')}")
        lineas.append("")
    return "\n".join(lineas)


def crear_paquete(guia_md, trivia_md, imagenes, carpeta_imagenes, zip_destino):
    creditos_txt = render_creditos(imagenes)

    with zipfile.ZipFile(zip_destino, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("guia_docente.md", guia_md)
        z.writestr("trivia.md", trivia_md)
        z.writestr("creditos_imagenes.txt", creditos_txt)

        for img in imagenes:
            nombre_local = img.get("archivo_local")
            if not nombre_local:
                continue
            ruta_local = os.path.join(carpeta_imagenes, nombre_local)
            if os.path.exists(ruta_local):
                z.write(ruta_local, arcname=f"imagenes/{nombre_local}")

    return zip_destino
