import json
import re
import unicodedata
from collections import Counter


# ============================================================
# CONFIGURACIÓN
# ============================================================

ARCHIVO_HISTORIAL = "historial.json"


# ============================================================
# PERFIL PERSONAL
# ============================================================

PERFIL = {
    "profesion": "Técnico en Automatización y Control Industrial",
    "experiencia_meses": 6,

    "certificacion": "SEC Clase D",
    "certificacion_estado": "En trámite",

    "zonas": [
        "Curicó",
        "Molina",
        "Lontué",
        "Talca",
        "Linares"
    ],

    "cargos": [
        "técnico eléctrico junior",
        "técnico de mantenimiento junior",
        "técnico en automatización junior",
        "ayudante eléctrico",
        "ayudante de mantenimiento",
        "técnico electromecánico junior",
        "técnico de instrumentación junior",
        "técnico eléctrico",
        "técnico de mantenimiento",
        "técnico en automatización",
        "electromecánico",
        "electromecánico junior",
        "instrumentista",
        "técnico instrumentista"
    ],

    "competencias": [
        "electricidad industrial",
        "mantenimiento industrial",
        "mantenimiento preventivo",
        "tableros eléctricos",
        "PLC",
        "automatización industrial",
        "control industrial",
        "variadores de frecuencia",
        "HMI",
        "motores eléctricos",
        "lectura de planos"
    ],

    "objetivos_desarrollo": [
        "PLC Siemens",
        "TIA Portal",
        "PLC Allen-Bradley",
        "PLC Schneider",
        "instrumentación industrial",
        "sensores",
        "diagnóstico de fallas",
        "neumática",
        "hidráulica",
        "SCADA",
        "EPLAN",
        "AutoCAD"
    ]
}


# ============================================================
# COMPETENCIAS GENERALES
# ============================================================

COMPETENCIAS = {

    "electricidad industrial": [
        "electricidad industrial",
        "eléctrica industrial",
        "eléctrico industrial",
        "electricista industrial"
    ],

    "mantenimiento industrial": [
        "mantenimiento industrial",
        "mantención industrial",
        "mantenimiento de maquinaria",
        "mantención de maquinaria"
    ],

    "mantenimiento preventivo": [
        "mantenimiento preventivo",
        "mantención preventiva"
    ],

    "mantenimiento correctivo": [
        "mantenimiento correctivo",
        "mantención correctiva"
    ],

    "tableros eléctricos": [
        "tablero eléctrico",
        "tableros eléctricos",
        "tableros electricos",
        "tablero electrico"
    ],

    "PLC": [
        "plc",
        "controlador lógico programable",
        "controlador logico programable"
    ],

    "automatización industrial": [
        "automatización industrial",
        "automatizacion industrial"
    ],

    "control industrial": [
        "control industrial",
        "control automático",
        "control automatico"
    ],

    "variadores de frecuencia": [
        "variador de frecuencia",
        "variadores de frecuencia",
        "vfd"
    ],

    "HMI": [
        "hmi",
        "interfaz hombre máquina",
        "interfaz hombre maquina"
    ],

    "SCADA": [
        "scada"
    ],

    "motores eléctricos": [
        "motor eléctrico",
        "motores eléctricos",
        "motor electrico",
        "motores electricos"
    ],

    "instrumentación industrial": [
        "instrumentación industrial",
        "instrumentacion industrial",
        "instrumentista",
        "instrumentación",
        "instrumentacion"
    ],

    "electromecánica": [
        "electromecánica",
        "electromecanica",
        "electromecánico",
        "electromecanico"
    ],

    "lectura de planos": [
        "lectura de planos",
        "interpretación de planos",
        "interpretacion de planos",
        "planos eléctricos",
        "planos electricos"
    ],

    "diagnóstico de fallas": [
        "diagnóstico de fallas",
        "diagnostico de fallas",
        "detección de fallas",
        "deteccion de fallas",
        "troubleshooting"
    ],

    "sensores": [
        "sensores",
        "sensor industrial",
        "sensor"
    ],

    "neumática": [
        "neumática",
        "neumatica"
    ],

    "hidráulica": [
        "hidráulica",
        "hidraulica"
    ],

    "puesta en marcha": [
        "puesta en marcha",
        "puesta en servicio",
        "comisionamiento"
    ],

    "seguridad eléctrica": [
        "seguridad eléctrica",
        "seguridad electrica"
    ]
}


# ============================================================
# MARCAS PLC
# ============================================================

PLC_MARCAS = {

    "Siemens": [
        "siemens",
        "s7-1200",
        "s7 1200",
        "s7-1500",
        "s7 1500",
        "s7-300",
        "s7 300",
        "s7-400",
        "s7 400",
        "logo!",
        "logo 8",
        "tia portal",
        "step 7",
        "wincc",
        "simatic",
        "sinamics"
    ],

    "Allen-Bradley": [
        "allen-bradley",
        "allen bradley",
        "rockwell automation",
        "rockwell",
        "controllogix",
        "compactlogix",
        "micrologix",
        "studio 5000",
        "studio5000",
        "rslogix",
        "factorytalk"
    ],

    "Schneider": [
        "schneider electric",
        "schneider",
        "modicon",
        "m221",
        "m251",
        "m241",
        "m340",
        "m580",
        "unity pro",
        "unitypro",
        "ecostruxure",
        "eco struxure",
        "plantstruxure"
    ],

    "Mitsubishi": [
        "mitsubishi electric",
        "mitsubishi",
        "fx3u",
        "fx5u",
        "fx5",
        "gx works",
        "gx works2",
        "gx works3"
    ],

    "Omron": [
        "omron",
        "cx-programmer",
        "cx programmer",
        "nx1p",
        "nx",
        "cj2",
        "cj1"
    ],

    "ABB": [
        "abb",
        "800xa",
        "abb acs"
    ],

    "Panasonic": [
        "panasonic",
        "matsushita"
    ],

    "GE / Fanuc": [
        "ge fanuc",
        "ge/fanuc",
        "gefanuc",
        "fanuc"
    ],

    "Beckhoff": [
        "beckhoff",
        "twincat",
        "twin cat"
    ]
}


# ============================================================
# TECNOLOGÍAS ESPECÍFICAS
# ============================================================

