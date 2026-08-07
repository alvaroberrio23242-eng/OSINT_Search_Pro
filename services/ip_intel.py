import socket
from concurrent.futures import ThreadPoolExecutor

from config import Config
from services.http_utils import safe_get

PUERTOS_NOMBRES = {
    21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP", 53: "DNS",
    80: "HTTP", 110: "POP3", 143: "IMAP", 443: "HTTPS",
    3306: "MySQL", 3389: "RDP", 8080: "HTTP-alt",
}


def _geolocalizar(ip):
    try:
        r = safe_get(
            f"http://ip-api.com/json/{ip}",
            params={"fields": "status,message,country,countryCode,region,regionName,city,zip,lat,lon,isp,org,as,asname,reverse,query"},
            timeout=6,
        )
        data = r.json()
        if data.get("status") != "success":
            return {"error": data.get("message", "No se pudo geolocalizar")}
        return data
    except Exception as e:
        return {"error": str(e)}


def _puerto_abierto(ip, puerto):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(Config.PORT_SCAN_TIMEOUT)
            resultado = s.connect_ex((ip, puerto))
            return {"puerto": puerto, "servicio": PUERTOS_NOMBRES.get(puerto, "?"), "abierto": resultado == 0}
    except Exception:
        return {"puerto": puerto, "servicio": PUERTOS_NOMBRES.get(puerto, "?"), "abierto": False}


def _escaneo_puertos(ip):
    """Escaneo ligero de un conjunto reducido de puertos comunes (uso diagnóstico)."""
    try:
        with ThreadPoolExecutor(max_workers=len(Config.COMMON_PORTS)) as ex:
            resultados = list(ex.map(lambda p: _puerto_abierto(ip, p), Config.COMMON_PORTS))
        return sorted(resultados, key=lambda r: r["puerto"])
    except Exception as e:
        return [{"error": str(e)}]


def _reverse_dns(ip):
    try:
        return socket.gethostbyaddr(ip)[0]
    except Exception:
        return None


def analizar_ip(ip: str, escanear_puertos: bool = True) -> dict:
    resultado = {
        "ip": ip,
        "geolocalizacion": _geolocalizar(ip),
        "reverse_dns": _reverse_dns(ip),
    }
    if escanear_puertos:
        resultado["puertos"] = _escaneo_puertos(ip)
    return resultado
