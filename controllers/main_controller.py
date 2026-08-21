from flask import Blueprint, render_template

from config import Config
from services.search_service import motores_disponibles

main = Blueprint("main", __name__)


@main.route("/")
def inicio():
    return render_template("index.html", motores=motores_disponibles())


@main.route("/personas")
def personas():
    return render_template("personas.html")


@main.route("/emails")
def emails():
    return render_template("emails.html")


@main.route("/dominios")
def dominios():
    return render_template("dominios.html")


@main.route("/ips")
def ips():
    return render_template("ips.html")


@main.route("/dorks")
def dorks():
    return render_template("dorks.html")


@main.route("/herramientas")
def herramientas():
    return render_template("herramientas.html")


@main.route("/configuracion")
def configuracion():
    return render_template("configuracion.html", servicios=Config.optional_services_status())
