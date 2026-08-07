import re
import unicodedata


def slugify(texto: str) -> str:
    """
    Convierte un nombre (ej. "The Beatles") en un slug para nombre de
    archivo (ej. "the-beatles"). Coincide con la lógica usada en
    RockQuest (app/services/utils.py) para que los nombres de archivo
    generados acá encajen directamente en static/images/<categoria>/
    del otro proyecto.
    """
    if not texto:
        return ""
    texto = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode("ascii")
    texto = texto.lower().strip()
    texto = re.sub(r"[^a-z0-9]+", "-", texto)
    texto = re.sub(r"-+", "-", texto).strip("-")
    return texto
