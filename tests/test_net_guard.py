import pytest

from services import http_utils, net_guard


def _resolver(monkeypatch, *ips):
    monkeypatch.setattr(net_guard, "_resolver_todas", lambda host: set(ips))


@pytest.mark.parametrize("ip", [
    "127.0.0.1", "10.0.0.5", "192.168.1.10", "172.16.0.1", "169.254.169.254",
    "0.0.0.0", "::1", "fe80::1", "100.64.0.1", "::ffff:127.0.0.1", "224.0.0.1",
])
def test_ip_no_publica_rechazada(ip):
    assert net_guard.validar_ip_publica(ip)[0] is False


@pytest.mark.parametrize("ip", ["8.8.8.8", "1.1.1.1", "2606:4700:4700::1111"])
def test_ip_publica_aceptada(ip):
    assert net_guard.validar_ip_publica(ip)[0] is True


@pytest.mark.parametrize("malo", ["abc", "", "999.1.1.1", None, 123, "8.8.8.8/../x"])
def test_ip_invalida(malo):
    assert net_guard.validar_ip_publica(malo)[0] is False


def test_dominio_se_normaliza():
    assert net_guard.validar_dominio("Example.COM") == (True, "", "example.com")
    assert net_guard.validar_dominio("https://example.com:8080/ruta?x=1")[2] == "example.com"


@pytest.mark.parametrize("malo", [
    "localhost", "127.0.0.1", "a b.com", "-x.com", "exa_mple.com", "", None,
    "x" * 300 + ".com", "https://user:pass@example.com/", "example.com:22", "evil.com\\@good.com",
])
def test_dominio_invalido(malo):
    assert net_guard.validar_dominio(malo)[0] is False


def test_destino_rechaza_resolucion_interna(monkeypatch):
    _resolver(monkeypatch, "10.0.0.1")
    assert net_guard.validar_destino("https://interno.example.com/")[0] is False


def test_destino_rechaza_resolucion_mixta(monkeypatch):
    _resolver(monkeypatch, "93.184.216.34", "127.0.0.1")
    assert net_guard.validar_destino("https://mixto.example.com/")[0] is False


def test_destino_publico_ok(monkeypatch):
    _resolver(monkeypatch, "93.184.216.34")
    ok, _, host = net_guard.validar_destino("https://Example.com/ruta")
    assert ok is True and host == "example.com"


@pytest.mark.parametrize("url", [
    "http://127.0.0.1/", "http://[::1]/", "http://169.254.169.254/latest/meta-data/",
    "http://10.1.2.3:8080/", "http://localhost/", "file:///etc/passwd", "gopher://127.0.0.1:6379/",
])
def test_destino_rechaza_internos(url):
    assert net_guard.validar_destino(url)[0] is False


def test_destino_ip_publica_literal():
    assert net_guard.validar_destino("http://8.8.8.8/")[0] is True


def test_email():
    assert net_guard.validar_email("ana@example.com")[0] is True
    for malo in ["ana@localhost", "sin-arroba", "", None, 5]:
        assert net_guard.validar_email(malo)[0] is False


def test_texto_libre():
    assert net_guard.validar_texto_libre("Ana Maria Perez", 100)[0] is True
    for malo in ["../../etc", "a/b", "x?y", "a@b", "", None, "z" * 101]:
        assert net_guard.validar_texto_libre(malo, 100)[0] is False


class _Resp:
    def __init__(self, status, headers=None, body=b""):
        self.status_code = status
        self.headers = headers or {}
        self._body = body
        self.url = ""

    def close(self):
        pass

    def raise_for_status(self):
        pass

    def iter_content(self, n):
        yield self._body


class _Sesion:
    def __init__(self, resp):
        self.headers = {}
        self._resp = resp

    def get(self, url, **kwargs):
        return self._resp


def test_redireccion_a_red_interna_bloqueada(monkeypatch):
    _resolver(monkeypatch, "93.184.216.34")
    resp = _Resp(302, {"Location": "http://127.0.0.1:8080/admin"})
    monkeypatch.setattr(http_utils, "get_session", lambda: _Sesion(resp))
    with pytest.raises(ValueError):
        http_utils.safe_get_public("https://example.com/")


def test_respuesta_normal_y_tope_de_tamano(monkeypatch):
    _resolver(monkeypatch, "93.184.216.34")
    resp = _Resp(200, {}, b"hola")
    monkeypatch.setattr(http_utils, "get_session", lambda: _Sesion(resp))
    r = http_utils.safe_get_public("https://example.com/")
    assert r._content == b"hola"
