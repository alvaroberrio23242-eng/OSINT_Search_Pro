#!/usr/bin/env python3
"""
sync_a_rockquest.py

Copia las imágenes descargadas por OSINT Search Pro
(static/descargas/<categoria>/<slug>-<n>.<ext> + su .json de licencia)
hacia RockQuest (app/static/images/<categoria>/<slug>.<ext>),
quedándose con la primera descarga de cada item (la de licencia
más segura, porque imagen_service.py ya las descarga en ese orden).

Uso:
    python sync_a_rockquest.py --rockquest /ruta/a/rockquest-main

Por defecto asume que este script vive dentro de OSINT_Search_Pro-main/
y que RockQuest está en una carpeta hermana ../rockquest-main.
Con --forzar, sobrescribe imágenes que ya existan del lado de RockQuest.
"""

import argparse
import json
import re
import shutil
from pathlib import Path

CATEGORIAS = ["bandas", "artistas", "grammys", "records"]
PATRON_ARCHIVO = re.compile(r"^(?P<slug>.+)-(?P<n>\d+)\.(?P<ext>[a-zA-Z0-9]+)$")


def agrupar_por_slug(carpeta_origen: Path):
    """
    Agrupa los archivos de una carpeta de descargas por slug y
    devuelve, para cada slug, la ruta del archivo con el número
    más bajo (la primera descarga = licencia más prioritaria).
    """
    candidatos = {}
    if not carpeta_origen.exists():
        return candidatos

    for archivo in carpeta_origen.iterdir():
        if archivo.suffix == ".json" or not archivo.is_file():
            continue
        m = PATRON_ARCHIVO.match(archivo.name)
        if not m:
            continue
        slug = m.group("slug")
        n = int(m.group("n"))
        if slug not in candidatos or n < candidatos[slug][0]:
            candidatos[slug] = (n, archivo)

    return {slug: archivo for slug, (n, archivo) in candidatos.items()}


def sincronizar(origen: Path, destino: Path, forzar: bool):
    reporte = {"copiadas": [], "omitidas_ya_existe": [], "sin_datos": []}

    for categoria in CATEGORIAS:
        carpeta_origen = origen / categoria
        carpeta_destino = destino / categoria
        carpeta_destino.mkdir(parents=True, exist_ok=True)

        por_slug = agrupar_por_slug(carpeta_origen)
        if not por_slug:
            reporte["sin_datos"].append(categoria)
            continue

        for slug, archivo_origen in por_slug.items():
            destino_archivo = carpeta_destino / f"{slug}{archivo_origen.suffix}"

            if destino_archivo.exists() and not forzar:
                reporte["omitidas_ya_existe"].append(str(destino_archivo))
                continue

            shutil.copyfile(archivo_origen, destino_archivo)

            # Copiamos también el sidecar de licencia/autor si existe,
            # para no perder la trazabilidad al pasar de un proyecto a otro.
            sidecar_origen = archivo_origen.with_suffix(archivo_origen.suffix + ".json")
            if sidecar_origen.exists():
                sidecar_destino = destino_archivo.with_suffix(destino_archivo.suffix + ".json")
                shutil.copyfile(sidecar_origen, sidecar_destino)

            reporte["copiadas"].append(f"{categoria}/{slug}{archivo_origen.suffix}")

    return reporte


def main():
    parser = argparse.ArgumentParser(description="Sincroniza imágenes de OSINT Search Pro hacia RockQuest.")
    parser.add_argument(
        "--rockquest",
        type=str,
        default=None,
        help="Ruta a la carpeta rockquest-main. Por defecto: ../rockquest-main junto a este script.",
    )
    parser.add_argument(
        "--forzar",
        action="store_true",
        help="Sobrescribe imágenes que ya existan en RockQuest.",
    )
    args = parser.parse_args()

    aqui = Path(__file__).resolve().parent
    origen = aqui / "static" / "descargas"

    if args.rockquest:
        destino = Path(args.rockquest).resolve() / "app" / "static" / "images"
    else:
        destino = (aqui.parent / "rockquest-main" / "app" / "static" / "images").resolve()

    if not destino.parent.exists():
        print(f"⚠ No encontré la carpeta de RockQuest en: {destino}")
        print("  Pasá la ruta correcta con --rockquest /ruta/a/rockquest-main")
        return

    reporte = sincronizar(origen, destino, args.forzar)

    print("\n=== Reporte de sincronización ===")
    print(f"Copiadas ({len(reporte['copiadas'])}):")
    for f in reporte["copiadas"]:
        print(f"  ✔ {f}")

    if reporte["omitidas_ya_existe"]:
        print(f"\nOmitidas, ya existían en RockQuest ({len(reporte['omitidas_ya_existe'])}) — usá --forzar para pisarlas:")
        for f in reporte["omitidas_ya_existe"]:
            print(f"  ⏭ {f}")

    if reporte["sin_datos"]:
        print(f"\nCategorías sin descargas todavía: {', '.join(reporte['sin_datos'])}")

    print(f"\nDestino usado: {destino}")


if __name__ == "__main__":
    main()
