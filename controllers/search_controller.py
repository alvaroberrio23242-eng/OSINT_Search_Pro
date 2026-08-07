from flask import Blueprint, render_template, request
from services.search_service import realizar_busqueda

search = Blueprint("search", __name__)


@search.route("/")
def inicio():
    return render_template("index.html")


@search.route("/buscar", methods=["POST"])
def buscar():
    consulta = request.form.get("consulta", "")
    resultados = []
    error = None

    if not consulta.strip():
        error = "Escribe algo para buscar."
    else:
        try:
            resultados = realizar_busqueda(consulta)
        except Exception as e:
            # ddgs hace scraping de motores de busqueda reales (DuckDuckGo/
            # Bing/etc), y esos motores bloquean por rate-limit con
            # frecuencia -- no es un bug nuestro, pero sin este try/except
            # el usuario veia un error 500 crudo de Flask en vez de un
            # aviso claro. Si vuelve a pasar seguido, toca reintentar con
            # backoff o cambiar a una API oficial de busqueda con key.
            error = (
                "El motor de búsqueda está saturado o bloqueó la consulta "
                "por un momento (esto pasa seguido con scraping de "
                "buscadores públicos). Intenta de nuevo en unos segundos."
            )

    return render_template(
        "resultados.html",
        consulta=consulta,
        resultados=resultados,
        error=error,
    )