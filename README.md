<div align="center">

# 🔎 OSINT Search Pro

### Plataforma OSINT de código abierto para búsquedas inteligentes y recolección de información pública.

![Python](https://img.shields.io/badge/Python-3.13-blue?style=for-the-badge&logo=python)
![Flask](https://img.shields.io/badge/Flask-3.x-black?style=for-the-badge&logo=flask)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-En%20Desarrollo-orange?style=for-the-badge)
![GitHub stars](https://img.shields.io/github/stars/alvaroberrio23242-eng/OSINT_Search_Pro?style=for-the-badge)
![GitHub forks](https://img.shields.io/github/forks/alvaroberrio23242-eng/OSINT_Search_Pro?style=for-the-badge)

---

### 🚀 Proyecto desarrollado con Python + Flask para facilitar investigaciones OSINT mediante múltiples motores de búsqueda y herramientas de inteligencia de fuentes abiertas.

</div>

---

# 📖 Descripción

**OSINT Search Pro** es una plataforma diseñada para investigadores, analistas de ciberseguridad, periodistas y profesionales de inteligencia que necesitan recopilar información pública desde diferentes fuentes de Internet.

Actualmente integra un buscador basado en **DuckDuckGo**, pero su objetivo es convertirse en una plataforma completa con múltiples módulos OSINT.

---

# ✨ Características actuales

- 🔍 Búsqueda mediante DuckDuckGo
- ⚡ Interfaz web desarrollada con Flask
- 🌙 Diseño oscuro
- 📄 Resultados organizados
- 🔗 Acceso directo a los enlaces encontrados
- 💻 Código modular

---

# 🚧 Próximas funciones

## Motores de búsqueda

- ✅ DuckDuckGo
- ⏳ Bing
- ⏳ Brave Search
- ⏳ Google Dorks
- ⏳ Yahoo
- ⏳ Startpage

---

## Herramientas OSINT

- 🌍 WHOIS
- 🌐 DNS Lookup
- 📡 Geolocalización IP
- 📧 Email Intelligence
- 📱 Redes Sociales
- 🛰 Shodan
- 🦠 VirusTotal
- 🔐 Hash Lookup
- 📂 Metadata Extraction

---

## Exportación

- 📄 PDF
- 📊 Excel
- 📁 CSV
- 📦 JSON

---

# 🖥 Capturas

## Página principal

```
(Agregar captura aquí)

docs/screenshot-home.png
```

---

## Resultados

```
(Agregar captura aquí)

docs/screenshot-results.png
```

---

# 📂 Estructura del proyecto

```
OSINT_Search_Pro
│
├── app.py
├── README.md
├── requirements.txt
├── .gitignore
│
├── buscadores/
│   ├── __init__.py
│   └── duckduckgo.py
│
├── templates/
│   ├── index.html
│   └── resultados.html
│
├── static/
│   ├── css/
│   ├── js/
│   └── img/
│
├── exportadores/
│
├── database/
│
└── resultados/
```

---

# ⚙ Instalación

## Clonar el repositorio

```bash
git clone https://github.com/alvaroberrio23242-eng/OSINT_Search_Pro.git
```

Entrar al proyecto

```bash
cd OSINT_Search_Pro
```

Crear entorno virtual

Windows

```bash
python -m venv .venv
```

Activar entorno

PowerShell

```powershell
.venv\Scripts\Activate.ps1
```

Git Bash

```bash
source .venv/Scripts/activate
```

Instalar dependencias

```bash
pip install -r requirements.txt
```

Ejecutar

```bash
python app.py
```

Abrir

```
http://127.0.0.1:5000
```

---

# 🛠 Tecnologías

- Python 3
- Flask
- HTML5
- CSS3
- JavaScript
- DuckDuckGo Search API (ddgs)

---

# 📌 Roadmap

## Versión 1.0

- [x] Buscador DuckDuckGo
- [x] Interfaz Flask
- [x] Resultados web

## Versión 2.0

- [ ] Bing
- [ ] Brave
- [ ] Google Dorks
- [ ] Exportar PDF
- [ ] Exportar Excel

## Versión 3.0

- [ ] WHOIS
- [ ] DNS
- [ ] GeoIP
- [ ] VirusTotal
- [ ] Shodan

## Versión 4.0

- [ ] Dashboard
- [ ] Estadísticas
- [ ] API REST
- [ ] Sistema de usuarios

---

# 🤝 Contribuciones

Las contribuciones son bienvenidas.

Si deseas mejorar el proyecto:

1. Haz un Fork.
2. Crea una nueva rama.

```bash
git checkout -b nueva-funcion
```

3. Haz Commit.

```bash
git commit -m "Nueva funcionalidad"
```

4. Envía un Pull Request.

---

# 📜 Licencia

Este proyecto está distribuido bajo la licencia MIT.

Consulta el archivo **LICENSE** para más información.

---

# 👨‍💻 Autor

## Álvaro Berrío

Desarrollador de software e investigador interesado en herramientas OSINT, automatización y ciberseguridad.

GitHub

https://github.com/alvaroberrio23242-eng

---

<div align="center">

## ⭐ Si este proyecto te resulta útil, considera darle una estrella en GitHub.

</div>