TECNOLOGIAS = {

    "PLC Siemens": [
        "plc siemens",
        "siemens s7",
        "s7-1200",
        "s7 1200",
        "s7-1500",
        "s7 1500",
        "s7-300",
        "s7 300",
        "s7-400",
        "s7 400"
    ],

    "PLC Allen-Bradley": [
        "plc allen-bradley",
        "plc allen bradley",
        "allen-bradley",
        "allen bradley",
        "rockwell",
        "controllogix",
        "compactlogix"
    ],

    "PLC Schneider": [
        "plc schneider",
        "schneider electric plc",
        "modicon",
        "m221",
        "m251",
        "m340",
        "m580"
    ],

    "PLC Mitsubishi": [
        "plc mitsubishi",
        "mitsubishi plc",
        "fx3u",
        "fx5u",
        "gx works"
    ],

    "PLC Omron": [
        "plc omron",
        "omron plc",
        "cx-programmer",
        "nx1p",
        "cj2"
    ],

    "PLC ABB": [
        "plc abb",
        "abb plc"
    ],

    "TIA Portal": [
        "tia portal",
        "tia portal siemens"
    ],

    "Step 7": [
        "step 7",
        "simatic step 7"
    ],

    "Studio 5000": [
        "studio 5000",
        "studio5000"
    ],

    "FactoryTalk": [
        "factorytalk",
        "factory talk"
    ],

    "WinCC": [
        "wincc",
        "siemens wincc"
    ],

    "EcoStruxure": [
        "ecostruxure",
        "eco struxure"
    ],

    "AutoCAD": [
        "autocad",
        "auto cad"
    ],

    "EPLAN": [
        "eplan"
    ],

    "HMI Siemens": [
        "hmi siemens",
        "simatic hmi"
    ],

    "SCADA": [
        "scada"
    ],

    "Variadores ABB": [
        "variador abb",
        "variadores abb",
        "abb acs"
    ],

    "Variadores Siemens": [
        "variador siemens",
        "variadores siemens",
        "sinamics"
    ],

    "Variadores Schneider": [
        "variador schneider",
        "variadores schneider",
        "altivar"
    ]
}


# ============================================================
# ELECTROMECÁNICA
# ============================================================

ELECTROMECANICA_DESGLOSE = {

    "mantenimiento industrial": [
        "mantenimiento industrial",
        "mantención industrial",
        "mantenimiento de maquinaria",
        "mantención de maquinaria"
    ],

    "mantenimiento preventivo": [
        "mantenimiento preventivo",
        "mantención preventiva"
    ],

    "mantenimiento correctivo": [
        "mantenimiento correctivo",
        "mantención correctiva"
    ],

    "electricidad industrial": [
        "electricidad industrial",
        "eléctrica industrial",
        "eléctrico industrial",
        "electricista industrial"
    ],

    "motores eléctricos": [
        "motor eléctrico",
        "motores eléctricos",
        "motor electrico",
        "motores electricos"
    ],

    "PLC": [
        "plc",
        "controlador lógico programable",
        "controlador logico programable"
    ],

    "automatización industrial": [
        "automatización industrial",
        "automatizacion industrial"
    ],

    "instrumentación industrial": [
        "instrumentación industrial",
        "instrumentacion industrial",
        "instrumentista"
    ],

    "variadores de frecuencia": [
        "variador de frecuencia",
        "variadores de frecuencia",
        "vfd"
    ],

    "sensores": [
        "sensores",
        "sensor industrial",
        "sensor"
    ],

    "neumática": [
        "neumática",
        "neumatica"
    ],

    "hidráulica": [
        "hidráulica",
        "hidraulica"
    ],

    "tableros eléctricos": [
        "tablero eléctrico",
        "tableros eléctricos",
        "tableros electricos",
        "tablero electrico"
    ],

    "lectura de planos": [
        "lectura de planos",
        "interpretación de planos",
        "interpretacion de planos",
        "planos eléctricos",
        "planos electricos"
    ],

    "diagnóstico de fallas": [
        "diagnóstico de fallas",
        "diagnostico de fallas",
        "detección de fallas",
        "deteccion de fallas",
        "troubleshooting"
    ],

    "puesta en marcha": [
        "puesta en marcha",
        "puesta en servicio",
        "comisionamiento"
    ],

    "HMI": [
        "hmi",
        "interfaz hombre máquina",
        "interfaz hombre maquina"
    ],

    "SCADA": [
        "scada"
    ]
}


# ============================================================
# NORMALIZAR
# ============================================================

def normalizar(texto):

    texto = str(texto or "").lower().strip()

    texto = unicodedata.normalize(
        "NFD",
        texto
    )

    texto = "".join(
        caracter
        for caracter in texto
        if unicodedata.category(caracter) != "Mn"
    )

    texto = texto.replace("–", "-")
    texto = texto.replace("—", "-")
    texto = texto.replace("’", "'")

    return texto


# ============================================================
# BUSCAR TÉRMINO
# ============================================================

def contiene_termino(texto, termino):

    texto = normalizar(texto)
    termino = normalizar(termino).strip()

    if not termino:
        return False

    patron = (
        r"(?<![a-z0-9])"
        + re.escape(termino)
        + r"(?![a-z0-9])"
    )

    return re.search(
        patron,
        texto
    ) is not None


# ============================================================
# TEXTO COMPLETO
# ============================================================

def texto_oferta(oferta):

    partes = [
        oferta.get("titulo", ""),
        oferta.get("descripcion", ""),
        oferta.get("requisitos", "")
    ]

    return " ".join(
        str(parte)
        for parte in partes
        if parte
    )


# ============================================================
# DETECTAR CATEGORÍAS
# ============================================================

def detectar_categorias(texto, catalogo):

    encontradas = []

    for nombre, variantes in catalogo.items():

        for variante in variantes:

            if contiene_termino(
                texto,
                variante
            ):

                encontradas.append(nombre)
                break

    return encontradas


# ============================================================
# CONTEXTO PLC
#
# IMPORTANTE:
# Esta función NO debe considerar simplemente palabras como
# "automatización industrial" como PLC.
#
# Para marcar una oferta como PLC debe existir una referencia
# directa a PLC/controlador o a una tecnología/marca claramente
# relacionada con PLC.
# ============================================================

def tiene_contexto_plc(texto):

    texto_normalizado = normalizar(texto)

    contexto_directo = [
        "plc",
        "controlador lógico programable",
        "controlador logico programable",
        "programacion plc",
        "programacion de plc",
        "programar plc",
        "programación plc",
        "programación de plc",
        "programar plc"
    ]

    if any(
        contiene_termino(
            texto_normalizado,
            termino
        )
        for termino in contexto_directo
    ):
        return True

    # Tecnologías inequívocamente asociadas a PLC
    tecnologias_plc = [
        "tia portal",
        "step 7",
        "simatic",
        "s7-1200",
        "s7 1200",
        "s7-1500",
        "s7 1500",
        "s7-300",
        "s7 300",
        "s7-400",
        "s7 400",
        "studio 5000",
        "studio5000",
        "controllogix",
        "compactlogix",
        "micrologix",
        "rslogix",
        "factorytalk",
        "modicon",
        "ecostruxure",
        "eco struxure",
        "m221",
        "m241",
        "m251",
        "m340",
        "m580",
        "gx works",
        "gx works2",
        "gx works3",
        "fx3u",
        "fx5u",
        "cx-programmer",
        "cx programmer",
        "twincat",
        "twin cat",
        "logo!",
        "logo 8"
    ]

    if any(
        contiene_termino(
            texto_normalizado,
            termino
        )
        for termino in tecnologias_plc
    ):
        return True

    return False


# ============================================================
# DETECTAR PLC
# ============================================================

