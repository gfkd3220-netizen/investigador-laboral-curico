import json

ARCHIVO_HISTORIAL = "historial.json"


def oferta_ya_existe(ofertas, nueva_oferta):

    for oferta in ofertas:

        mismo_titulo = (
            oferta.get("titulo", "").strip().lower()
            == nueva_oferta.get("titulo", "").strip().lower()
        )

        misma_empresa = (
            oferta.get("empresa", "").strip().lower()
            == nueva_oferta.get("empresa", "").strip().lower()
        )

        misma_ubicacion = (
            oferta.get("ubicacion", "").strip().lower()
            == nueva_oferta.get("ubicacion", "").strip().lower()
        )

        if mismo_titulo and misma_empresa and misma_ubicacion:
            return True

    return False


def agregar_oferta(oferta):

    with open(ARCHIVO_HISTORIAL, "r", encoding="utf-8") as archivo:
        historial = json.load(archivo)

    historial.setdefault("ofertas", [])

    ofertas = historial["ofertas"]

    if oferta_ya_existe(ofertas, oferta):

        print("La oferta ya existe. No se agregó nuevamente.")
        return

    ofertas.append(oferta)

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
