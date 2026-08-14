import json

ARCHIVO_HISTORIAL = "historial.json"


def agregar_oferta(oferta):

    with open(ARCHIVO_HISTORIAL, "r", encoding="utf-8") as archivo:
        historial = json.load(archivo)

    historial.setdefault("ofertas", [])

    historial["ofertas"].append(oferta)

    with open(ARCHIVO_HISTORIAL, "w", encoding="utf-8") as archivo:
        json.dump(
            historial,
            archivo,
            ensure_ascii=False,
            indent=2
        )

    print("Oferta agregada correctamente.")


if __name__ == "__main__":

    oferta = {
        "titulo": "Técnico Eléctrico Industrial",
        "empresa": "Empresa de Prueba 2",
        "ubicacion": "Curicó",
        "descripcion": "Mantenimiento industrial, electricidad y tableros eléctricos.",
        "requisitos": "Experiencia de 1 año. Conocimientos de PLC y mantenimiento preventivo."
    }

    agregar_oferta(oferta)
