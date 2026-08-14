import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote
from datetime import datetime


ARCHIVO = "historial.json"


# ============================================================
# BÚSQUEDAS
#
# Buscamos términos amplios del área.
# No filtramos por junior/senior porque queremos estudiar
# qué pide el mercado completo.
# ============================================================

BUSQUEDAS = [
    "automatizacion industrial",
    "mantenimiento industrial",
    "tecnico electrico",
    "tecnico automatizacion",
    "electromecanico",
    "instrumentacion industrial",
    "PLC",
    "electricidad industrial",
    "control industrial",
    "electricista industrial",
    "mantenimiento electrico"
]


# ============================================================
# TÉRMINOS DEL ÁREA
#
# Se utilizan para evitar guardar ofertas que no tengan
# relación real con electricidad, mantenimiento,
# automatización, control o electromecánica.
# ============================================================

PALABRAS_TITULO = [
    "automatizacion",
    "automatización",
    "mantenimiento industrial",
    "mantenimiento",
    "tecnico electrico",
    "técnico eléctrico",
    "tecnico automatizacion",
    "técnico automatización",
    "tecnico de mantenimiento",
    "técnico de mantenimiento",
    "tecnico electromecanico",
    "técnico electromecánico",
    "electromecanico",
    "electromecánico",
    "instrumentacion",
    "instrumentación",
    "instrumentista",
    "electricista industrial",
    "electricidad industrial",
    "electrico industrial",
    "eléctrico industrial",
    "control industrial",
    "tablerista",
    "planner de mantenimiento",
    "tecnico en electricidad",
    "técnico en electricidad"
]


PALABRAS_TECNICAS = [
    "automatizacion",
    "automatización",
    "mantenimiento industrial",
    "mantenimiento preventivo",
    "mantenimiento correctivo",
    "mantencion industrial",
    "mantención industrial",
    "diagnostico de fallas",
    "diagnóstico de fallas",
    "electricidad industrial",
    "electrico",
    "eléctrico",
    "electromecanico",
    "electromecánico",
    "instrumentacion",
    "instrumentación",
    "plc",
    "control industrial",
    "control automatico",
    "control automático",
    "tableros electricos",
    "tableros eléctricos",
    "variadores",
    "variadores de frecuencia",
    "hmi",
    "scada",
    "sensores",
    "motores electricos",
    "motores eléctricos",
    "lectura de planos",
    "planos electricos",
    "planos eléctricos",
    "puesta en marcha",
    "neumatica",
    "neumática",
    "hidraulica",
    "hidráulica",
    "vfd",
    "contactor",
    "relé",
    "rele",
    "multimetro",
    "multímetro",
    "mediciones electricas",
    "mediciones eléctricas"
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
# COMPROBAR CONTENIDO TÉCNICO
# ============================================================

def contar_terminos_tecnicos(
    titulo,
    descripcion
):

    texto = normalizar(
        titulo + " " + descripcion
    )

    encontrados = set()

    for palabra in PALABRAS_TECNICAS:

        palabra_normalizada = normalizar(
            palabra
        )

        if palabra_normalizada in texto:

            encontrados.add(
                palabra_normalizada
            )

    return len(encontrados)


def contenido_es_relevante(
    titulo,
    descripcion
):

    coincidencias = contar_terminos_tecnicos(
        titulo,
        descripcion
    )

    return coincidencias >= 2


# ============================================================
# FILTRO FINAL
# ============================================================

def es_de_nuestra_area(
    titulo,
    descripcion
):

    # El título debe indicar claramente que el cargo
    # pertenece al área.

    if not titulo_es_relevante(titulo):

        return False

    # Además, el contenido debe tener suficiente
    # vocabulario técnico.

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
# EXTRAER TEXTO LIMPIO
# ============================================================

def limpiar_texto(soup):

    # Eliminamos elementos que no aportan información
    # laboral y contaminan el análisis.

    for elemento in soup([
        "script",
        "style",
        "nav",
        "footer",
        "header",
        "form"
    ]):

        elemento.decompose()

    texto = soup.get_text(
        " ",
        strip=True
    )

    # Evitar espacios repetidos.

    texto = " ".join(
        texto.split()
    )

    return texto


# ============================================================
# INTENTAR EXTRAER EMPRESA
# ============================================================

def extraer_empresa(soup):

    selectores = [
        "[class*='empresa']",
        "[class*='company']",
        "[id*='empresa']",
        "[id*='company']"
    ]

    for selector in selectores:

        elemento = soup.select_one(
            selector
        )

        if elemento:

            texto = elemento.get_text(
                " ",
                strip=True
            )

            if texto and len(texto) < 150:

                return texto

    return ""


# ============================================================
# INTENTAR EXTRAER UBICACIÓN
# ============================================================

def extraer_ubicacion(soup):

    selectores = [
        "[class*='ubicacion']",
        "[class*='location']",
        "[class*='comuna']",
        "[class*='region']",
        "[id*='ubicacion']",
        "[id*='location']"
    ]

    for selector in selectores:

        elemento = soup.select_one(
            selector
        )

        if elemento:

            texto = elemento.get_text(
                " ",
                strip=True
            )

            if texto and len(texto) < 150:

                return texto

    return ""


# ============================================================
# OBTENER DETALLE
# ============================================================

def obtener_detalle(
    oferta,
    termino_busqueda
):

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

    titulo = oferta["titulo"]

    texto = limpiar_texto(
        soup
    )

    # Filtro final.

    if not es_de_nuestra_area(
        titulo,
        texto
    ):

        return None

    empresa = extraer_empresa(
        soup
    )

    ubicacion = extraer_ubicacion(
        soup
    )

    coincidencias_tecnicas = (
        contar_terminos_tecnicos(
            titulo,
            texto
        )
    )

    return {

        "titulo": titulo,

        "empresa": empresa,

        "ubicacion": ubicacion,

        "descripcion": texto,

        "requisitos": "",

        "url": oferta["url"],

        "fuente": "Chiletrabajos",

        "busqueda_origen": termino_busqueda,

        "fecha_recoleccion": (
            datetime.now().isoformat()
        ),

        "terminos_tecnicos_detectados": (
            coincidencias_tecnicas
        )
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

    duplicadas = 0


    # ========================================================
    # BUSCAR
    # ========================================================

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


        # ====================================================
        # PROCESAR RESULTADOS
        # ====================================================

        for resultado in resultados:

            encontradas += 1

            # -----------------------------------------------
            # Filtro rápido por título
            # -----------------------------------------------

            if not titulo_es_relevante(
                resultado["titulo"]
            ):

                descartadas += 1

                continue


            # -----------------------------------------------
            # Duplicados
            # -----------------------------------------------

            if existe_oferta(
                historial,
                resultado["url"]
            ):

                duplicadas += 1

                continue


            # -----------------------------------------------
            # Obtener detalle
            # -----------------------------------------------

            detalle = obtener_detalle(
                resultado,
                termino
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
    # ACTUALIZAR HISTORIAL
    # ========================================================

    historial[
        "ultima_actualizacion"
    ] = datetime.now().isoformat()


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
        "Duplicadas:",
        duplicadas
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
