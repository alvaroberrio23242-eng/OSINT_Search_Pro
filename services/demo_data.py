"""Resultados de muestra para cuando un motor de búsqueda está bloqueado
(HTTP 403/429/503) o sin librería disponible. No son resultados reales:
sirven para que el demo del portafolio se vea completo y coherente incluso
en hosting (Railway/Render) donde Google/Bing/etc. bloquean el tráfico de
datacenter.

TODO: reemplazar por integraciones con APIs oficiales (Google Custom Search,
Bing Search API v7, Brave Search API) cuando el proyecto pase a producción
real. Este archivo queda pensado para desaparecer ese día.
"""

import hashlib


def _seed(consulta, motor):
    """Determinístico: la misma consulta+motor siempre da los mismos
    resultados de muestra, para que la demo no parezca aleatoria."""
    h = hashlib.md5(f"{motor}:{consulta}".encode()).hexdigest()
    return int(h[:8], 16)


_PLANTILLAS = [
    ("{q} — panorama general y contexto", "Resumen introductorio sobre '{q}' con los puntos más relevantes y enlaces relacionados."),
    ("Todo sobre {q} en {motor}", "Artículo de referencia que cubre los aspectos principales de '{q}'."),
    ("{q}: guía actualizada", "Recopilación de información reciente y fuentes verificadas sobre '{q}'."),
    ("Noticias recientes sobre {q}", "Últimas menciones y actualizaciones relacionadas con '{q}'."),
    ("{q} — preguntas frecuentes", "Respuestas a las dudas más comunes relacionadas con '{q}'."),
]


def generar_resultados_demo(consulta, motor_nombre, limite=5):
    """Genera N resultados de muestra, marcados como demo=True, para un
    motor y consulta dados. No hace ninguna petición de red."""
    limite = max(1, min(limite or 5, len(_PLANTILLAS)))
    seed = _seed(consulta, motor_nombre)
    slug = "".join(c if c.isalnum() else "-" for c in consulta.strip().lower()) or "consulta"

    resultados = []
    for i in range(limite):
        titulo_tpl, desc_tpl = _PLANTILLAS[(seed + i) % len(_PLANTILLAS)]
        resultados.append(
            {
                "titulo": titulo_tpl.format(q=consulta, motor=motor_nombre),
                "descripcion": desc_tpl.format(q=consulta),
                "url": f"https://ejemplo-demo.local/{slug}-{i + 1}",
                "motor": motor_nombre,
                "demo": True,
            }
        )
    return resultados
