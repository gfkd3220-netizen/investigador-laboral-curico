import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote


ARCHIVO = "historial.json"


# ============================================================
# BÚSQUEDAS
# ============================================================

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


# ============================================================
# PALABRAS QUE IDENTIFICAN EL CARGO
#
# Estas palabras deben aparecer en el título para considerar
# que el cargo pertenece claramente a nuestra área.
# ============================================================

PALABRAS_TITULO = [
    "automatizacion",
    "mantenimiento industrial",
    "tecnico electrico",
    "tecnico automatizacion",
    "tecnico de mantenimiento",
    "tecnico electromecanico",
    "tecnico instrumentacion",
    "electromecanico",
    "instrumentacion industrial",
    "electricista industrial",
    "electricidad industrial",
    "control industrial",
    "tablerista industrial",
    "planner de mantenimiento",
    "mantenimiento",
    "electrico industrial"
]


# ============================================================
# CONOCIMIENTOS DEL ÁREA
#
# Se utilizan para comprobar que el contenido de la oferta
# realmente tenga relación con el área técnica.
# ============================================================

PALABRAS_TECNICAS = [
    "automatizacion",
    "mantenimiento industrial",
    "mantenimiento preventivo",
    "mantenimiento correctivo",
    "diagnostico de fallas",
    "electricidad industrial",
    "electrico",
    "electromecanico",
    "instrumentacion",
    "plc",
    "control industrial",
    "control automatico",
    "tableros electricos",
    "variadores",
    "hmi",
    "scada",
    "sensores",
    "motores electricos",
    "lectura de planos",
    "puesta en marcha",
    "neumatica",
    "hidraulica"
]


# ============================================================
# CARGAR HISTORIAL
# ============================================================

def cargar_historial():

    try:

        with open(
            ARCHIVO,
            "r",
            encoding="utf-8"
        ) as archivo:

            historial = json.load(archivo)

    except FileNotFoundError:

        historial = {
            "ultima_actualizacion": "",
            "ofertas": []
        }

    if "ofertas" not in historial:

        historial["ofertas"] = []

    return historial


# ============================================================
# GUARDAR HISTORIAL
# ============================================================

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


# ============================================================
# NORMALIZAR
# ============================================================

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

        texto = texto.replace(
            viejo,
            nuevo
        )

    return texto


# ============================================================
# COMPROBAR TÍTULO
# ============================================================

def titulo_es_relevante(titulo):

    titulo_normalizado = normalizar(
        titulo
    )

    for palabra in PALABRAS_TITULO:

        if normalizar(palabra) in titulo_normalizado:

            return True

    return False


# ============================================================
# COMPROBAR CONTENIDO
# ============================================================

def contenido_es_relevante(
    titulo,
    descripcion
):

    texto = normalizar(
        titulo + " " + descripcion
    )

    coincidencias = 0

    for palabra in PALABRAS_TECNICAS:

        if normalizar(palabra) in texto:

            coincidencias += 1

    # Necesitamos al menos dos elementos técnicos
    # para evitar falsos positivos.

    return coincidencias >= 2


# ============================================================
# COMPROBAR OFERTA COMPLETA
# ============================================================

def es_de_nuestra_area(
    titulo,
    descripcion
):

    # Primero revisamos el título.
    #
    # Esto evita guardar cosas como:
    # "Operario de fábrica"
    # simplemente porque la página contiene
    # la palabra electricidad en alguna parte.

    if not titulo_es_relevante(titulo):

        return False

    # Después comprobamos que el contenido
    # tenga relación técnica real.

    if not contenido_es_relevante(
        titulo,
        descripcion
    ):

        return False

    return True


# ============================================================
# BUSCAR EN CHILETRABAJOS
# ============================================================

def buscar_chiletrabajos(termino):

    url = (
        "https://www.chiletrabajos.cl/"
        "encuentra-un-empleo/"
        "?2=" + quote(termino)
    )

    headers = {
        "User-Agent": (
            "Mozilla/5.0 "
            "(Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 "
            "(KHTML, like Gecko) "
            "Chrome/120.0 Safari/537.36"
        )
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

    urls_vistas = set()

    for enlace in soup.find_all(
        "a",
        href=True
    ):

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

        if href in urls_vistas:

            continue

        urls_vistas.add(href)

        ofertas.append({
            "titulo": titulo,
            "url": href
        })

    return ofertas


# ============================================================
# OBTENER DETALLE
# ============================================================

def obtener_detalle(oferta):

    headers = {
        "User-Agent": (
            "Mozilla/5.0 "
            "(Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 "
            "(KHTML, like Gecko) "
            "Chrome/120.0 Safari/537.36"
        )
    }

    try:

        respuesta = requests.get(
            oferta["url"],
            headers=headers,
            timeout=20
        )

        respuesta.raise_for_status()

    except Exception as error:

        print(
            "  Error obteniendo oferta:",
            error
        )

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


    # --------------------------------------------------------
    # Filtro final
    # --------------------------------------------------------

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


# ============================================================
# COMPROBAR DUPLICADO
# ============================================================

def existe_oferta(
    historial,
    url
):

    for oferta in historial["ofertas"]:

        if oferta.get("url") == url:

            return True

    return False


# ============================================================
# EJECUTAR
# ============================================================

def ejecutar():

    historial = cargar_historial()

    nuevas = 0

    encontradas = 0

    descartadas = 0


    # --------------------------------------------------------
    # BUSCAR
    # --------------------------------------------------------

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


        # ----------------------------------------------------
        # PROCESAR RESULTADOS
        # ----------------------------------------------------

        for resultado in resultados:

            encontradas += 1


            # -----------------------------------------------
            # Primero filtramos por título.
            #
            # Así no descargamos cientos de ofertas
            # claramente irrelevantes.
            # -----------------------------------------------

            if not titulo_es_relevante(
                resultado["titulo"]
            ):

                descartadas += 1

                continue


            # -----------------------------------------------
            # Evitar duplicados
            # -----------------------------------------------

            if existe_oferta(
                historial,
                resultado["url"]
            ):

                continue


            # -----------------------------------------------
            # Descargar detalle
            # -----------------------------------------------

            detalle = obtener_detalle(
                resultado
            )


            if detalle is None:

                descartadas += 1

                continue


            # -----------------------------------------------
            # Guardar
            # -----------------------------------------------

            historial["ofertas"].append(
                detalle
            )

            nuevas += 1

            print(
                "  +",
                detalle["titulo"]
            )


    # ========================================================
    # ACTUALIZAR
    # ========================================================

    historial[
        "ultima_actualizacion"
    ] = "actualizado automáticamente"


    guardar_historial(
        historial
    )


    # ========================================================
    # RESULTADO
    # ========================================================

    print()

    print(
        "=============================="
    )

    print(
        "RECOLECTOR"
    )

    print(
        "=============================="
    )

    print(
        "Resultados encontrados:",
        encontradas
    )

    print(
        "Ofertas descartadas:",
        descartadas
    )

    print(
        "Ofertas nuevas:",
        nuevas
    )

    print(
        "Total guardadas:",
        len(historial["ofertas"])
    )

    print(
        "=============================="
    )


# ============================================================
# EJECUTAR
# ============================================================

if __name__ == "__main__":

    ejecutar()
