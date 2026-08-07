"""Generador de Google Dorks a partir de una consulta base."""

DORK_TEMPLATES = [
    {"op": "site:", "ejemplo": "site:{q}", "descripcion": "Limita resultados a un dominio o sitio concreto."},
    {"op": "filetype:", "ejemplo": "{q} filetype:pdf", "descripcion": "Busca archivos de un tipo específico (pdf, docx, xlsx, sql...)."},
    {"op": "intitle:", "ejemplo": "intitle:{q}", "descripcion": "Busca páginas cuyo título contenga el término."},
    {"op": "inurl:", "ejemplo": "inurl:{q}", "descripcion": "Busca páginas cuya URL contenga el término."},
    {"op": "cache:", "ejemplo": "cache:{q}", "descripcion": "Muestra la última versión indexada por Google de una URL."},
    {"op": "related:", "ejemplo": "related:{q}", "descripcion": "Encuentra sitios relacionados/similares a una URL."},
    {"op": "intext:", "ejemplo": "intext:{q}", "descripcion": "Busca el término dentro del cuerpo de texto de la página."},
    {"op": "link:", "ejemplo": "link:{q}", "descripcion": "Busca páginas que enlazan a una URL (soporte limitado en motores actuales)."},
    {"op": "ext:", "ejemplo": "{q} ext:log", "descripcion": "Alias corto de filetype:, útil para logs y configuraciones."},
    {"op": "\"frase exacta\"", "ejemplo": "\"{q}\"", "descripcion": "Busca la coincidencia exacta de la frase."},
]

DORK_PRESETS = [
    {
        "nombre": "Documentos expuestos",
        "query": '{q} filetype:pdf OR filetype:doc OR filetype:xls',
    },
    {
        "nombre": "Paneles de login",
        "query": 'site:{q} inurl:login OR inurl:admin',
    },
    {
        "nombre": "Archivos de configuración",
        "query": 'site:{q} ext:env OR ext:log OR ext:conf',
    },
    {
        "nombre": "Directorios listados",
        "query": 'site:{q} intitle:"index of"',
    },
    {
        "nombre": "Perfiles en redes",
        "query": '"{q}" (site:linkedin.com OR site:twitter.com OR site:facebook.com)',
    },
]


def generar_dorks(consulta: str) -> dict:
    q = consulta.strip() or "ejemplo.com"
    operadores = [
        {**t, "query": t["ejemplo"].format(q=q)} for t in DORK_TEMPLATES
    ]
    presets = [{**p, "query": p["query"].format(q=q)} for p in DORK_PRESETS]
    return {"operadores": operadores, "presets": presets, "base": q}
