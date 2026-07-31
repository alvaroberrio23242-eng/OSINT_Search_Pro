from flask import Flask, render_template, request
from buscadores.duckduckgo import buscar

app = Flask(__name__)


@app.route("/")
def inicio():
    return render_template("index.html")


@app.route("/buscar", methods=["POST"])
def buscar_web():
    consulta = request.form["consulta"]

    resultados = buscar(consulta)

    return render_template(
        "resultados.html",
        consulta=consulta,
        resultados=resultados
    )


if __name__ == "__main__":
    app.run(debug=True)