def tiene_plc(texto):

    return tiene_contexto_plc(texto)


# ============================================================
# DETECTAR MARCAS PLC
#
# ÚNICA FUENTE DE VERDAD PARA TODAS LAS SECCIONES DEL
# ANALIZADOR.
#
# Si una oferta no es considerada PLC por tiene_plc(),
# ninguna marca será contabilizada como PLC.
# ============================================================

def detectar_marcas_plc(texto):

    texto_normalizado = normalizar(texto)

    if not tiene_plc(texto_normalizado):
        return []

    marcas = []

    for marca, variantes in PLC_MARCAS.items():

        for variante in variantes:

            if contiene_termino(
                texto_normalizado,
                variante
            ):

                marcas.append(marca)
                break

    return marcas


# ============================================================
# DETECTAR TECNOLOGÍAS PLC
#
# También depende de la misma detección PLC.
# ============================================================

def detectar_tecnologias_plc(texto):

    texto_normalizado = normalizar(texto)

    if not tiene_plc(texto_normalizado):
        return []

    tecnologias = []

    for tecnologia, variantes in TECNOLOGIAS.items():

        for variante in variantes:

            if contiene_termino(
                texto_normalizado,
                variante
            ):

                tecnologias.append(tecnologia)
                break

    return tecnologias


# ============================================================
# DETECTAR EXPERIENCIA
# ============================================================

def detectar_experiencia(texto):

    texto = normalizar(texto)

    # --------------------------------------------------------
    # SIN EXPERIENCIA
    # --------------------------------------------------------

    patrones_sin_experiencia = [
        "sin experiencia",
        "no requiere experiencia",
        "sin experiencia previa",
        "sin experiencia laboral",
        "no se requiere experiencia",
        "no requiere de experiencia",
        "sin requerir experiencia"
    ]

    if any(
        patron in texto
        for patron in patrones_sin_experiencia
    ):

        return {
            "anos": 0,
            "meses": 0,
            "tipo": "sin_experiencia"
        }

    encontrados = []

    # --------------------------------------------------------
    # MÁS DE X AÑOS
    # --------------------------------------------------------

    patron_mas = re.compile(
        r"mas\s+de\s+"
        r"(\d+(?:[.,]\d+)?)"
        r"\s*anos?"
    )

    for numero in patron_mas.findall(texto):

        numero = float(
            numero.replace(",", ".")
        )

        meses = numero * 12

        if meses <= 240:

            encontrados.append({
                "meses": meses,
                "tipo": "mas_de"
            })

    # --------------------------------------------------------
    # MENOS DE X AÑOS
    # --------------------------------------------------------

    patron_menos = re.compile(
        r"menos\s+de\s+"
        r"(\d+(?:[.,]\d+)?)"
        r"\s*anos?"
    )

    for numero in patron_menos.findall(texto):

        numero = float(
            numero.replace(",", ".")
        )

        meses = max(
            1,
            numero * 12 - 1
        )

        if meses <= 240:

            encontrados.append({
                "meses": meses,
                "tipo": "menos_de"
            })

    # --------------------------------------------------------
    # RANGOS
    # --------------------------------------------------------

    patron_rango = re.compile(
        r"(\d+(?:[.,]\d+)?)"
        r"\s*(?:a|-|hasta)\s*"
        r"(\d+(?:[.,]\d+)?)"
        r"\s*(anos?|mes(?:es)?)"
    )

    for minimo, maximo, unidad in patron_rango.findall(texto):

        maximo = float(
            maximo.replace(",", ".")
        )

        if unidad.startswith("ano"):
            meses = maximo * 12
        else:
            meses = maximo

        if meses <= 240:

            encontrados.append({
                "meses": meses,
                "tipo": "rango"
            })

    # --------------------------------------------------------
    # "experiencia de 2 años"
    # "experiencia mínima de 2 años"
    # --------------------------------------------------------

    patron_experiencia = re.compile(
        r"(?:experiencia|experiencia\s+laboral)"
        r"[^.\n]{0,80}?"
        r"(\d+(?:[.,]\d+)?)"
        r"\s*(anos?|mes(?:es)?)"
    )

    for numero, unidad in patron_experiencia.findall(texto):

        numero = float(
            numero.replace(",", ".")
        )

        if unidad.startswith("ano"):
            meses = numero * 12
        else:
            meses = numero

        if meses <= 240:

            encontrados.append({
                "meses": meses,
                "tipo": "especificada"
            })

    # --------------------------------------------------------
    # "2 años de experiencia"
    # --------------------------------------------------------

    patron_numero = re.compile(
        r"(\d+(?:[.,]\d+)?)"
        r"\s*(anos?|mes(?:es)?)"
        r"\s*(?:de\s*)?"
        r"experiencia"
    )

    for numero, unidad in patron_numero.findall(texto):

        numero = float(
            numero.replace(",", ".")
        )

        if unidad.startswith("ano"):
            meses = numero * 12
        else:
            meses = numero

        if meses <= 240:

            encontrados.append({
                "meses": meses,
                "tipo": "especificada"
            })

    # --------------------------------------------------------
    # EXPERIENCIA EXPRESADA COMO "12 MESES"
    # EN CONTEXTO LABORAL
    # --------------------------------------------------------

    patron_meses_experiencia = re.compile(
        r"(\d+(?:[.,]\d+)?)"
        r"\s*mes(?:es)?"
        r"[^.\n]{0,30}"
        r"experiencia"
    )

    for numero in patron_meses_experiencia.findall(texto):

        numero = float(
            numero.replace(",", ".")
        )

        if numero <= 240:

            encontrados.append({
                "meses": numero,
                "tipo": "especificada"
            })

    # --------------------------------------------------------
    # SIN RESULTADOS
    # --------------------------------------------------------

    if not encontrados:

        return {
            "anos": None,
            "meses": None,
            "tipo": "no_especificada"
        }

    # --------------------------------------------------------
    # EL REQUISITO MÁS EXIGENTE
    # --------------------------------------------------------

    requisito = max(
        encontrados,
        key=lambda x: x["meses"]
    )

    meses = requisito["meses"]

    return {
        "anos": round(
            meses / 12,
            2
        ),
        "meses": meses,
        "tipo": requisito["tipo"]
    }


# ============================================================
# UBICACIÓN
# ============================================================

def analizar_ubicacion(ubicacion):

    ubicacion_normalizada = normalizar(
        ubicacion
    )

    for zona in PERFIL["zonas"]:

        if contiene_termino(
            ubicacion_normalizada,
            zona
        ):

            return {
                "zona_prioritaria": True,
                "zona_coincidente": zona
            }

    return {
        "zona_prioritaria": False,
        "zona_coincidente": None
    }


# ============================================================
# CARGO
# ============================================================

