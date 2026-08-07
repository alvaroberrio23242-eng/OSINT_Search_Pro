import hashlib

from services.http_utils import safe_get


def _mx_records(dominio):
    try:
        import dns.resolver

        respuestas = dns.resolver.resolve(dominio, "MX")
        return sorted(
            [{"prioridad": r.preference, "servidor": str(r.exchange).rstrip(".")} for r in respuestas],
            key=lambda x: x["prioridad"],
        )
    except Exception as e:
        return {"error": str(e)}


def _dns_basico(dominio):
    registros = {}
    try:
        import dns.resolver

        for tipo in ("A", "AAAA", "NS", "TXT"):
            try:
                respuestas = dns.resolver.resolve(dominio, tipo)
                registros[tipo] = [str(r).strip('"') for r in respuestas]
            except Exception:
                registros[tipo] = []
    except Exception as e:
        registros["error"] = str(e)
    return registros


def _gravatar(email):
    email_hash = hashlib.md5(email.strip().lower().encode("utf-8")).hexdigest()
    url = f"https://www.gravatar.com/avatar/{email_hash}?d=404"
    perfil_url = f"https://www.gravatar.com/{email_hash}"
    existe = None
    try:
        r = safe_get(url, timeout=4)
        existe = r.status_code == 200
    except Exception:
        existe = None
    return {"hash": email_hash, "avatar_url": url, "perfil_url": perfil_url, "existe": existe}


def _github_por_email(email):
    try:
        r = safe_get(
            "https://api.github.com/search/users",
            params={"q": f"{email} in:email"},
            timeout=5,
        )
        if r.status_code == 200:
            data = r.json()
            items = [
                {"usuario": it.get("login"), "perfil": it.get("html_url"), "avatar": it.get("avatar_url")}
                for it in data.get("items", [])[:5]
            ]
            return {"total": data.get("total_count", 0), "resultados": items}
        return {"total": 0, "resultados": [], "nota": f"GitHub respondió {r.status_code} (límite de tasa sin autenticar)"}
    except Exception as e:
        return {"total": 0, "resultados": [], "error": str(e)}


def analizar_email(email: str) -> dict:
    dominio = email.split("@")[-1] if "@" in email else ""
    return {
        "email": email,
        "dominio": dominio,
        "mx": _mx_records(dominio) if dominio else [],
        "dns": _dns_basico(dominio) if dominio else {},
        "gravatar": _gravatar(email),
        "github": _github_por_email(email),
    }
