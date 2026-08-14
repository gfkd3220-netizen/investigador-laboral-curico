import json
import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote


ARCHIVO = "historial.json"

BUSQUEDAS = [
    "automatizacion industrial",
    "mantenimiento industrial",
    "tecnico electrico",
    "tecnico automatizacion",
    "electromecanico",
    "instrumentacion industrial",
    "PLC",
    "electricidad industrial"
]

PALABRAS_VALIDAS = [
    "automatizacion",
    "automatización",
    "mantenimiento industrial",
    "mantenimiento",
    "tecnico electrico",
    "técnico eléctrico",
    "electrico",
    "eléctrico",
    "electromecanico",
    "electromecánico",
    "instrumentacion",
    "instrumentación",
    "plc",
    "electricidad industrial",
    "control industrial",
    "tableros electricos",
    "tableros eléctricos",
    "variadores",
    "hmi",
    "scada"
]


def cargar_historial():

    try:
        with open(ARCHIVO, "r", encoding="utf-8") as archivo:
            return json.load(archivo)

    except FileNotFoundError:

        return {
            "ultima_actualizacion": "",
            "ofertas": []
        }


def guardar_historial(historial):

    with open(
        ARCHIVO,
        "w",
        encoding="utf-8"
    ) as archivo:

        json.dump(
            historial,
            archivo,
            ensure_ascii=False,
            indent=2
        )


def normalizar(texto):

    texto = str(texto).lower()

    reemplazos = {
        "á": "a",
        "é": "e",
        "í": "i",
        "ó": "o",
        "ú": "u",
        "ñ": "n"
    }

    for viejo, nuevo in reemplazos.items():
        texto = texto.replace(viejo, nuevo)

    return texto


def es_de_nuestra_area(titulo, descripcion):

    texto = normalizar(
        titulo + " " + descripcion
    )

    for palabra in PALABRAS_VALIDAS:

        if normalizar(palabra) in texto:
            return True

    return False


def buscar_chiletrabajos(termino):

    url = (
        "https://www.chiletrabajos.cl/"
        "encuentra-un-empleo/"
        "?2=" + quote(termino)
    )

    headers = {
        "User-Agent":
            "Mozilla/5.0"
    }

    respuesta = requests.get(
        url,
        headers=headers,
        timeout=20
    )

    respuesta.raise_for_status()

    soup = BeautifulSoup(
        respuesta.text,
        "html.parser"
    )

    ofertas = []

    for enlace in soup.find_all("a", href=True):

        titulo = enlace.get_text(
            " ",
            strip=True
        )

        href = enlace["href"]

        if "/trabajo/" not in href:
            continue

        if not titulo:
            continue

        if not href.startswith("http"):

            href = (
                "https://www.chiletrabajos.cl"
                + href
            )

        ofertas.append({
            "titulo": titulo,
            "url": href
        })

    return ofertas


def obtener_detalle(oferta):

    headers = {
        "User-Agent":
            "Mozilla/5.0"
    }

    try:

        respuesta = requests.get(
            oferta["url"],
            headers=headers,
            timeout=20
        )

        respuesta.raise_for_status()

    except Exception:

        return None

    soup = BeautifulSoup(
        respuesta.text,
        "html.parser"
    )

    texto = soup.get_text(
        " ",
        strip=True
    )

    titulo = oferta["titulo"]

    if not es_de_nuestra_area(
        titulo,
        texto
    ):

        return None

    return {
        "titulo": titulo,
        "empresa": "",
        "ubicacion": "",
        "descripcion": texto,
        "requisitos": "",
        "url": oferta["url"],
        "fuente": "Chiletrabajos"
    }


def existe_oferta(historial, url):

    for oferta in historial["ofertas"]:

        if oferta.get("url") == url:
            return True

    return False


def ejecutar():

    historial = cargar_historial()

    nuevas = 0

    encontradas = 0

    for termino in BUSQUEDAS:

        print()
        print(
            "Buscando:",
            termino
        )

        try:

            resultados = buscar_chiletrabajos(
                termino
            )

        except Exception as error:

            print(
                "Error:",
                error
            )

            continue

        for resultado in resultados:

            encontradas += 1

            if existe_oferta(
                historial,
                resultado["url"]
            ):
                continue

            detalle = obtener_detalle(
                resultado
            )

            if detalle is None:
                continue

            historial["ofertas"].append(
                detalle
            )

            nuevas += 1

            print(
                "  +",
                detalle["titulo"]
            )

    historial[
        "ultima_actualizacion"
    ] = "actualizado automáticamente"

    guardar_historial(
        historial
    )

    print()
    print("==============================")
    print("RECOLECTOR")
    print("==============================")
    print(
        "Resultados encontrados:",
        encontradas
    )
    print(
        "Ofertas nuevas:",
        nuevas
    )
    print(
        "Total guardadas:",
        len(historial["ofertas"])
    )


if __name__ == "__main__":
    ejecutar()
