"""Detección automática del tipo de consulta introducida por el usuario."""
import re

EMAIL_RE = re.compile(r"^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$")
IPV4_RE = re.compile(
    r"^(25[0-5]|2[0-4]\d|1\d{2}|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d{2}|[1-9]?\d)){3}$"
)
IPV6_RE = re.compile(r"^[0-9a-fA-F:]{3,}$")
DOMAIN_RE = re.compile(
    r"^(?!-)[A-Za-z0-9-]{1,63}(?<!-)(\.[A-Za-z0-9-]{1,63})+$"
)
URL_RE = re.compile(r"^https?://", re.IGNORECASE)
PHONE_RE = re.compile(r"^\+?[0-9][0-9\s\-\(\)]{6,17}[0-9]$")
USERNAME_RE = re.compile(r"^@?[A-Za-z0-9_.\-]{2,32}$")

HASH_LENGTHS = {
    32: "MD5",
    40: "SHA-1",
    56: "SHA-224",
    64: "SHA-256",
    96: "SHA-384",
    128: "SHA-512",
}
HEX_RE = re.compile(r"^[a-fA-F0-9]+$")

TYPE_LABELS = {
    "email": "Email",
    "ip": "Dirección IP",
    "domain": "Dominio",
    "url": "URL",
    "hash": "Hash",
    "phone": "Teléfono",
    "username": "Usuario",
    "name": "Persona / Nombre",
}


def detectar_tipo(consulta: str) -> dict:
    """Devuelve {'tipo': str, 'label': str, 'valor': str} según el patrón detectado."""
    if not consulta:
        return {"tipo": "name", "label": TYPE_LABELS["name"], "valor": ""}

    q = consulta.strip()

    if URL_RE.match(q):
        return {"tipo": "url", "label": TYPE_LABELS["url"], "valor": q}

    if EMAIL_RE.match(q):
        return {"tipo": "email", "label": TYPE_LABELS["email"], "valor": q}

    if IPV4_RE.match(q):
        return {"tipo": "ip", "label": TYPE_LABELS["ip"], "valor": q}

    if ":" in q and IPV6_RE.match(q) and q.count(":") >= 2:
        return {"tipo": "ip", "label": TYPE_LABELS["ip"], "valor": q}

    if HEX_RE.match(q) and len(q) in HASH_LENGTHS:
        return {
            "tipo": "hash",
            "label": f"Hash ({HASH_LENGTHS[len(q)]})",
            "valor": q,
        }

    if DOMAIN_RE.match(q) and "." in q and " " not in q:
        return {"tipo": "domain", "label": TYPE_LABELS["domain"], "valor": q}

    if PHONE_RE.match(q):
        return {"tipo": "phone", "label": TYPE_LABELS["phone"], "valor": q}

    if q.startswith("@") or (USERNAME_RE.match(q) and " " not in q and len(q.split()) == 1 and not q.replace(".", "").isdigit()):
        # Heurística: una sola palabra sin espacios, alfanumérica -> posible usuario
        if len(q.split()) == 1 and len(q) <= 32:
            return {
                "tipo": "username",
                "label": TYPE_LABELS["username"],
                "valor": q.lstrip("@"),
            }

    return {"tipo": "name", "label": TYPE_LABELS["name"], "valor": q}
