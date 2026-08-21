import time

from flask import Blueprint, jsonify, request

from extensions import limiter

from services import dorks as dorks_service
from services import email_intel, domain_intel, ip_intel, username_intel, tools_service, person_intel
from services.detector import detectar_tipo
from services.search_service import realizar_busqueda, motores_disponibles

api = Blueprint("api", __name__, url_prefix="/api")


@api.route("/detect", methods=["POST"])
def detect():
    consulta = (request.json or {}).get("consulta", "")
    return jsonify(detectar_tipo(consulta))


@api.route("/motores")
def motores():
    return jsonify(motores_disponibles())


@api.route("/search", methods=["POST"])
@limiter.limit("15 per minute")
def search():
    body = request.json or {}
    consulta = body.get("consulta", "").strip()
    motores = body.get("motores") or None

    inicio = time.time()
    tipo = detectar_tipo(consulta)

    if not consulta:
        return jsonify({"error": "Consulta vacía"}), 400

    resultados = realizar_busqueda(consulta, motores=motores)
    duracion = round(time.time() - inicio, 2)

    total = sum(len(r["resultados"]) for r in resultados)

    return jsonify(
        {
            "consulta": consulta,
            "tipo": tipo,
            "duracion_seg": duracion,
            "total_resultados": total,
            "motores": resultados,
        }
    )


@api.route("/dorks", methods=["POST"])
def dorks():
    consulta = (request.json or {}).get("consulta", "")
    return jsonify(dorks_service.generar_dorks(consulta))


@api.route("/lookup/email", methods=["POST"])
@limiter.limit("10 per minute")
def lookup_email():
    email = (request.json or {}).get("email", "").strip()
    if not email:
        return jsonify({"error": "Email vacío"}), 400
    return jsonify(email_intel.analizar_email(email))


@api.route("/lookup/domain", methods=["POST"])
@limiter.limit("10 per minute")
def lookup_domain():
    dominio = (request.json or {}).get("dominio", "").strip()
    if not dominio:
        return jsonify({"error": "Dominio vacío"}), 400
    return jsonify(domain_intel.analizar_dominio(dominio))


@api.route("/lookup/ip", methods=["POST"])
@limiter.limit("10 per minute")
def lookup_ip():
    body = request.json or {}
    ip = body.get("ip", "").strip()
    escanear = bool(body.get("escanear_puertos", True))
    if not ip:
        return jsonify({"error": "IP vacía"}), 400
    return jsonify(ip_intel.analizar_ip(ip, escanear_puertos=escanear))


@api.route("/lookup/username", methods=["POST"])
@limiter.limit("10 per minute")
def lookup_username():
    usuario = (request.json or {}).get("usuario", "").strip()
    if not usuario:
        return jsonify({"error": "Usuario vacío"}), 400
    return jsonify({"usuario": usuario, "plataformas": username_intel.buscar_usuario(usuario)})


@api.route("/lookup/persona", methods=["POST"])
@limiter.limit("10 per minute")
def lookup_persona():
    body = request.json or {}
    nombre = body.get("nombre", "").strip()
    if not nombre:
        return jsonify({"error": "Nombre vacío"}), 400
    return jsonify(person_intel.investigar_persona(nombre))


# ---------------- Herramientas ----------------


@api.route("/tools/base64", methods=["POST"])
def tools_base64():
    body = request.json or {}
    modo = body.get("modo", "encode")
    texto = body.get("texto", "")
    if modo == "decode":
        return jsonify(tools_service.base64_decode(texto))
    return jsonify({"ok": True, "resultado": tools_service.base64_encode(texto)})


@api.route("/tools/hash", methods=["POST"])
def tools_hash():
    texto = (request.json or {}).get("texto", "")
    return jsonify(tools_service.generar_hashes(texto))


@api.route("/tools/hash-identify", methods=["POST"])
def tools_hash_identify():
    valor = (request.json or {}).get("valor", "")
    return jsonify(tools_service.identificar_hash(valor))


@api.route("/tools/url", methods=["POST"])
def tools_url():
    body = request.json or {}
    texto = body.get("texto", "")
    return jsonify({"decoded": tools_service.url_decode(texto), "partes": tools_service.analizar_url(texto)})


@api.route("/tools/password", methods=["POST"])
def tools_password():
    body = request.json or {}
    resultado = tools_service.generar_password(
        longitud=int(body.get("longitud", 16)),
        mayus=bool(body.get("mayus", True)),
        numeros=bool(body.get("numeros", True)),
        simbolos=bool(body.get("simbolos", True)),
    )
    return jsonify({"password": resultado})


@api.route("/tools/dns", methods=["POST"])
def tools_dns():
    dominio = (request.json or {}).get("dominio", "")
    return jsonify(tools_service.dns_lookup(dominio))


@api.route("/tools/robots", methods=["POST"])
def tools_robots():
    dominio = (request.json or {}).get("dominio", "")
    return jsonify(tools_service.ver_robots(dominio))


@api.route("/tools/headers", methods=["POST"])
def tools_headers():
    url = (request.json or {}).get("url", "")
    return jsonify(tools_service.ver_headers(url))


@api.route("/tools/qr", methods=["POST"])
def tools_qr():
    body = request.json or {}
    texto = body.get("texto", "")
    tamano = int(body.get("tamano", 300))
    return jsonify({"url": tools_service.qr_url(texto, tamano)})