def detectar_cargo(titulo):

    titulo = normalizar(titulo)

    encontrados = []

    for cargo in PERFIL["cargos"]:

        cargo_normalizado = normalizar(
            cargo
        )

        palabras = [
            palabra
            for palabra in cargo_normalizado.split()
            if len(palabra) >= 3
        ]

        if not palabras:
            continue

        coincidencias = 0

        for palabra in palabras:

            if contiene_termino(
                titulo,
                palabra
            ):

                coincidencias += 1

        if len(palabras) <= 2:

            minimo = len(palabras)

        else:

            minimo = 2

        if coincidencias >= minimo:

            encontrados.append(
                cargo
            )

    return list(
        dict.fromkeys(encontrados)
    )


# ============================================================
# COMPARAR EXPERIENCIA
# ============================================================

def comparar_experiencia(meses_solicitados):

    meses_perfil = PERFIL[
        "experiencia_meses"
    ]

    if meses_solicitados is None:
        return "no_especificada"

    if meses_solicitados == 0:
        return "sin_experiencia"

    if meses_solicitados <= meses_perfil:
        return "cumple"

    diferencia = (
        meses_solicitados
        - meses_perfil
    )

    if diferencia <= 6:
        return "brecha_pequena"

    if diferencia <= 12:
        return "brecha_moderada"

    return "brecha_alta"


# ============================================================
# PUNTAJE PERSONAL
#
# Máximo:
# - Competencias: 40
# - Ubicación: 20
# - Cargo: 20
# - Experiencia: 20
# = 100
# ============================================================

def calcular_puntaje(
    competencias,
    experiencia,
    ubicacion,
    cargos
):

    puntaje = 0

    # --------------------------------------------------------
    # COMPETENCIAS
    # --------------------------------------------------------

    coincidencias = sum(
        1
        for competencia in competencias
        if competencia in PERFIL["competencias"]
    )

    puntaje += min(
        coincidencias * 5,
        40
    )

    # --------------------------------------------------------
    # UBICACIÓN
    # --------------------------------------------------------

    if ubicacion["zona_prioritaria"]:
        puntaje += 20

    # --------------------------------------------------------
    # CARGO
    # --------------------------------------------------------

    if cargos:
        puntaje += 20

    # --------------------------------------------------------
    # EXPERIENCIA
    # --------------------------------------------------------

    if experiencia == "cumple":

        puntaje += 20

    elif experiencia == "sin_experiencia":

        puntaje += 20

    elif experiencia == "no_especificada":

        puntaje += 15

    elif experiencia == "brecha_pequena":

        puntaje += 10

    elif experiencia == "brecha_moderada":

        puntaje += 5

    elif experiencia == "brecha_alta":

        puntaje += 0

    return min(
        puntaje,
        100
    )


# ============================================================
# NIVEL
# ============================================================

def nivel(puntaje):

    if puntaje >= 80:
        return "ALTA"

    if puntaje >= 60:
        return "MEDIA"

    return "BAJA"


# ============================================================
# PRIORIDAD
# ============================================================

def prioridad(puntaje):

    if puntaje >= 80:
        return "ALTA"

    if puntaje >= 60:
        return "MEDIA"

    return "BAJA"


# ============================================================
# ANALIZAR UNA OFERTA
# ============================================================

def analizar_oferta(oferta):

    texto = texto_oferta(
        oferta
    )

    competencias = detectar_categorias(
        texto,
        COMPETENCIAS
    )

    # --------------------------------------------------------
    # PLC CANÓNICO
    #
    # Esta variable será reutilizada en todo el sistema.
    # --------------------------------------------------------

    plc_detectado = tiene_plc(
        texto
    )

    # Si la oferta tiene una referencia PLC inequívoca,
    # PLC queda registrado como competencia aunque el texto
    # no use literalmente la palabra "PLC".
    if plc_detectado and "PLC" not in competencias:

        competencias.append("PLC")

    # --------------------------------------------------------
    # TECNOLOGÍAS
    # --------------------------------------------------------

    tecnologias_generales = detectar_categorias(
        texto,
        TECNOLOGIAS
    )

    tecnologias_plc = detectar_tecnologias_plc(
        texto
    )

    tecnologias = list(
        dict.fromkeys(
            tecnologias_generales
            + tecnologias_plc
        )
    )

    # --------------------------------------------------------
    # MARCAS PLC
    # --------------------------------------------------------

    marcas_plc = detectar_marcas_plc(
        texto
    )

    experiencia_detectada = detectar_experiencia(
        texto
    )

    meses_solicitados = (
        experiencia_detectada["meses"]
    )

    ajuste_experiencia = comparar_experiencia(
        meses_solicitados
    )

    ubicacion = analizar_ubicacion(
        oferta.get(
            "ubicacion",
            ""
        )
    )

    cargos = detectar_cargo(
        oferta.get(
            "titulo",
            ""
        )
    )

    puntaje = calcular_puntaje(
        competencias,
        ajuste_experiencia,
        ubicacion,
        cargos
    )

    coincidencias_perfil = [
        competencia
        for competencia in competencias
        if competencia in PERFIL["competencias"]
    ]

    # --------------------------------------------------------
    # FORTALEZAS
    # --------------------------------------------------------

    fortalezas = []

    if coincidencias_perfil:

        fortalezas.append(
            "Coincide con: "
            + ", ".join(
                coincidencias_perfil
            )
        )

    if plc_detectado:

        fortalezas.append(
            "Se detectó requerimiento relacionado "
            "con PLC."
        )

    if marcas_plc:

        fortalezas.append(
            "PLC detectado: "
            + ", ".join(
                marcas_plc
            )
        )

    if tecnologias_plc:

        fortalezas.append(
            "Tecnologías PLC: "
            + ", ".join(
                tecnologias_plc
            )
        )

    if ubicacion["zona_prioritaria"]:

        fortalezas.append(
            "Ubicación dentro de las zonas prioritarias."
        )

    if cargos:

        fortalezas.append(
            "El cargo coincide con el perfil."
        )

    if PERFIL["certificacion_estado"] == "En trámite":

        fortalezas.append(
            "SEC Clase D en trámite."
        )

    # --------------------------------------------------------
    # BRECHAS
    # --------------------------------------------------------

    brechas = []

    if (
        meses_solicitados is not None
        and meses_solicitados > PERFIL["experiencia_meses"]
    ):

        brechas.append(
            f"Solicita {meses_solicitados:g} meses "
            f"de experiencia y el perfil tiene "
            f"{PERFIL['experiencia_meses']} meses."
        )

    for competencia in competencias:

        if competencia not in PERFIL["competencias"]:

            brechas.append(
                competencia
            )

    # --------------------------------------------------------
    # RECOMENDACIÓN
    # --------------------------------------------------------

    if puntaje >= 80:

        recomendacion = "POSTULAR"

    elif puntaje >= 60:

        recomendacion = (
            "EVALUAR Y POSTULAR SI "
            "LOS REQUISITOS NO SON EXCLUYENTES"
        )

    else:

        recomendacion = (
            "PRIORIZAR OTRAS OFERTAS"
        )

    return {

        "competencias_detectadas":
            competencias,

        "tecnologias_detectadas":
            tecnologias,

        "tecnologias_plc_detectadas":
            tecnologias_plc,

        "plc_detectado":
            plc_detectado,

        "plc_marcas_detectadas":
            marcas_plc,

        "experiencia_solicitada": {

            "anos":
                experiencia_detectada["anos"],

            "meses":
                experiencia_detectada["meses"],

            "tipo":
                experiencia_detectada["tipo"]
        },

        "experiencia_perfil": {

            "meses":
                PERFIL["experiencia_meses"],

            "anos":
                round(
                    PERFIL["experiencia_meses"] / 12,
                    2
                )
        },

        "ajuste_experiencia":
            ajuste_experiencia,

        "ubicacion":
            ubicacion,

        "cargos_coincidentes":
            cargos,

        "compatibilidad": {

            "puntaje":
                puntaje,

            "nivel":
                nivel(puntaje),

            "prioridad":
                prioridad(puntaje),

            "recomendacion":
                recomendacion,

            "fortalezas":
                fortalezas,

            "brechas":
                list(
                    dict.fromkeys(
                        brechas
                    )
                )
        }
    }


