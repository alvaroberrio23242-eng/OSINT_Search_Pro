"""
Generación de contenido pedagógico original sobre cultura salsera.
Todo el texto es propio (plantillas + variación aleatoria), no se
reproduce material de terceros.
"""
import random

# ---------------------------------------------------------------------------
# Bloques de contenido temático, por enfoque
# ---------------------------------------------------------------------------

TEMAS = {
    "cultura": [
        {
            "titulo": "Medellín y la salsa: una relación centenaria",
            "texto": (
                "Desde mediados del siglo XX, Medellín se convirtió en uno de los "
                "epicentros de la salsa en América Latina, al punto de ganarse el "
                "apodo de 'Capital Mundial de la Salsa'. La ciudad combina una "
                "tradición de baile popular en barrios como Manrique y el centro "
                "histórico, con una industria discográfica y radial que en los años "
                "70 y 80 impulsó a orquestas locales e internacionales por igual."
            ),
        },
        {
            "titulo": "Barrios, esquinas y salsotecas",
            "texto": (
                "La salsa en Medellín no vive solo en tarima: se transmite en "
                "esquinas, tiendas de barrio y 'salsotecas' —locales dedicados por "
                "completo a coleccionar y reproducir vinilos de salsa— donde varias "
                "generaciones de melómanos han construido una memoria musical "
                "colectiva que hoy es parte del patrimonio cultural de la ciudad."
            ),
        },
        {
            "titulo": "El Festival de Orquestas y otros hitos",
            "texto": (
                "Eventos como el Festival de Orquestas de Medellín, celebrado cada "
                "diciembre, reúnen agrupaciones locales e internacionales, y son "
                "una buena puerta de entrada para que los estudiantes conecten la "
                "teoría del aula con la práctica viva de la ciudad."
            ),
        },
    ],
    "instrumentos": [
        {
            "titulo": "La clave: el corazón rítmico",
            "texto": (
                "La clave es el patrón rítmico base sobre el que se organiza casi "
                "toda la música salsera. Tradicionalmente se toca con dos palos de "
                "madera del mismo nombre, y su función es servir de 'columna "
                "vertebral' para que el resto de los instrumentos se sincronicen."
            ),
        },
        {
            "titulo": "Percusión: congas, bongós y timbales",
            "texto": (
                "Cada tambor cumple un rol distinto: las congas aportan la base "
                "grave y continua, los bongós añaden adornos melódicos de alta "
                "frecuencia, y los timbales marcan los cambios de sección y los "
                "acentos que anuncian coros o solos."
            ),
        },
        {
            "titulo": "Instrumentos melódicos y de viento",
            "texto": (
                "El piano y el bajo tejen el 'montuno' —un patrón armónico "
                "repetitivo— mientras que trompetas y trombones aportan los "
                "'mambos' o pasajes instrumentales que dialogan con la voz "
                "principal y el coro."
            ),
        },
    ],
}

OBJETIVOS_BASE = [
    "Reconocer la salsa como una manifestación cultural con raíces históricas y sociales concretas.",
    "Identificar los principales instrumentos de la música salsera y su función dentro del conjunto.",
    "Relacionar la música con el contexto urbano de Medellín y su identidad como ciudad.",
    "Fomentar la escucha activa y el respeto por las tradiciones musicales populares.",
]

ACTIVIDADES = [
    "Escucha guiada: identificar en una grabación qué instrumento entra en cada momento.",
    "Cartografía sonora: ubicar en un mapa de Medellín los lugares mencionados en la guía.",
    "Rueda de preguntas: aplicar la trivia incluida en este paquete como cierre de la sesión.",
    "Círculo de clave: practicar el patrón rítmico de la clave con palmas, en grupo.",
    "Línea de tiempo colectiva: construir en cartelera los hitos históricos vistos en clase.",
]


def _temas_para_enfoque(enfoque):
    if enfoque == "cultura":
        return TEMAS["cultura"]
    if enfoque == "instrumentos":
        return TEMAS["instrumentos"]
    # ambos
    return TEMAS["cultura"] + TEMAS["instrumentos"]


def generar_guia(enfoque="ambos", nivel=""):
    temas = _temas_para_enfoque(enfoque)
    random.shuffle(temas)
    actividades = random.sample(ACTIVIDADES, k=min(3, len(ACTIVIDADES)))

    nivel_txt = nivel.strip() if nivel else "educación básica y media"

    guia = {
        "titulo": "Unidad pedagógica: cultura salsera de Medellín",
        "nivel": nivel_txt,
        "introduccion": (
            "Esta unidad ofrece un punto de partida para llevar al aula la "
            "cultura salsera de Medellín, combinando contexto histórico y "
            "nociones básicas de los instrumentos que la conforman. Está "
            "pensada como material flexible: el docente puede tomar solo "
            "algunos bloques según el tiempo disponible."
        ),
        "objetivos": OBJETIVOS_BASE,
        "temas": temas,
        "actividades": actividades,
    }
    return guia


