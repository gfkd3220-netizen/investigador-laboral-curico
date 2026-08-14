import json
import re
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
        "técnico en automatización"
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
    ]
}


# ============================================================
# COMPETENCIAS GENERALES
#
# Cada publicación cuenta SOLO 1 vez por competencia.
# ============================================================

COMPETENCIAS = {

    "electricidad industrial": [
        "electricidad industrial",
        "eléctrica industrial",
        "electrico industrial",
        "electricista industrial"
    ],

    "mantenimiento industrial": [
        "mantenimiento industrial",
        "mantención industrial"
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
        "tableros electricos"
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
        "instrumentista"
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
        "sensor industrial"
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
# ============================================================
# DESGLOSE PLC POR MARCA
#
# Una publicación cuenta SOLO 1 vez por marca.
#
# No basta con que aparezca la palabra "Siemens" de forma
# aislada. Se intenta comprobar que exista contexto de PLC,
# automatización, programación o modelos de la marca.
# ============================================================
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
        "tia portal",
        "step 7",
        "wincc",
        "simatic"
    ],

    "Allen-Bradley": [
        "allen-bradley",
        "allen bradley",
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
        "schneider",
        "schneider electric",
        "modicon",
        "m251",
        "m340",
        "m580",
        "m580",
        "unity pro",
        "unitypro",
        "ecostruxure",
        "plantstruxure"
    ],

    "Mitsubishi": [
        "mitsubishi",
        "fx3u",
        "fx5u",
        "gx works"
    ],

    "Omron": [
        "omron",
        "cx-programmer",
        "cx programmer",
        "nx1p",
        "cj2"
    ],

    "ABB": [
        "abb",
        "800xa",
        "800xA",
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
        "twincat"
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
# DESGLOSE DE ELECTROMECÁNICA
#
# Este bloque NO cuenta todo el mercado.
#
# Primero identifica las ofertas donde aparece
# "electromecánica/electromecánico".
#
# Después analiza qué competencias aparecen DENTRO
# de esas ofertas.
# ============================================================

ELECTROMECANICA_DESGLOSE = {

    "mantenimiento industrial": [
        "mantenimiento industrial",
        "mantención industrial",
        "mantenimiento de maquinaria",
        "mantencion de maquinaria"
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
        "electrico industrial",
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
        "vfd",
        "variador"
    ],

    "sensores": [
        "sensores",
        "sensor industrial"
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
        "tableros electricos"
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

    texto = str(texto).lower()

    reemplazos = {
        "á": "a",
        "é": "e",
        "í": "i",
        "ó": "o",
        "ú": "u",
        "ñ": "n"
    }

    for a, b in reemplazos.items():
        texto = texto.replace(a, b)

    return texto


# ============================================================
# TEXTO COMPLETO DE UNA OFERTA
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
#
# Una publicación = máximo 1 conteo por categoría.
# ============================================================

def detectar_categorias(texto, catalogo):

    texto = normalizar(texto)

    encontradas = []

    for nombre, variantes in catalogo.items():

        for variante in variantes:

            if normalizar(variante) in texto:

                encontradas.append(nombre)

                break

    return encontradas


# ============================================================
# DETECTAR MARCAS PLC
#
# Una publicación = máximo 1 conteo por marca.
# ============================================================

def detectar_marcas_plc(texto):

    texto = normalizar(texto)

    marcas = []

    # Contexto que indica que la oferta realmente
    # está hablando de automatización / PLC.
    contexto_plc = [
        "plc",
        "programacion",
        "programación",
        "automatizacion",
        "automatización",
        "control industrial",
        "sistema de control",
        "hmi",
        "scada",
        "tia portal",
        "step 7",
        "controllogix",
        "compactlogix",
        "modicon",
        "s7-1200",
        "s7 1200",
        "s7-1500",
        "s7 1500"
    ]

    tiene_contexto = any(
        normalizar(palabra) in texto
        for palabra in contexto_plc
    )

    if not tiene_contexto:

        return marcas

    for marca, variantes in PLC_MARCAS.items():

        for variante in variantes:

            if normalizar(variante) in texto:

                marcas.append(marca)

                break

    return marcas


# ============================================================
# DETECTAR EXPERIENCIA
#
# Evita fechas, teléfonos, códigos, etc.
# ============================================================

def detectar_experiencia(texto):

    texto = normalizar(texto)

    # --------------------------------------------------------
    # SIN EXPERIENCIA
    # --------------------------------------------------------

    if (
        "sin experiencia" in texto
        or "no requiere experiencia" in texto
        or "sin experiencia previa" in texto
    ):

        return {
            "anos": 0,
            "meses": 0
        }

    encontrados = []

    # --------------------------------------------------------
    # "experiencia de 2 años"
    # "experiencia mínima de 2 años"
    # "experiencia laboral de 6 meses"
    # --------------------------------------------------------

    patron_1 = (
        r"experiencia"
        r"[^.\n]{0,50}?"
        r"(\d+(?:[.,]\d+)?)"
        r"\s*"
        r"(anos?|mes(?:es)?)"
    )

    # --------------------------------------------------------
    # "2 años de experiencia"
    # "6 meses de experiencia"
    # --------------------------------------------------------

    patron_2 = (
        r"(\d+(?:[.,]\d+)?)"
        r"\s*"
        r"(anos?|mes(?:es)?)"
        r"\s*(?:de\s*)?"
        r"experiencia"
    )

    for patron in [patron_1, patron_2]:

        coincidencias = re.findall(
            patron,
            texto
        )

        for numero, unidad in coincidencias:

            numero = float(
                numero.replace(",", ".")
            )

            if unidad.startswith("ano"):

                meses = numero * 12

            else:

                meses = numero

            # Máximo razonable considerado:
            # 20 años.
            if meses <= 240:

                encontrados.append(meses)

    # --------------------------------------------------------
    # "más de 3 años"
    # --------------------------------------------------------

    patron_mas = (
        r"mas\s+de\s+"
        r"(\d+(?:[.,]\d+)?)"
        r"\s*anos?"
    )

    for numero in re.findall(
        patron_mas,
        texto
    ):

        numero = float(
            numero.replace(",", ".")
        )

        meses = numero * 12

        if meses <= 240:

            encontrados.append(meses)

    # --------------------------------------------------------
    # "menos de 1 año"
    # --------------------------------------------------------

    patron_menos = (
        r"menos\s+de\s+"
        r"(\d+(?:[.,]\d+)?)"
        r"\s*anos?"
    )

    for numero in re.findall(
        patron_menos,
        texto
    ):

        numero = float(
            numero.replace(",", ".")
        )

        meses = numero * 12

        if meses <= 240:

            encontrados.append(
                max(1, meses - 1)
            )

    if not encontrados:

        return {
            "anos": None,
            "meses": None
        }

    meses = max(encontrados)

    return {
        "anos": meses / 12,
        "meses": meses
    }


# ============================================================
# UBICACIÓN
# ============================================================

def analizar_ubicacion(ubicacion):

    ubicacion = str(ubicacion)

    ubicacion_normalizada = normalizar(
        ubicacion
    )

    for zona in PERFIL["zonas"]:

        if normalizar(zona) in ubicacion_normalizada:

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

        palabras = cargo_normalizado.split()

        coincidencias = 0

        for palabra in palabras:

            if (
                len(palabra) >= 4
                and palabra in titulo
            ):

                coincidencias += 1

        if coincidencias >= 2:

            encontrados.append(cargo)

    return encontrados


# ============================================================
# COMPARAR EXPERIENCIA
# ============================================================

def comparar_experiencia(meses_solicitados):

    meses_perfil = PERFIL[
        "experiencia_meses"
    ]

    if meses_solicitados is None:

        return "no_especificada"

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
# ============================================================

def calcular_puntaje(
    competencias,
    experiencia,
    ubicacion,
    cargos
):

    puntaje = 0

    for competencia in competencias:

        if competencia in PERFIL["competencias"]:

            puntaje += 8

    puntaje = min(
        puntaje,
        40
    )

    if ubicacion["zona_prioritaria"]:

        puntaje += 20

    if cargos:

        puntaje += 20

    if experiencia == "cumple":

        puntaje += 20

    elif experiencia == "no_especificada":

        puntaje += 15

    elif experiencia == "brecha_pequena":

        puntaje += 10

    elif experiencia == "brecha_moderada":

        puntaje += 5

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

    tecnologias = detectar_categorias(
        texto,
        TECNOLOGIAS
    )

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
        if competencia
        in PERFIL["competencias"]
    ]

    fortalezas = []

    if coincidencias_perfil:

        fortalezas.append(
            "Coincide con: "
            + ", ".join(
                coincidencias_perfil
            )
        )

    if ubicacion[
        "zona_prioritaria"
    ]:

        fortalezas.append(
            "Ubicación dentro de las zonas prioritarias."
        )

    if cargos:

        fortalezas.append(
            "El cargo coincide con el perfil."
        )

    fortalezas.append(
        "SEC Clase D en trámite."
    )

    brechas = []

    if (
        meses_solicitados is not None
        and meses_solicitados
        > PERFIL["experiencia_meses"]
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

        "plc_marcas_detectadas":
            marcas_plc,

        "experiencia_solicitada": {

            "anos":
                experiencia_detectada["anos"],

            "meses":
                experiencia_detectada["meses"]
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
# DESGLOSE PLC POR MARCA
#
# Analiza todas las ofertas y cuenta una vez por marca.
# ============================================================

def analizar_plc_por_marca(ofertas):

    contador = Counter()

    for oferta in ofertas:

        texto = texto_oferta(
            oferta
        )

        marcas = detectar_marcas_plc(
            texto
        )

        for marca in set(marcas):

            contador[marca] += 1

    return dict(
        contador.most_common()
    )


# ============================================================
# DESGLOSE ELECTROMECÁNICA
#
# Primero detecta las ofertas que realmente mencionan
# electromecánica/electromecánico.
#
# Después analiza las competencias solicitadas dentro
# de ese subconjunto.
# ============================================================

def analizar_electromecanica(ofertas):

    contador = Counter()

    ofertas_electromecanica = 0

    for oferta in ofertas:

        texto = texto_oferta(
            oferta
        )

        texto_normalizado = normalizar(
            texto
        )

        es_electromecanica = (
            "electromecanica" in texto_normalizado
            or "electromecanico" in texto_normalizado
        )

        if not es_electromecanica:

            continue

        ofertas_electromecanica += 1

        competencias = detectar_categorias(
            texto,
            ELECTROMECANICA_DESGLOSE
        )

        for competencia in set(
            competencias
        ):

            contador[
                competencia
            ] += 1

    return {

        "ofertas_electromecanica":
            ofertas_electromecanica,

        "competencias_dentro_electromecanica":
            dict(
                contador.most_common()
            )
    }


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

        texto = texto_oferta(
            oferta
        )

        # ----------------------------------------------------
        # COMPETENCIAS
        # ----------------------------------------------------

        competencias = detectar_categorias(
            texto,
            COMPETENCIAS
        )

        for competencia in set(
            competencias
        ):

            contador_competencias[
                competencia
            ] += 1

        # ----------------------------------------------------
        # TECNOLOGÍAS
        # ----------------------------------------------------

        tecnologias = detectar_categorias(
            texto,
            TECNOLOGIAS
        )

        for tecnologia in set(
            tecnologias
        ):

            contador_tecnologias[
                tecnologia
            ] += 1

        # ----------------------------------------------------
        # EXPERIENCIA
        # ----------------------------------------------------

        experiencia = detectar_experiencia(
            texto
        )

        meses = experiencia["meses"]

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
    # EXPERIENCIA PROMEDIO
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
    # NUEVOS ANÁLISIS
    # --------------------------------------------------------

    plc_por_marca = analizar_plc_por_marca(
        ofertas
    )

    desglose_electromecanica = (
        analizar_electromecanica(
            ofertas
        )
    )

    return {

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


# ============================================================
# PLAN DE DESARROLLO
# ============================================================

def generar_plan_desarrollo(mercado):

    plan = {}

    competencias_mercado = (
        mercado[
            "competencias_mas_solicitadas"
        ]
    )

    competencias_perfil = set(
        normalizar(x)
        for x in PERFIL["competencias"]
    )

    for competencia, cantidad in (
        competencias_mercado.items()
    ):

        if normalizar(
            competencia
        ) not in competencias_perfil:

            plan[competencia] = cantidad

    return dict(
        sorted(
            plan.items(),
            key=lambda x: x[1],
            reverse=True
        )
    )


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

    ofertas = historial.get(
        "ofertas",
        []
    )

    # ========================================================
    # 1. ANALIZAR CADA OFERTA
    # ========================================================

    for oferta in ofertas:

        oferta["analisis"] = (
            analizar_oferta(
                oferta
            )
        )

    # ========================================================
    # 2. ANALIZAR MERCADO
    # ========================================================

    mercado = analizar_mercado(
        ofertas
    )

    historial[
        "resumen_mercado"
    ] = mercado

    historial[
        "plan_desarrollo"
    ] = generar_plan_desarrollo(
        mercado
    )

    # ========================================================
    # 3. GUARDAR PERFIL
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

        "certificacion_electrica": {

            "tipo":
                PERFIL["certificacion"],

            "estado":
                PERFIL[
                    "certificacion_estado"
                ]
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
    # 4. GUARDAR
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
        mercado[
            "ofertas_analizadas"
        ]
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
    # TECNOLOGÍAS ESPECÍFICAS
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

    print(
        "Ofertas de electromecánica:",
        cantidad_electromecanica
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
            cantidad
        ) in enumerate(
            competencias_electromecanica.items(),
            start=1
        ):

            print(
                f"{i}. {nombre}: "
                f"{cantidad} ofertas"
            )

    else:

        print(
            "No se detectaron competencias dentro de electromecánica."
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

    for nombre, cantidad in (
        mercado[
            "ubicaciones_mas_repetidas"
        ].items()
    ):

        print(
            f"- {nombre}: "
            f"{cantidad} ofertas"
        )

    # ========================================================
    # PLAN DE DESARROLLO
    # ========================================================

    print()
    print("======================================")
    print("COMPETENCIAS A DESARROLLAR")
    print("======================================")

    plan = historial[
        "plan_desarrollo"
    ]

    if plan:

        for nombre, cantidad in (
            list(plan.items())[:10]
        ):

            print(
                f"- {nombre}: "
                f"{cantidad} ofertas"
            )

    else:

        print(
            "No se detectaron brechas."
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
                "recomendacion",
                ""
            )
        )

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

        marcas_plc = analisis.get(
            "plc_marcas_detectadas",
            []
        )

        if marcas_plc:

            print(
                "PLC:",
                ", ".join(
                    marcas_plc
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
