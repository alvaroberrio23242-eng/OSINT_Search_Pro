import requests
from config import Config


def get_session():
    s = requests.Session()
    s.headers.update(
        {
            "User-Agent": Config.USER_AGENT,
            "Accept-Language": "es-ES,es;q=0.9,en;q=0.8",
        }
    )
    return s


def safe_get(url, params=None, timeout=None, headers=None):
    session = get_session()
    if headers:
        session.headers.update(headers)
    return session.get(url, params=params, timeout=timeout or Config.HTTP_TIMEOUT)