# ============================================================
# ANALIZAR PLC POR MARCA
#
# IMPORTANTE:
# Solo se utiliza el campo plc_detectado generado por
# analizar_oferta().
#
# Esto garantiza que esta sección y el análisis de mercado
# tengan exactamente el mismo universo de ofertas.
# ============================================================

def analizar_plc_por_marca(ofertas):

    contador = Counter()

    for oferta in ofertas:

        analisis = oferta.get(
            "analisis",
            {}
        )

        if not analisis.get(
            "plc_detectado",
            False
        ):
            continue

        marcas = analisis.get(
            "plc_marcas_detectadas",
            []
        )

        for marca in set(marcas):

            contador[marca] += 1

    return dict(
        contador.most_common()
    )


# ============================================================
# ANÁLISIS DETALLADO DE PLC
#
# MISMA FUENTE DE VERDAD:
# plc_detectado
# ============================================================

def analizar_mercado_plc(ofertas):

    ofertas_plc = 0

    marcas = Counter()
    tecnologias = Counter()

    tecnologias_validas = {
        "PLC Siemens",
        "PLC Allen-Bradley",
        "PLC Schneider",
        "PLC Mitsubishi",
        "PLC Omron",
        "PLC ABB",
        "TIA Portal",
        "Step 7",
        "Studio 5000",
        "FactoryTalk",
        "WinCC",
        "EcoStruxure"
    }

    for oferta in ofertas:

        analisis = oferta.get(
            "analisis",
            {}
        )

        if not analisis.get(
            "plc_detectado",
            False
        ):
            continue

        ofertas_plc += 1

        marcas_oferta = analisis.get(
            "plc_marcas_detectadas",
            []
        )

        tecnologias_oferta = analisis.get(
            "tecnologias_plc_detectadas",
            []
        )

        for marca in set(
            marcas_oferta
        ):

            marcas[marca] += 1

        for tecnologia in set(
            tecnologias_oferta
        ):

            if tecnologia in tecnologias_validas:

                tecnologias[
                    tecnologia
                ] += 1

    return {

        "ofertas_con_PLC":
            ofertas_plc,

        "marcas_PLC":
            dict(
                marcas.most_common()
            ),

        "tecnologias_PLC":
            dict(
                tecnologias.most_common()
            )
    }


# ============================================================
# DESGLOSE ELECTROMECÁNICA
# ============================================================

def analizar_electromecanica(ofertas):

    contador = Counter()

    ofertas_electromecanica = 0

    for oferta in ofertas:

        analisis = oferta.get(
            "analisis",
            {}
        )

        competencias = analisis.get(
            "competencias_detectadas",
            []
        )

        if "electromecánica" not in competencias:

            continue

        ofertas_electromecanica += 1

        competencias_electro = detectar_categorias(
            texto_oferta(oferta),
            ELECTROMECANICA_DESGLOSE
        )

        for competencia in set(
            competencias_electro
        ):

            contador[
                competencia
            ] += 1

    desglose = {}

    for competencia, cantidad in (
        contador.most_common()
    ):

        porcentaje = round(
            (
                cantidad
                / ofertas_electromecanica
            ) * 100,
            1
        )

        desglose[competencia] = {

            "ofertas":
                cantidad,

            "porcentaje":
                porcentaje
        }

    return {

        "ofertas_electromecanica":
            ofertas_electromecanica,

        "competencias_dentro_electromecanica":
            desglose
    }


# ============================================================
# GENERAR PLAN DE DESARROLLO
# ============================================================

def generar_plan_desarrollo(mercado):

    competencias_mercado = (
        mercado[
            "competencias_mas_solicitadas"
        ]
    )

    resultado = []

    for competencia, cantidad in (
        competencias_mercado.items()
    ):

        esta_en_perfil = (
            competencia
            in PERFIL["competencias"]
        )

        es_objetivo = any(
            normalizar(competencia)
            == normalizar(objetivo)
            for objetivo
            in PERFIL["objetivos_desarrollo"]
        )

        # ----------------------------------------------------
        # ESTADO
        # ----------------------------------------------------

        if esta_en_perfil:

            estado = "YA_EN_PERFIL"

            prioridad_base = 1

        else:

            estado = "BRECHA"

            prioridad_base = 3

        # ----------------------------------------------------
        # OBJETIVO PERSONAL
        # ----------------------------------------------------

        if es_objetivo:

            prioridad_base += 3

        # ----------------------------------------------------
        # DEMANDA DEL MERCADO
        # ----------------------------------------------------

        if cantidad >= 50:

            prioridad_base += 4

        elif cantidad >= 30:

            prioridad_base += 3

        elif cantidad >= 20:

            prioridad_base += 2

        elif cantidad >= 10:

            prioridad_base += 1

        # ----------------------------------------------------
        # COMPETENCIA DE ALTA PRIORIDAD PARA EL PERFIL
        # ----------------------------------------------------

        competencias_criticas = {
            "instrumentación industrial": 2,
            "diagnóstico de fallas": 2,
            "sensores": 2,
            "SCADA": 2,
            "neumática": 1,
            "hidráulica": 1,
            "puesta en marcha": 1
        }

        prioridad_base += competencias_criticas.get(
            competencia,
            0
        )

        resultado.append({

            "competencia":
                competencia,

            "ofertas":
                cantidad,

            "estado":
                estado,

            "es_objetivo":
                es_objetivo,

            "prioridad":
                prioridad_base
        })

    resultado.sort(
        key=lambda x: (
            x["prioridad"],
            x["ofertas"]
        ),
        reverse=True
    )

    return resultado


# ============================================================
# GENERAR RECOMENDACIONES
# ============================================================

