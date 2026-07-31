from flask import Blueprint, render_template, request
from services.search_service import realizar_busqueda

search = Blueprint("search", __name__)


@search.route("/")
def inicio():
    return render_template("index.html")


@search.route("/buscar", methods=["POST"])
def buscar():
    consulta = request.form.get("consulta", "")

    resultados = realizar_busqueda(consulta)

    return render_template(
        "resultados.html",
        consulta=consulta,
        resultados=resultados
    )