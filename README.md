# 🛰️ OSINT Search Pro

**Plataforma de Inteligencia de Fuentes Abiertas (OSINT)** construida con Flask. Un único cuadro de búsqueda con detección automática de tipo, agregación de motores gratuitos y módulos especializados de reconocimiento — todo con datos ya públicos.

![status](https://img.shields.io/badge/status-active-37d67a)
![python](https://img.shields.io/badge/python-3.11%2B-3776AB)
![flask](https://img.shields.io/badge/flask-3.x-black)
![license](https://img.shields.io/badge/license-MIT-blue)

---

## ✨ Características

### 🔍 Búsqueda inteligente
Escribe cualquier cosa — un nombre, un email, un dominio, una IP, un hash, un usuario o un teléfono — y la plataforma **detecta automáticamente el tipo** y sugiere el módulo correcto.

### 🌐 Agregador multi-motor (sin API keys)
- DuckDuckGo · Google · Bing · Brave Search · Yandex · Startpage · Mojeek
- Ejecución **en paralelo** (ThreadPoolExecutor), con manejo de errores por motor.

### 🧩 Módulos especializados
| Módulo | Qué hace |
|---|---|
| **Personas** | Comprueba en tiempo real si un nombre de usuario existe en GitHub, Reddit, X, Instagram, TikTok, Facebook, Pinterest, Steam, Twitch y YouTube. |
| **Emails** | MX, registros DNS del dominio, Gravatar y búsqueda cruzada de usuarios en GitHub. |
| **Dominios** | WHOIS, registros DNS completos y subdominios vía Certificate Transparency (crt.sh). |
| **Direcciones IP** | Geolocalización (país, ciudad, ISP, ASN), reverse DNS y verificación de 12 puertos comunes. |
| **Google Dorks** | Generador automático de operadores (`site:`, `filetype:`, `intitle:`, `inurl:`, `cache:`, `related:`...) y combinaciones predefinidas. |
| **Herramientas** | Base64, generador/identificador de hashes, decodificador de URL, generador de QR, generador de contraseñas, DNS lookup, visor de robots.txt y de cabeceras HTTP. |

### 📊 Estadísticas reales
Contadores de búsquedas, tipos de consulta y motores usados — calculados a partir del uso real guardado en `localStorage`, no simulados.

### 🕘 Historial y favoritos
Guardado en el navegador (localStorage) con filtro de búsqueda y posibilidad de marcar consultas como favoritas.

### 🎛️ Diseño "Recon Console"
Interfaz oscura con sidebar persistente, paneles con esquinas tipo retícula, radar animado y fondo de partículas — pensada para transmitir la estética de una consola de reconocimiento, no una plantilla genérica.

---

## 🖥️ Capturas

> Añade aquí tus propias capturas de pantalla tras desplegar la app (`/`, `/personas`, `/dominios`, `/ips`, `/herramientas`).

---

## 🏗️ Arquitectura

```
OSINT_Search_Pro/
├── app.py                     # Punto de entrada Flask
├── config.py                  # Configuración y feature flags
├── controllers/
│   ├── main_controller.py     # Rutas de páginas (HTML)
│   └── api_controller.py      # Rutas de API (JSON)
├── services/
│   ├── detector.py            # Detección automática de tipo de consulta
│   ├── dorks.py                # Generador de Google Dorks
│   ├── email_intel.py         # MX / DNS / Gravatar / GitHub
│   ├── domain_intel.py        # WHOIS / DNS / subdominios (crt.sh)
│   ├── ip_intel.py            # Geolocalización / puertos comunes
│   ├── username_intel.py      # Verificación multi-plataforma
│   ├── tools_service.py       # Herramientas auxiliares
│   ├── search_service.py      # Orquestador de motores en paralelo
│   └── engines/                # Un módulo por motor de búsqueda
├── static/
│   ├── css/                   # main / components / dashboard / animations
│   └── js/
│       ├── api.js storage.js render.js app.js particles.js
│       └── pages/              # Un script por página
└── templates/                 # Jinja2 (layout + una plantilla por módulo)
```

Patrón **MVC ligero**: `controllers` (rutas) → `services` (lógica de negocio y llamadas externas) → `templates`/`static` (presentación). El frontend es JS vanilla (sin build step) que consume la API JSON interna.

---

## 🚀 Instalación

```bash
git clone https://github.com/tu-usuario/OSINT_Search_Pro.git
cd OSINT_Search_Pro
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env               # opcional
python app.py
```

Abre `http://localhost:5000`.

### Despliegue (Heroku / Render / Railway)
El proyecto ya incluye `Procfile` (`web: gunicorn app:app`). Solo conecta el repositorio y despliega.

---

## 🔑 Integraciones opcionales

Shodan, Censys, VirusTotal, HaveIBeenPwned, Hunter.io y SecurityTrails **no están activadas por defecto** (requieren claves de pago/registro). El código ya prevé sus variables de entorno en `config.py` para quien quiera extender la plataforma; sin ellas, el resto de módulos funciona con normalidad usando fuentes 100% gratuitas.

---

## 📡 API interna

Todas las rutas devuelven JSON y aceptan `POST` con cuerpo `application/json`.

| Endpoint | Descripción |
|---|---|
| `POST /api/detect` | Detecta el tipo de una consulta |
| `POST /api/search` | Búsqueda multi-motor |
| `POST /api/dorks` | Genera Google Dorks |
| `POST /api/lookup/email` | Análisis de email |
| `POST /api/lookup/domain` | Análisis de dominio |
| `POST /api/lookup/ip` | Análisis de IP |
| `POST /api/lookup/username` | Verificación de usuario |
| `POST /api/tools/*` | Base64, hash, url, password, dns, robots, headers, qr |

---

## ⚠️ Uso responsable

OSINT Search Pro consulta exclusivamente **información ya pública** (motores de búsqueda, WHOIS, DNS, certificados TLS públicos, perfiles públicos). El escaneo de puertos incluido es un chequeo diagnóstico ligero (12 puertos, timeout corto) pensado para **activos propios o con autorización expresa**. El scraping de motores de búsqueda depende de su HTML público y puede romperse si esos sitios cambian su estructura; úsalo respetando los términos de servicio de cada proveedor.

Este proyecto es un ejercicio educativo / de portfolio. No está afiliado a ninguno de los motores o plataformas que consulta.

---

## 📄 Licencia

MIT — libre para usar, modificar y distribuir.