def generar_recomendaciones(mercado):

    recomendaciones = []

    competencias = mercado[
        "competencias_mas_solicitadas"
    ]

    plc = mercado[
        "plc_por_marca"
    ]

    electro = mercado[
        "electromecanica"
    ]

    # --------------------------------------------------------
    # PLC
    # --------------------------------------------------------

    if plc:

        marcas = list(
            plc.keys()
        )

        recomendaciones.append(
            "Priorizar formación práctica en PLC. "
            "Las marcas detectadas con mayor frecuencia "
            "son: "
            + ", ".join(
                marcas[:3]
            )
            + "."
        )

    # --------------------------------------------------------
    # ELECTROMECÁNICA
    # --------------------------------------------------------

    cantidad_electro = (
        electro[
            "ofertas_electromecanica"
        ]
    )

    total = mercado[
        "ofertas_analizadas"
    ]

    if cantidad_electro and total:

        porcentaje = round(
            cantidad_electro
            / total
            * 100,
            1
        )

        recomendaciones.append(
            f"Considerar electromecánica como "
            f"línea importante de búsqueda: "
            f"{cantidad_electro} ofertas "
            f"({porcentaje}% del conjunto analizado)."
        )

    # --------------------------------------------------------
    # TOP COMPETENCIAS
    # --------------------------------------------------------

    top = list(
        competencias.items()
    )[:5]

    if top:

        recomendaciones.append(
            "Mantener como núcleo profesional: "
            + ", ".join(
                nombre
                for nombre, _ in top
            )
            + "."
        )

    # --------------------------------------------------------
    # COMBINACIÓN ESTRATÉGICA
    # --------------------------------------------------------

    nombres = set(
        competencias.keys()
    )

    if (
        "mantenimiento industrial" in nombres
        and "PLC" in nombres
        and "electricidad industrial" in nombres
    ):

        recomendaciones.append(
            "Buscar especialmente cargos que combinen "
            "mantenimiento industrial + electricidad "
            "industrial + PLC/automatización."
        )

    # --------------------------------------------------------
    # EXPERIENCIA
    # --------------------------------------------------------

    experiencia = mercado[
        "experiencia_requerida"
    ]

    sin_experiencia = experiencia.get(
        "sin experiencia",
        0
    )

    no_especificada = experiencia.get(
        "no especificada",
        0
    )

    if sin_experiencia > 0:

        recomendaciones.append(
            "No limitar la búsqueda a cargos que "
            "exijan experiencia: también seguir "
            "las ofertas que aceptan candidatos "
            "sin experiencia."
        )

    if no_especificada > 0:

        recomendaciones.append(
            "Dar prioridad adicional a ofertas donde "
            "la experiencia no está especificada, "
            "porque no presentan una barrera explícita "
            "de años de experiencia."
        )

    # --------------------------------------------------------
    # PLAN DE DESARROLLO
    # --------------------------------------------------------

    plan = mercado.get(
        "plan_desarrollo",
        []
    )

    brechas = [
        x
        for x in plan
        if x["estado"] == "BRECHA"
    ]

    brechas.sort(
        key=lambda x: (
            x["prioridad"],
            x["ofertas"]
        ),
        reverse=True
    )

    if brechas:

        recomendaciones.append(
            "Para cerrar brechas, comenzar por: "
            + ", ".join(
                x["competencia"]
                for x in brechas[:5]
            )
            + "."
        )

    return recomendaciones


# ============================================================
# ANALIZAR MERCADO
# ============================================================

def analizar_mercado(ofertas):

    total = len(ofertas)

    contador_competencias = Counter()
    contador_tecnologias = Counter()
    contador_experiencia = Counter()
    contador_ubicaciones = Counter()
    contador_cargos = Counter()

    ofertas_sin_experiencia = 0

    experiencias = []

    for oferta in ofertas:

        analisis = oferta.get(
            "analisis",
            {}
        )

        competencias = analisis.get(
            "competencias_detectadas",
            []
        )

        tecnologias = analisis.get(
            "tecnologias_detectadas",
            []
        )

        experiencia = analisis.get(
            "experiencia_solicitada",
            {}
        )

        # ----------------------------------------------------
        # COMPETENCIAS
        # ----------------------------------------------------

        for competencia in set(
            competencias
        ):

            contador_competencias[
                competencia
            ] += 1

        # ----------------------------------------------------
        # TECNOLOGÍAS
        # ----------------------------------------------------

        for tecnologia in set(
            tecnologias
        ):

            contador_tecnologias[
                tecnologia
            ] += 1

        # ----------------------------------------------------
        # EXPERIENCIA
        # ----------------------------------------------------

        meses = experiencia.get(
            "meses"
        )

        if meses is None:

            contador_experiencia[
                "no especificada"
            ] += 1

        elif meses == 0:

            contador_experiencia[
                "sin experiencia"
            ] += 1

            ofertas_sin_experiencia += 1

        else:

            anos = meses / 12

            experiencias.append(
                anos
            )

            if anos < 1:

                etiqueta = "menos de 1 año"

            elif anos <= 1:

                etiqueta = "1 año"

            elif anos <= 2:

                etiqueta = "2 años"

            elif anos <= 3:

                etiqueta = "3 años"

            else:

                etiqueta = "más de 3 años"

            contador_experiencia[
                etiqueta
            ] += 1

        # ----------------------------------------------------
        # UBICACIÓN
        # ----------------------------------------------------

        ubicacion = str(
            oferta.get(
                "ubicacion",
                ""
            )
        ).strip()

        if ubicacion:

            contador_ubicaciones[
                ubicacion
            ] += 1

        # ----------------------------------------------------
        # CARGO
        # ----------------------------------------------------

        titulo = str(
            oferta.get(
                "titulo",
                ""
            )
        ).strip()

        if titulo:

            contador_cargos[
                titulo
            ] += 1

    # --------------------------------------------------------
    # ESTADÍSTICAS EXPERIENCIA
    # --------------------------------------------------------

    if experiencias:

        experiencia_promedio = round(
            sum(experiencias)
            / len(experiencias),
            1
        )

        experiencia_minima = round(
            min(experiencias),
            1
        )

        experiencia_maxima = round(
            max(experiencias),
            1
        )

    else:

        experiencia_promedio = None
        experiencia_minima = None
        experiencia_maxima = None

    # --------------------------------------------------------
    # PLC
    # --------------------------------------------------------

    plc_por_marca = analizar_plc_por_marca(
        ofertas
    )

    analisis_plc = analizar_mercado_plc(
        ofertas
    )

    # --------------------------------------------------------
    # VERIFICACIÓN DE CONSISTENCIA PLC
    #
    # Esta comprobación evita volver a guardar resultados
    # contradictorios.
    # --------------------------------------------------------

    if plc_por_marca != analisis_plc["marcas_PLC"]:

        raise RuntimeError(
            "ERROR DE CONSISTENCIA PLC: "
            "el desglose por marca y el análisis de mercado "
            "no coinciden."
        )

    # --------------------------------------------------------
    # ELECTROMECÁNICA
    # --------------------------------------------------------

    desglose_electromecanica = (
        analizar_electromecanica(
            ofertas
        )
    )

    mercado = {

        "ofertas_analizadas":
            total,

        "competencias_mas_solicitadas":
            dict(
                contador_competencias.most_common()
            ),

        "tecnologias_especificas":
            dict(
                contador_tecnologias.most_common()
            ),

        "plc_por_marca":
            plc_por_marca,

        "analisis_PLC":
            analisis_plc,

        "electromecanica":
            desglose_electromecanica,

        "experiencia_requerida":
            dict(
                contador_experiencia.most_common()
            ),

        "experiencia_promedio_anos":
            experiencia_promedio,

        "experiencia_minima_anos":
            experiencia_minima,

        "experiencia_maxima_anos":
            experiencia_maxima,

        "ofertas_sin_experiencia":
            ofertas_sin_experiencia,

        "ubicaciones_mas_repetidas":
            dict(
                contador_ubicaciones.most_common(15)
            ),

        "cargos_mas_repetidos":
            dict(
                contador_cargos.most_common(15)
            )
    }

    mercado[
        "plan_desarrollo"
    ] = generar_plan_desarrollo(
        mercado
    )

    mercado[
        "recomendaciones"
    ] = generar_recomendaciones(
        mercado
    )

    return mercado


