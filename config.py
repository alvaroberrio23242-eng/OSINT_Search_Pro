import os
import secrets


class Config:
    """Configuración central de OSINT Search Pro.

    Todas las claves de API son opcionales. Si no están presentes,
    las funciones que dependen de ellas se desactivan automáticamente
    y el resto de la plataforma sigue funcionando con fuentes gratuitas.
    """

    SECRET_KEY = os.environ.get("SECRET_KEY")
    if not SECRET_KEY:
        if os.environ.get("OSP_DEV") == "1":
            SECRET_KEY = secrets.token_hex(32)  # solo desarrollo local: clave efimera
        else:
            raise RuntimeError("SECRET_KEY no configurada. Definela como variable de entorno (OSP_DEV=1 solo en local).")

    # Timeouts / límites usados por los servicios de red
    HTTP_TIMEOUT = float(os.environ.get("OSP_HTTP_TIMEOUT", 6))
    MAX_RESULTS_PER_ENGINE = int(os.environ.get("OSP_MAX_RESULTS", 8))

    # Segundos que se guarda una búsqueda en caché antes de repetirla contra los motores
    SEARCH_CACHE_TTL = int(os.environ.get("OSP_CACHE_TTL", 3600))

    # Puertos comunes para el escáner básico (solo diagnóstico, no intrusivo)
    COMMON_PORTS = [21, 22, 23, 25, 53, 80, 110, 143, 443, 3306, 3389, 8080]
    PORT_SCAN_TIMEOUT = float(os.environ.get("OSP_PORT_TIMEOUT", 0.6))

    # User-Agent usado en las peticiones salientes
    USER_AGENT = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0 Safari/537.36 OSINTSearchPro/2.0"
    )

    # Clave gratuita de Brave Search API (https://api.search.brave.com/register).
    # Si está presente, el motor "Brave Search" usa la API oficial (resultados
    # reales, no bloqueados por IPs de hosting) en vez de scraping HTML.
    BRAVE_API_KEY = os.environ.get("BRAVE_API_KEY", "")

    # Google Custom Search JSON API (https://programmablesearchengine.google.com/
    # + https://console.cloud.google.com/apis/credentials). Gratis hasta
    # 100 consultas/día. Se necesitan las dos variables para activarse.
    GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY", "")
    GOOGLE_CSE_ID = os.environ.get("GOOGLE_CSE_ID", "")

    # Claves opcionales de servicios de pago (no requeridas para funcionar)
    HUNTER_API_KEY = os.environ.get("HUNTER_API_KEY", "")
    SHODAN_API_KEY = os.environ.get("SHODAN_API_KEY", "")
    VIRUSTOTAL_API_KEY = os.environ.get("VIRUSTOTAL_API_KEY", "")
    HIBP_API_KEY = os.environ.get("HIBP_API_KEY", "")
    CENSYS_API_ID = os.environ.get("CENSYS_API_ID", "")
    CENSYS_API_SECRET = os.environ.get("CENSYS_API_SECRET", "")
    SECURITYTRAILS_API_KEY = os.environ.get("SECURITYTRAILS_API_KEY", "")

    @classmethod
    def optional_services_status(cls):
        return {
            "brave_search_api": bool(cls.BRAVE_API_KEY),
            "google_custom_search": bool(cls.GOOGLE_API_KEY and cls.GOOGLE_CSE_ID),
            "hunter": bool(cls.HUNTER_API_KEY),
            "shodan": bool(cls.SHODAN_API_KEY),
            "virustotal": bool(cls.VIRUSTOTAL_API_KEY),
            "hibp": bool(cls.HIBP_API_KEY),
            "censys": bool(cls.CENSYS_API_ID and cls.CENSYS_API_SECRET),
            "securitytrails": bool(cls.SECURITYTRAILS_API_KEY),
        }
