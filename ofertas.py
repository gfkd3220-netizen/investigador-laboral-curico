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
# PALABRAS FUERTES
#
# Si aparecen en el TÍTULO, consideramos que la oferta
# probablemente pertenece a nuestra área.
# ============================================================

PALABRAS_FUERTES = [
    "automatizacion industrial",
    "mantenimiento industrial",
    "tecnico electrico",
    "tecnico automatizacion",
    "electromecanico",
    "instrumentacion industrial",
    "electricidad industrial",
    "control industrial",
    "ingeniero automatizacion",
    "ingeniero control",
    "tecnico mantenimiento",
    "tecnico electromecanico",
    "tecnico instrumentacion",
    "electricista industrial"
]


# ============================================================
# PALABRAS TÉCNICAS
#
# Se usan para comprobar que una oferta realmente tenga
# relación con electricidad, automatización o mantenimiento.
# ============================================================

PALABRAS_VALIDAS = [
    "automatizacion",
    "mantenimiento",
    "tecnico electrico",
    "electrico",
    "electromecanico",
    "instrumentacion",
    "plc",
    "electricidad industrial",
    "control industrial",
    "tableros electricos",
    "variadores",
    "hmi",
    "scada",
    "sensores",
    "motores electricos",
    "diagnostico de fallas",
    "mantenimiento preventivo",
    "mantenimiento correctivo",
    "control automatico",
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
# NORMALIZAR TEXTO
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
# COMPROBAR SI LA OFERTA ES DE NUESTRA ÁREA
# ============================================================

def es_de_nuestra_area(
    titulo,
    descripcion
):

    titulo_normalizado = normalizar(
        titulo
    )

    texto = normalizar(
        titulo + " " + descripcion
    )

    # --------------------------------------------------------
    # 1. Coincidencia fuerte en el título
    # --------------------------------------------------------

    for palabra in PALABRAS_FUERTES:

        if normalizar(palabra) in titulo_normalizado:

            return True


    # --------------------------------------------------------
    # 2. Si el título no es claramente técnico,
    #    exigimos al menos 2 elementos relacionados
    # --------------------------------------------------------

    coincidencias = 0

    for palabra in PALABRAS_VALIDAS:

        if normalizar(palabra) in texto:

            coincidencias += 1

    return coincidencias >= 2


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

        ofertas.append({
            "titulo": titulo,
            "url": href
        })

    return ofertas


# ============================================================
# OBTENER DETALLE DE LA OFERTA
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
            "  Error obteniendo detalle:",
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
    # Comprobar nuevamente que la oferta sea relevante.
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
# COMPROBAR SI YA EXISTE
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
# EJECUTAR RECOLECTOR
# ============================================================

def ejecutar():

    historial = cargar_historial()

    nuevas = 0

    encontradas = 0

    descartadas = 0


    # --------------------------------------------------------
    # Buscar cada término
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
        # Procesar resultados
        # ----------------------------------------------------

        for resultado in resultados:

            encontradas += 1


            # -----------------------------------------------
            # Evitar duplicados
            # -----------------------------------------------

            if existe_oferta(
                historial,
                resultado["url"]
            ):

                continue


            # -----------------------------------------------
            # Obtener contenido real
            # -----------------------------------------------

            detalle = obtener_detalle(
                resultado
            )


            if detalle is None:

                descartadas += 1

                continue


            # -----------------------------------------------
            # Guardar oferta
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
    # ACTUALIZAR HISTORIAL
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
        "Ofertas nuevas:",
        nuevas
    )

    print(
        "Ofertas descartadas:",
        descartadas
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
