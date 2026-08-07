from concurrent.futures import ThreadPoolExecutor, as_completed

from services.engines import duckduckgo, google, bing, brave, yandex, startpage, mojeek

MOTORES = {
    "duckduckgo": duckduckgo,
    "google": google,
    "bing": bing,
    "brave": brave,
    "yandex": yandex,
    "startpage": startpage,
    "mojeek": mojeek,
}


def motores_disponibles():
    return [
        {"id": key, "nombre": mod.NOMBRE, "icono": mod.ICONO} for key, mod in MOTORES.items()
    ]


def realizar_busqueda(consulta, motores=None, limite=None):
    """Ejecuta la consulta en los motores solicitados en paralelo.

    motores: lista de ids ('duckduckgo', 'google', ...). Si es None, usa todos.
    """
    if not motores:
        motores = list(MOTORES.keys())
    motores = [m for m in motores if m in MOTORES]

    salida = []
    with ThreadPoolExecutor(max_workers=max(len(motores), 1)) as ex:
        futuros = {ex.submit(MOTORES[m].buscar, consulta, limite): m for m in motores}
        for fut in as_completed(futuros):
            try:
                salida.append(fut.result())
            except Exception as e:
                salida.append(
                    {"motor": futuros[fut], "ok": False, "error": str(e), "resultados": []}
                )

    orden = {m: i for i, m in enumerate(motores)}
    nombre_a_id = {MOTORES[m].NOMBRE: m for m in motores}
    salida.sort(key=lambda r: orden.get(nombre_a_id.get(r["motor"], ""), 99))
    return salida
