import pytest


def test_cabeceras_de_seguridad(client):
    r = client.get("/")
    assert r.status_code == 200
    assert r.headers["X-Content-Type-Options"] == "nosniff"
    assert r.headers["X-Frame-Options"] == "DENY"
    assert "Content-Security-Policy-Report-Only" in r.headers


@pytest.mark.parametrize("url", [
    "http://127.0.0.1/", "http://localhost:5000/", "http://169.254.169.254/latest/meta-data/",
    "http://10.0.0.1/", "http://[::1]/", "file:///etc/passwd",
])
def test_headers_bloquea_destinos_internos(client, url):
    assert client.post("/api/tools/headers", json={"url": url}).status_code == 400


@pytest.mark.parametrize("dominio", ["127.0.0.1", "localhost", "10.0.0.1"])
def test_robots_bloquea_destinos_internos(client, dominio):
    assert client.post("/api/tools/robots", json={"dominio": dominio}).status_code == 400


@pytest.mark.parametrize("ip", ["10.0.0.1", "127.0.0.1", "abc", "169.254.169.254"])
def test_lookup_ip_rechaza_no_publicas(client, ip):
    r = client.post("/api/lookup/ip", json={"ip": ip, "escanear_puertos": True})
    assert r.status_code == 400


def test_validaciones_de_entrada(client):
    assert client.post("/api/lookup/domain", json={"dominio": "localhost"}).status_code == 400
    assert client.post("/api/tools/dns", json={"dominio": "127.0.0.1"}).status_code == 400
    assert client.post("/api/lookup/email", json={"email": "a@localhost"}).status_code == 400
    assert client.post("/api/lookup/username", json={"usuario": "../../etc"}).status_code == 400


def test_tipos_inesperados_dan_400_json(client):
    r = client.post("/api/lookup/email", json={"email": 123})
    assert r.status_code == 400
    assert "error" in r.get_json()


def test_cuerpo_demasiado_grande(client):
    r = client.post("/api/tools/hash", data="x" * (300 * 1024), content_type="application/json")
    assert r.status_code == 413


def test_portscan_apagado_por_defecto(client, monkeypatch):
    from services import ip_intel

    monkeypatch.setattr(ip_intel, "_geolocalizar", lambda ip: {"status": "success"})
    monkeypatch.setattr(ip_intel, "_reverse_dns", lambda ip: None)

    def prohibido(ip):
        raise AssertionError("no debe escanear")

    monkeypatch.setattr(ip_intel, "_escaneo_puertos", prohibido)
    r = client.post("/api/lookup/ip", json={"ip": "8.8.8.8", "escanear_puertos": True})
    assert r.status_code == 200
    assert r.get_json()["puertos"] == []


def test_limite_en_tools_dns(client):
    codigos = [client.post("/api/tools/dns", json={"dominio": "x"}).status_code for _ in range(12)]
    assert 429 not in codigos[:10]
    assert 429 in codigos[10:]


def test_limite_en_detect(client):
    codigos = [client.post("/api/detect", json={"consulta": "a"}).status_code for _ in range(32)]
    assert 429 not in codigos[:30]
    assert 429 in codigos[30:]
