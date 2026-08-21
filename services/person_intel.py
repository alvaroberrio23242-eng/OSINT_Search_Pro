"""Investigación de una persona por nombre completo.

Combina dos cosas distintas a propósito:

1. Menciones reales en la web: reutiliza el motor multi-buscador (mismo que
   usa Inicio) con el nombre completo como consulta. Esto SÍ trae resultados
   indexados públicamente (noticias, blogs, perfiles públicos, foros...).

2. Enlaces dirigidos: para sitios que bloquean scraping agresivamente o lo
   prohíben en sus términos (LinkedIn, plataformas de cursos, bases de datos
   legales/judiciales), no se intenta traer datos automáticamente. En su
   lugar se generan enlaces de búsqueda ya armados que el usuario abre y
   revisa él mismo. Es la diferencia entre "la app inventa que existe un
   perfil" y "la app te ahorra escribir la búsqueda".

No se incluye NADA relacionado con números de WhatsApp/teléfono o historial
académico privado: no existe una fuente pública y gratuita legítima para eso,
y cualquier resultado de ese tipo sería inventado o vendría de una base de
datos filtrada, ninguna de las dos aceptable aquí.
"""

from urllib.parse import quote_plus

from services.search_service import realizar_busqueda

_SITIOS_PROFESIONALES = [
    ("LinkedIn", "linkedin.com/in"),
    ("Facebook", "facebook.com"),
    ("Instagram", "instagram.com"),
]

_SITIOS_EDUCACION = [
    ("Coursera", "coursera.org"),
    ("Platzi", "platzi.com"),
    ("LinkedIn Learning", "linkedin.com/learning"),
    ("Udemy", "udemy.com"),
]

_SITIOS_LEGALES_CO = [
    ("Rama Judicial (procesos)", "consultaprocesos.ramajudicial.gov.co"),
    ("Procuraduría (antecedentes)", "procuraduria.gov.co"),
    ("RUES (registro mercantil)", "rues.org.co"),
]


def _dork_url(nombre, dominio=None, sitio_extra=None):
    q = f'"{nombre}"'
    if dominio:
        q += f" site:{dominio}"
    if sitio_extra:
        q += f" {sitio_extra}"
    return f"https://www.google.com/search?q={quote_plus(q)}"


def generar_enlaces_dirigidos(nombre):
    """Enlaces de búsqueda ya armados, agrupados por categoría. No hace
    ninguna petición de red: solo arma URLs de búsqueda."""
    return {
        "redes_profesionales": [
            {"nombre": etiqueta, "url": _dork_url(nombre, dominio)}
            for etiqueta, dominio in _SITIOS_PROFESIONALES
        ],
        "educacion_cursos": [
            {"nombre": etiqueta, "url": _dork_url(nombre, dominio)}
            for etiqueta, dominio in _SITIOS_EDUCACION
        ],
        "registros_legales_co": [
            {"nombre": etiqueta, "url": _dork_url(nombre, dominio)}
            for etiqueta, dominio in _SITIOS_LEGALES_CO
        ],
    }


def investigar_persona(nombre, motores=None, limite=None):
    nombre = nombre.strip()
    menciones = realizar_busqueda(nombre, motores=motores, limite=limite)
    enlaces = generar_enlaces_dirigidos(nombre)
    return {
        "nombre": nombre,
        "menciones_web": menciones,
        "enlaces_dirigidos": enlaces,
        "aviso": (
            "LinkedIn y sitios similares bloquean la lectura automática y no "
            "permiten hacerlo según sus términos de uso, así que se generan "
            "enlaces de búsqueda para revisarlos manualmente en vez de "
            "intentar extraer datos de ellos. No se incluyen datos privados "
            "(teléfono, WhatsApp, historial académico) porque no existe una "
            "fuente pública y legítima gratuita para eso."
        ),
    }