# ============================================================
# ANALIZAR HISTORIAL
# ============================================================

def analizar_historial():

    try:

        with open(
            ARCHIVO_HISTORIAL,
            "r",
            encoding="utf-8"
        ) as archivo:

            historial = json.load(
                archivo
            )

    except FileNotFoundError:

        print(
            "No se encontró historial.json"
        )

        return

    except json.JSONDecodeError as error:

        print(
            "Error al leer historial.json:"
        )

        print(error)

        return

    ofertas = historial.get(
        "ofertas",
        []
    )

    if not isinstance(
        ofertas,
        list
    ):

        print(
            "Error: 'ofertas' no contiene una lista."
        )

        return

    # ========================================================
    # ANALIZAR CADA OFERTA UNA SOLA VEZ
    # ========================================================

    for oferta in ofertas:

        oferta["analisis"] = analizar_oferta(
            oferta
        )

    # ========================================================
    # ANALIZAR MERCADO
    # ========================================================

    mercado = analizar_mercado(
        ofertas
    )

    historial[
        "resumen_mercado"
    ] = mercado

    # ========================================================
    # GUARDAR PERFIL
    # ========================================================

    historial["perfil"] = {

        "profesion":
            PERFIL["profesion"],

        "experiencia_meses":
            PERFIL["experiencia_meses"],

        "certificacion":
            PERFIL["certificacion"],

        "certificacion_estado":
            PERFIL["certificacion_estado"]
    }

    historial[
        "perfil_analizado"
    ] = {

        "profesion":
            PERFIL["profesion"],

        "experiencia_meses":
            PERFIL["experiencia_meses"],

        "anos_experiencia":
            round(
                PERFIL["experiencia_meses"] / 12,
                2
            ),

        "certificacion_electrica": {

            "tipo":
                PERFIL["certificacion"],

            "estado":
                PERFIL["certificacion_estado"]
        },

        "objetivo":
            "Conseguir experiencia práctica "
            "en terreno y crecer hacia "
            "automatización y mantenimiento "
            "industrial."
    }

    historial[
        "ultima_actualizacion"
    ] = "actualizado automáticamente"

    # ========================================================
    # GUARDAR
    # ========================================================

    with open(
        ARCHIVO_HISTORIAL,
        "w",
        encoding="utf-8"
    ) as archivo:

        json.dump(
            historial,
            archivo,
            ensure_ascii=False,
            indent=2
        )

    # ========================================================
    # RESULTADO
    # ========================================================

    print()
    print("======================================")
    print("       INVESTIGADOR LABORAL")
    print("======================================")

    print()
    print(
        "Ofertas analizadas:",
        mercado["ofertas_analizadas"]
    )

    # ========================================================
    # COMPETENCIAS
    # ========================================================

    print()
    print("======================================")
    print("COMPETENCIAS MÁS SOLICITADAS")
    print("======================================")

    for i, (
        nombre,
        cantidad
    ) in enumerate(
        mercado[
            "competencias_mas_solicitadas"
        ].items(),
        start=1
    ):

        if i > 20:
            break

        print(
            f"{i}. {nombre}: "
            f"{cantidad} ofertas"
        )

    # ========================================================
    # PLC POR MARCA
    # ========================================================

    print()
    print("======================================")
    print("DESGLOSE PLC POR MARCA")
    print("======================================")

    plc_por_marca = mercado[
        "plc_por_marca"
    ]

    if plc_por_marca:

        for i, (
            marca,
            cantidad
        ) in enumerate(
            plc_por_marca.items(),
            start=1
        ):

            print(
                f"{i}. {marca}: "
                f"{cantidad} ofertas"
            )

    else:

        print(
            "No se detectaron marcas de PLC."
        )

    # ========================================================
    # ANÁLISIS PLC
    # ========================================================

    print()
    print("======================================")
    print("ANÁLISIS DEL MERCADO PLC")
    print("======================================")

    analisis_plc = mercado[
        "analisis_PLC"
    ]

    print(
        "Ofertas con PLC:",
        analisis_plc[
            "ofertas_con_PLC"
        ]
    )

    print()
    print("Marcas PLC:")

    for marca, cantidad in (
        analisis_plc[
            "marcas_PLC"
        ].items()
    ):

        print(
            f"- {marca}: "
            f"{cantidad} ofertas"
        )

    print()
    print("Tecnologías PLC:")

    for tecnologia, cantidad in (
        analisis_plc[
            "tecnologias_PLC"
        ].items()
    ):

        print(
            f"- {tecnologia}: "
            f"{cantidad} ofertas"
        )

    # ========================================================
    # TECNOLOGÍAS
    # ========================================================

    print()
    print("======================================")
    print("TECNOLOGÍAS ESPECÍFICAS")
    print("======================================")

    tecnologias = mercado[
        "tecnologias_especificas"
    ]

    if tecnologias:

        for i, (
            nombre,
            cantidad
        ) in enumerate(
            tecnologias.items(),
            start=1
        ):

            if i > 20:
                break

            print(
                f"{i}. {nombre}: "
                f"{cantidad} ofertas"
            )

    else:

        print(
            "No se detectaron tecnologías específicas."
        )

    # ========================================================
    # ELECTROMECÁNICA
    # ========================================================

    print()
    print("======================================")
    print("DESGLOSE ELECTROMECÁNICA")
    print("======================================")

    electromecanica = mercado[
        "electromecanica"
    ]

    cantidad_electromecanica = (
        electromecanica[
            "ofertas_electromecanica"
        ]
    )

    total = mercado[
        "ofertas_analizadas"
    ]

    print(
        "Ofertas de electromecánica:",
        cantidad_electromecanica
    )

    if total:

        porcentaje = round(
            cantidad_electromecanica
            / total
            * 100,
            1
        )

        print(
            "Porcentaje del mercado:",
            f"{porcentaje}%"
        )

    competencias_electromecanica = (
        electromecanica[
            "competencias_dentro_electromecanica"
        ]
    )

    if competencias_electromecanica:

        print()

        for i, (
            nombre,
            datos
        ) in enumerate(
            competencias_electromecanica.items(),
            start=1
        ):

            print(
                f"{i}. {nombre}: "
                f"{datos['ofertas']} ofertas "
                f"({datos['porcentaje']}%)"
            )

    else:

        print(
            "No se detectaron competencias "
            "dentro de electromecánica."
        )

    # ========================================================
    # EXPERIENCIA
    # ========================================================

    print()
    print("======================================")
    print("EXPERIENCIA SOLICITADA")
    print("======================================")

    for nombre, cantidad in (
        mercado[
            "experiencia_requerida"
        ].items()
    ):

        print(
            f"- {nombre}: "
            f"{cantidad} ofertas"
        )

    if (
        mercado[
            "experiencia_promedio_anos"
        ] is not None
    ):

        print()
        print(
            "Experiencia promedio:",
            mercado[
                "experiencia_promedio_anos"
            ],
            "años"
        )

        print(
            "Experiencia mínima:",
            mercado[
                "experiencia_minima_anos"
            ],
            "años"
        )

        print(
            "Experiencia máxima:",
            mercado[
                "experiencia_maxima_anos"
            ],
            "años"
        )

    # ========================================================
    # UBICACIONES
    # ========================================================

    print()
    print("======================================")
    print("UBICACIONES MÁS REPETIDAS")
    print("======================================")

    ubicaciones = mercado[
        "ubicaciones_mas_repetidas"
    ]

    if ubicaciones:

        for nombre, cantidad in (
            ubicaciones.items()
        ):

            print(
                f"- {nombre}: "
                f"{cantidad} ofertas"
            )

    else:

        print(
            "No se detectaron ubicaciones."
        )

    # ========================================================
    # PLAN DE DESARROLLO
    # ========================================================

    print()
    print("======================================")
    print("PLAN DE DESARROLLO")
    print("======================================")

    plan = mercado[
        "plan_desarrollo"
    ]

    if plan:

        for item in plan[:15]:

            estado = item[
                "estado"
            ]

            objetivo = (
                "OBJETIVO"
                if item["es_objetivo"]
                else ""
            )

            print(
                f"- {item['competencia']}: "
                f"{item['ofertas']} ofertas | "
                f"{estado} | "
                f"prioridad {item['prioridad']} "
                f"{objetivo}"
            )

    else:

        print(
            "No se detectaron brechas."
        )

    # ========================================================
    # RECOMENDACIONES
    # ========================================================

    print()
    print("======================================")
    print("RECOMENDACIONES")
    print("======================================")

    recomendaciones = mercado[
        "recomendaciones"
    ]

    for i, recomendacion in enumerate(
        recomendaciones,
        start=1
    ):

        print(
            f"{i}. {recomendacion}"
        )

    # ========================================================
    # OFERTAS DE MAYOR COMPATIBILIDAD
    # ========================================================

    print()
    print("======================================")
    print("OFERTAS DE MAYOR COMPATIBILIDAD")
    print("======================================")

    ofertas_ordenadas = sorted(
        ofertas,
        key=lambda oferta:
            oferta.get(
                "analisis",
                {}
            ).get(
                "compatibilidad",
                {}
            ).get(
                "puntaje",
                0
            ),
        reverse=True
    )

    for oferta in ofertas_ordenadas[:10]:

        analisis = oferta.get(
            "analisis",
            {}
        )

        compatibilidad = analisis.get(
            "compatibilidad",
            {}
        )

        print()
        print(
            oferta.get(
                "titulo",
                "Sin título"
            )
        )

        print(
            "Puntaje:",
            compatibilidad.get(
                "puntaje",
                0
            ),
            "/ 100",
            "|",
            compatibilidad.get(
                "nivel",
                ""
            ),
            "|",
            compatibilidad.get(
                "recomendacion",
                ""
            )
        )

        # ----------------------------------------------------
        # UBICACIÓN
        # ----------------------------------------------------

        ubicacion = analisis.get(
            "ubicacion",
            {}
        )

        if ubicacion.get(
            "zona_prioritaria"
        ):

            print(
                "Zona:",
                ubicacion.get(
                    "zona_coincidente"
                )
            )

        # ----------------------------------------------------
        # COMPETENCIAS
        # ----------------------------------------------------

        competencias_oferta = analisis.get(
            "competencias_detectadas",
            []
        )

        if competencias_oferta:

            print(
                "Competencias:",
                ", ".join(
                    competencias_oferta
                )
            )

        # ----------------------------------------------------
        # TECNOLOGÍAS
        # ----------------------------------------------------

        tecnologias_oferta = analisis.get(
            "tecnologias_detectadas",
            []
        )

        if tecnologias_oferta:

            print(
                "Tecnologías:",
                ", ".join(
                    tecnologias_oferta
                )
            )

        # ----------------------------------------------------
        # PLC
        # ----------------------------------------------------

        if analisis.get(
            "plc_detectado",
            False
        ):

            print(
                "PLC: SÍ"
            )

            marcas_plc = analisis.get(
                "plc_marcas_detectadas",
                []
            )

            if marcas_plc:

                print(
                    "Marcas PLC:",
                    ", ".join(
                        marcas_plc
                    )
                )

            tecnologias_plc = analisis.get(
                "tecnologias_plc_detectadas",
                []
            )

            if tecnologias_plc:

                print(
                    "Tecnologías PLC:",
                    ", ".join(
                        tecnologias_plc
                    )
                )

        # ----------------------------------------------------
        # EXPERIENCIA
        # ----------------------------------------------------

        experiencia_oferta = analisis.get(
            "experiencia_solicitada",
            {}
        )

        if experiencia_oferta.get(
            "tipo"
        ) != "no_especificada":

            print(
                "Experiencia solicitada:",
                experiencia_oferta.get(
                    "anos"
                ),
                "años"
            )

            print(
                "Ajuste experiencia:",
                analisis.get(
                    "ajuste_experiencia",
                    ""
                )
            )

        else:

            print(
                "Experiencia solicitada: "
                "no especificada"
            )

        # ----------------------------------------------------
        # FORTALEZAS
        # ----------------------------------------------------

        fortalezas = compatibilidad.get(
            "fortalezas",
            []
        )

        if fortalezas:

            print(
                "Fortalezas:",
                " | ".join(
                    fortalezas[:4]
                )
            )

        # ----------------------------------------------------
        # BRECHAS
        # ----------------------------------------------------

        brechas = compatibilidad.get(
            "brechas",
            []
        )

        if brechas:

            print(
                "Brechas:",
                ", ".join(
                    str(brecha)
                    for brecha in brechas[:5]
                )
            )

    print()
    print("======================================")
    print("ANÁLISIS COMPLETADO")
    print("======================================")


# ============================================================
# EJECUTAR
# ============================================================

if __name__ == "__main__":

    analizar_historial()