def render_guia_markdown(guia):
    lineas = [f"# {guia['titulo']}", "", f"**Nivel sugerido:** {guia['nivel']}", ""]
    lineas.append("## Introducción")
    lineas.append(guia["introduccion"])
    lineas.append("")
    lineas.append("## Objetivos de aprendizaje")
    for obj in guia["objetivos"]:
        lineas.append(f"- {obj}")
    lineas.append("")
    lineas.append("## Contenido temático")
    for tema in guia["temas"]:
        lineas.append(f"### {tema['titulo']}")
        lineas.append(tema["texto"])
        lineas.append("")
    lineas.append("## Actividades sugeridas")
    for act in guia["actividades"]:
        lineas.append(f"- {act}")
    lineas.append("")
    return "\n".join(lineas)


# ---------------------------------------------------------------------------
# Trivia
# ---------------------------------------------------------------------------

BANCO_TRIVIA = {
    "cultura": [
        {
            "pregunta": "¿Con qué apodo se conoce popularmente a Medellín en relación con la salsa?",
            "opciones": ["Capital Mundial de la Salsa", "Ciudad del Vinilo", "Cuna del Mambo", "Distrito Sonoro"],
            "correcta": 0,
        },
        {
            "pregunta": "¿Qué es una 'salsoteca'?",
            "opciones": [
                "Un tipo de tambor",
                "Un local dedicado a coleccionar y reproducir vinilos de salsa",
                "Una academia de baile exclusiva",
                "Un festival anual",
            ],
            "correcta": 1,
        },
        {
            "pregunta": "¿En qué mes se celebra tradicionalmente el Festival de Orquestas de Medellín?",
            "opciones": ["Marzo", "Julio", "Diciembre", "Octubre"],
            "correcta": 2,
        },
        {
            "pregunta": "La memoria musical de la salsa en Medellín se transmite principalmente en:",
            "opciones": [
                "Solo en teatros formales",
                "Barrios, esquinas y salsotecas",
                "Únicamente en la radio",
                "Museos especializados",
            ],
            "correcta": 1,
        },
    ],
    "instrumentos": [
        {
            "pregunta": "¿Qué instrumento suele considerarse la 'columna vertebral' rítmica de la salsa?",
            "opciones": ["El piano", "La clave", "El trombón", "El bajo"],
            "correcta": 1,
        },
        {
            "pregunta": "¿Qué tambor aporta la base grave y continua en la percusión salsera?",
            "opciones": ["El bongó", "El timbal", "La conga", "La campana"],
            "correcta": 2,
        },
        {
            "pregunta": "¿Qué instrumentos suelen marcar los cambios de sección y acentos?",
            "opciones": ["Los timbales", "El piano", "La flauta", "El bajo"],
            "correcta": 0,
        },
        {
            "pregunta": "El patrón armónico repetitivo que tejen el piano y el bajo se conoce como:",
            "opciones": ["Mambo", "Montuno", "Clave", "Guajeo cruzado"],
            "correcta": 1,
        },
    ],
}


def generar_trivia(enfoque="ambos", cantidad=8):
    if enfoque == "cultura":
        banco = list(BANCO_TRIVIA["cultura"])
    elif enfoque == "instrumentos":
        banco = list(BANCO_TRIVIA["instrumentos"])
    else:
        banco = list(BANCO_TRIVIA["cultura"]) + list(BANCO_TRIVIA["instrumentos"])

    random.shuffle(banco)
    return banco[: min(cantidad, len(banco))]


def render_trivia_markdown(preguntas):
    lineas = ["# Trivia: cultura salsera de Medellín", ""]
    letras = ["A", "B", "C", "D"]
    for i, p in enumerate(preguntas, start=1):
        lineas.append(f"**{i}. {p['pregunta']}**")
        for j, opcion in enumerate(p["opciones"]):
            lineas.append(f"   {letras[j]}) {opcion}")
        lineas.append("")
    lineas.append("---")
    lineas.append("## Respuestas correctas")
    for i, p in enumerate(preguntas, start=1):
        lineas.append(f"{i}. {letras[p['correcta']]}")
    return "\n".join(lineas)
