from concurrent.futures import ThreadPoolExecutor, as_completed

from services.http_utils import get_session

# Cada entrada define cómo comprobar si un usuario existe en la plataforma.
# 'not_found_text' permite distinguir páginas que siempre devuelven 200
# pero muestran un mensaje de "no encontrado".
PLATAFORMAS = {
    "GitHub":    {"url": "https://github.com/{u}", "not_found_status": [404]},
    "Reddit":    {"url": "https://www.reddit.com/user/{u}/about.json", "not_found_status": [404]},
    "Twitter/X": {"url": "https://x.com/{u}", "not_found_status": [404]},
    "Instagram": {"url": "https://www.instagram.com/{u}/", "not_found_status": [404]},
    "TikTok":    {"url": "https://www.tiktok.com/@{u}", "not_found_status": [404], "not_found_text": ["Couldn't find this account"]},
    "Facebook":  {"url": "https://www.facebook.com/{u}", "not_found_status": [404]},
    "Pinterest": {"url": "https://www.pinterest.com/{u}/", "not_found_status": [404]},
    "Steam":     {"url": "https://steamcommunity.com/id/{u}", "not_found_status": [404], "not_found_text": ["The specified profile could not be found"]},
    "Twitch":    {"url": "https://www.twitch.tv/{u}", "not_found_status": [404]},
    "YouTube":   {"url": "https://www.youtube.com/@{u}", "not_found_status": [404]},
}


def _check(nombre, cfg, usuario):
    url = cfg["url"].format(u=usuario)
    try:
        session = get_session()
        r = session.get(url, timeout=6, allow_redirects=True)
        existe = r.status_code not in cfg.get("not_found_status", [404])
        for frase in cfg.get("not_found_text", []):
            if frase.lower() in r.text.lower():
                existe = False
        return {
            "plataforma": nombre,
            "url": url,
            "existe": existe,
            "status": r.status_code,
        }
    except Exception as e:
        return {"plataforma": nombre, "url": url, "existe": None, "error": str(e)}


def buscar_usuario(usuario: str) -> list:
    usuario = usuario.strip().lstrip("@")
    salida = []
    with ThreadPoolExecutor(max_workers=len(PLATAFORMAS)) as ex:
        futuros = {
            ex.submit(_check, nombre, cfg, usuario): nombre for nombre, cfg in PLATAFORMAS.items()
        }
        for fut in as_completed(futuros):
            salida.append(fut.result())

    orden = {n: i for i, n in enumerate(PLATAFORMAS.keys())}
    salida.sort(key=lambda r: orden.get(r["plataforma"], 99))
    return salida
