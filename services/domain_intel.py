from services.http_utils import safe_get


def _whois(dominio):
    try:
        import whois

        datos = whois.whois(dominio)
        return {
            "registrante": datos.get("org") or datos.get("name"),
            "registrador": datos.get("registrar"),
            "creado": _fmt_fecha(datos.get("creation_date")),
            "expira": _fmt_fecha(datos.get("expiration_date")),
            "actualizado": _fmt_fecha(datos.get("updated_date")),
            "servidores_nombre": datos.get("name_servers"),
            "estado": datos.get("status"),
            "pais": datos.get("country"),
            "emails": datos.get("emails"),
        }
    except Exception as e:
        return {"error": str(e)}


def _fmt_fecha(valor):
    if isinstance(valor, list):
        valor = valor[0] if valor else None
    if valor is None:
        return None
    try:
        return valor.isoformat()
    except AttributeError:
        return str(valor)


def _dns(dominio):
    registros = {}
    try:
        import dns.resolver

        for tipo in ("A", "AAAA", "MX", "NS", "TXT", "SOA", "CNAME"):
            try:
                respuestas = dns.resolver.resolve(dominio, tipo)
                registros[tipo] = [str(r).strip('"') for r in respuestas]
            except Exception:
                registros[tipo] = []
    except Exception as e:
        registros["error"] = str(e)
    return registros


def _subdominios_crtsh(dominio):
    try:
        r = safe_get(f"https://crt.sh/", params={"q": f"%.{dominio}", "output": "json"}, timeout=8)
        if r.status_code != 200:
            return {"total": 0, "subdominios": [], "nota": f"crt.sh respondió {r.status_code}"}
        data = r.json()
        nombres = set()
        for entry in data:
            for n in entry.get("name_value", "").split("\n"):
                n = n.strip().lower()
                if n and not n.startswith("*."):
                    nombres.add(n)
        subs = sorted(nombres)
        return {"total": len(subs), "subdominios": subs[:60]}
    except Exception as e:
        return {"total": 0, "subdominios": [], "error": str(e)}


def analizar_dominio(dominio: str) -> dict:
    dominio = dominio.strip().lower().replace("http://", "").replace("https://", "").split("/")[0]
    return {
        "dominio": dominio,
        "whois": _whois(dominio),
        "dns": _dns(dominio),
        "subdominios": _subdominios_crtsh(dominio),
    }
