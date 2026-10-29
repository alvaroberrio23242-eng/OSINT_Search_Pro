"""Validacion de destinos para evitar SSRF y abuso desde la demo publica.

Regla general: cualquier host que escriba un visitante debe resolver SOLO a
direcciones IP publicas. Se rechazan redes privadas, loopback, link-local
(incluye el endpoint de metadatos 169.254.169.254), CGNAT, multicast y reservadas.
"""
import ipaddress
import re
import socket
from urllib.parse import urlparse

PUERTOS_PERMITIDOS = (None, 80, 443, 8080, 8443)

_RE_ETIQUETA = re.compile(r"^(?!-)[a-z0-9-]{1,63}(?<!-)$")
_RE_EMAIL = re.compile(r"^[^@\s]{1,64}@[^@\s]{1,255}$")
_RE_INVALIDO = re.compile(r"[\s\\\x00-\x1f]")
_RE_PELIGROSO = re.compile(r"[\x00-\x1f/\\?#:@]")

MSG_DOMINIO = "Dominio no v\u00e1lido"
MSG_INTERNO = "Destino no permitido (red interna)"


def _ip_o_none(texto):
    try:
        return ipaddress.ip_address(texto)
    except ValueError:
        return None


def _es_global(ip):
    if ip.version == 6 and ip.ipv4_mapped is not None:
        ip = ip.ipv4_mapped
    return ip.is_global and not (ip.is_multicast or ip.is_reserved)


def validar_ip_publica(texto):
    """Devuelve (ok, motivo). Solo IPs literales publicas."""
    if not isinstance(texto, str):
        return False, "IP no v\u00e1lida"
    ip = _ip_o_none(texto.strip())
    if ip is None:
        return False, "IP no v\u00e1lida"
    if not _es_global(ip):
        return False, "Solo se permiten IPs p\u00fablicas"
    return True, ""


def _extraer_host(texto):
    """Host en minusculas de un dominio o URL; '' si algo no cuadra."""
    if not isinstance(texto, str):
        return ""
    t = texto.strip().lower()
    if not t or len(t) > 300 or _RE_INVALIDO.search(t):
        return ""
    if "://" not in t:
        t = "//" + t
    try:
        p = urlparse(t)
        host = p.hostname or ""
        puerto = p.port
    except ValueError:
        return ""
    if "@" in p.netloc or puerto not in PUERTOS_PERMITIDOS:
        return ""
    return host.rstrip(".")


def _validar_nombre(host):
    if not host or len(host) > 253 or "." not in host:
        return False, MSG_DOMINIO, ""
    try:
        ascii_host = host.encode("idna").decode("ascii")
    except UnicodeError:
        return False, MSG_DOMINIO, ""
    etiquetas = ascii_host.split(".")
    if not all(_RE_ETIQUETA.match(e) for e in etiquetas) or etiquetas[-1].isdigit():
        return False, MSG_DOMINIO, ""
    return True, "", ascii_host


def validar_dominio(texto):
    """Solo formato (sin conexiones): para DNS, WHOIS y email. Devuelve (ok, motivo, dominio)."""
    host = _extraer_host(texto)
    if _ip_o_none(host) is not None:
        return False, "Se esperaba un dominio, no una IP", ""
    return _validar_nombre(host)


def _resolver_todas(host):
    infos = socket.getaddrinfo(host, None, proto=socket.IPPROTO_TCP)
    return {i[4][0] for i in infos}


def _validar_resolucion(host):
    try:
        direcciones = _resolver_todas(host)
    except (socket.gaierror, UnicodeError, OSError):
        return False, "No se pudo resolver el dominio", ""
    if not direcciones:
        return False, "No se pudo resolver el dominio", ""
    for d in direcciones:
        ip = _ip_o_none(d.split("%")[0])
        if ip is None or not _es_global(ip):
            return False, MSG_INTERNO, ""
    return True, "", host


def validar_destino(texto):
    """Para peticiones HTTP salientes. Devuelve (ok, motivo, host)."""
    host = _extraer_host(texto)
    if not host:
        return False, "Destino no v\u00e1lido", ""
    ip = _ip_o_none(host)
    if ip is not None:
        if not _es_global(ip):
            return False, MSG_INTERNO, ""
        return True, "", host
    ok, motivo, host_ascii = _validar_nombre(host)
    if not ok:
        return False, motivo, ""
    return _validar_resolucion(host_ascii)


def validar_email(texto):
    if not isinstance(texto, str):
        return False, "Email no v\u00e1lido"
    t = texto.strip()
    if len(t) > 254 or not _RE_EMAIL.match(t):
        return False, "Email no v\u00e1lido"
    ok, motivo, _ = validar_dominio(t.rsplit("@", 1)[1])
    return (True, "") if ok else (False, motivo)


def validar_texto_libre(valor, max_len=64):
    """Usuarios y nombres: sin separadores de ruta/URL ni caracteres de control."""
    if not isinstance(valor, str):
        return False, "Valor no v\u00e1lido"
    v = valor.strip()
    if not v or len(v) > max_len or _RE_PELIGROSO.search(v):
        return False, "Valor no v\u00e1lido"
    return True, ""
