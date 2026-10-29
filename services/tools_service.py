import base64
import hashlib
import secrets
import string
from urllib.parse import unquote, urlparse

from services.http_utils import safe_get_public

# ---------- Base64 ----------


def base64_encode(texto: str) -> str:
    return base64.b64encode(texto.encode("utf-8")).decode("utf-8")


def base64_decode(texto: str) -> dict:
    try:
        return {"ok": True, "resultado": base64.b64decode(texto).decode("utf-8", errors="replace")}
    except Exception as e:
        return {"ok": False, "error": str(e)}


# ---------- Hashes ----------

ALGORITMOS = ["md5", "sha1", "sha224", "sha256", "sha384", "sha512"]


def generar_hashes(texto: str) -> dict:
    data = texto.encode("utf-8")
    return {algo: hashlib.new(algo, data).hexdigest() for algo in ALGORITMOS}


HASH_LENGTHS = {
    32: ["MD5", "NTLM", "MD4"],
    40: ["SHA-1"],
    56: ["SHA-224"],
    64: ["SHA-256"],
    96: ["SHA-384"],
    128: ["SHA-512"],
}


def identificar_hash(valor: str) -> dict:
    valor = valor.strip()
    es_hex = all(c in "0123456789abcdefABCDEF" for c in valor)
    posibles = HASH_LENGTHS.get(len(valor), []) if es_hex else []
    if valor.startswith("$2a$") or valor.startswith("$2b$") or valor.startswith("$2y$"):
        posibles = ["bcrypt"]
    elif valor.startswith("$1$"):
        posibles = ["MD5 crypt"]
    elif valor.startswith("$6$"):
        posibles = ["SHA-512 crypt"]
    return {"valor": valor, "longitud": len(valor), "hex_valido": es_hex, "posibles": posibles or ["Desconocido"]}


# ---------- URL ----------


def url_decode(texto: str) -> str:
    return unquote(texto)


def analizar_url(url: str) -> dict:
    p = urlparse(url)
    return {
        "esquema": p.scheme,
        "host": p.netloc,
        "ruta": p.path,
        "query": p.query,
        "fragmento": p.fragment,
    }


# ---------- Password generator ----------


def generar_password(longitud: int = 16, mayus=True, numeros=True, simbolos=True) -> str:
    longitud = max(4, min(longitud, 128))
    alfabeto = string.ascii_lowercase
    if mayus:
        alfabeto += string.ascii_uppercase
    if numeros:
        alfabeto += string.digits
    if simbolos:
        alfabeto += "!@#$%^&*()-_=+[]{}"
    return "".join(secrets.choice(alfabeto) for _ in range(longitud))


# ---------- DNS lookup ----------


def dns_lookup(dominio: str) -> dict:
    registros = {}
    try:
        import dns.resolver

        for tipo in ("A", "AAAA", "MX", "NS", "TXT", "CNAME", "SOA"):
            try:
                respuestas = dns.resolver.resolve(dominio, tipo)
                registros[tipo] = [str(r).strip('"') for r in respuestas]
            except Exception:
                registros[tipo] = []
    except Exception as e:
        registros["error"] = str(e)
    return registros


# ---------- Robots.txt viewer ----------


def ver_robots(dominio: str) -> dict:
    dominio = dominio.replace("http://", "").replace("https://", "").split("/")[0]
    for esquema in ("https", "http"):
        try:
            r = safe_get_public(f"{esquema}://{dominio}/robots.txt", timeout=6)
            if r.status_code == 200:
                return {"ok": True, "url": r.url, "contenido": r.text[:8000]}
        except Exception:
            continue
    return {"ok": False, "error": "No se pudo obtener robots.txt"}


# ---------- HTTP headers viewer ----------


def ver_headers(url: str) -> dict:
    if not url.startswith("http"):
        url = "https://" + url
    try:
        r = safe_get_public(url, timeout=8)
        return {"ok": True, "url": r.url, "status": r.status_code, "headers": dict(r.headers)}
    except Exception as e:
        return {"ok": False, "error": str(e)}


# ---------- QR generator (usa API pública, sin key, solo genera la URL de la imagen) ----------


def qr_url(texto: str, tamano: int = 300) -> str:
    from urllib.parse import quote

    return f"https://api.qrserver.com/v1/create-qr-code/?size={tamano}x{tamano}&data={quote(texto)}"
