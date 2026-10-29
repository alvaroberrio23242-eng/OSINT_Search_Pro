import random
import time

import requests

from config import Config
from services import net_guard


class MotorBloqueadoError(Exception):
    """Se lanza cuando el motor responde 403/429/503: bloqueo o rate-limit,
    no ausencia real de resultados. Permite que la UI distinga ambos casos."""

    def __init__(self, status_code):
        self.status_code = status_code
        super().__init__(f"Bloqueado o limitado por el motor (HTTP {status_code})")


# Varios User-Agent reales para no golpear siempre con la misma huella
_USER_AGENTS = [
    Config.USER_AGENT,
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 "
    "(KHTML, like Gecko) Version/17.4 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/124.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0",
]


def get_session():
    s = requests.Session()
    s.headers.update(
        {
            "User-Agent": random.choice(_USER_AGENTS),
            "Accept-Language": "es-ES,es;q=0.9,en;q=0.8",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Cache-Control": "no-cache",
        }
    )
    return s


def safe_get(url, params=None, timeout=None, headers=None, reintentos=2):
    """GET con reintentos y backoff. Lanza MotorBloqueadoError en 403/429/503
    (para no confundir un bloqueo con "0 resultados"), y deja pasar el resto
    de errores HTTP tal cual para que el motor los reporte."""
    ultimo_error = None
    for intento in range(reintentos + 1):
        session = get_session()
        if headers:
            session.headers.update(headers)
        try:
            r = session.get(url, params=params, timeout=timeout or Config.HTTP_TIMEOUT)
        except requests.RequestException as e:
            ultimo_error = e
            time.sleep(0.4 * (intento + 1))
            continue

        if r.status_code in (403, 429, 503):
            ultimo_error = MotorBloqueadoError(r.status_code)
            time.sleep(0.6 * (intento + 1) + random.random() * 0.3)
            continue

        r.raise_for_status()
        return r

    raise ultimo_error


def safe_get_public(url, timeout=None, headers=None, max_redirects=3, max_bytes=1_000_000):
    """GET para destinos escritos por el usuario (anti-SSRF).

    Valida el destino en cada salto, incluidas las redirecciones, y limita el
    tamano de la respuesta. No usar para las URLs fijas de los motores.
    """
    from urllib.parse import urljoin, urlparse

    actual = url
    for _ in range(max_redirects + 1):
        if urlparse(actual).scheme not in ("http", "https"):
            raise ValueError("Solo se permiten URLs http o https")
        ok, motivo, _host = net_guard.validar_destino(actual)
        if not ok:
            raise ValueError(motivo)

        session = get_session()
        if headers:
            session.headers.update(headers)
        r = session.get(
            actual,
            timeout=timeout or Config.HTTP_TIMEOUT,
            allow_redirects=False,
            stream=True,
        )

        if r.status_code in (301, 302, 303, 307, 308):
            destino = r.headers.get("Location")
            r.close()
            if not destino:
                raise ValueError("Redireccion sin destino")
            actual = urljoin(actual, destino)
            continue

        if r.status_code in (403, 429, 503):
            r.close()
            raise MotorBloqueadoError(r.status_code)
        r.raise_for_status()

        partes, total = [], 0
        for trozo in r.iter_content(8192):
            partes.append(trozo)
            total += len(trozo)
            if total >= max_bytes:
                break
        r.close()
        r._content = b"".join(partes)
        r._content_consumed = True
        return r

    raise ValueError("Demasiadas redirecciones")
