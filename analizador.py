import json
import re


# ============================================================
# CONFIGURACIÓN
# ============================================================

ARCHIVO_HISTORIAL = "historial.json"


# ============================================================
# PERFIL
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
        "automatización",
        "control industrial",
        "variadores de frecuencia",
        "HMI",
        "motores eléctricos",
        "lectura de planos"
    ]
}


# ============================================================
# COMPETENCIAS PARA ANÁLISIS DE COMPATIBILIDAD
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

    "tableros eléctricos": [
        "tablero eléctrico",
        "tableros eléctricos",
        "tableros electricos"
    ],

    "PLC": [
        "plc",
        "controlador lógico programable"
    ],

    "automatización": [
        "automatización",
        "automatizacion"
    ],

    "control industrial": [
        "control industrial"
    ],

    "variadores de frecuencia": [
        "variador de frecuencia",
        "variadores de frecuencia",
        "vfd"
    ],

    "HMI": [
        "hmi"
    ],

    "motores eléctricos": [
        "motor eléctrico",
        "motores eléctricos",
        "motor electrico",
        "motores electricos"
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
    ]
}


# ============================================================
# TECNOLOGÍAS ESPECÍFICAS DEL MERCADO
#
# Cada oferta cuenta UNA SOLA VEZ por cada categoría.
# ============================================================

TECNOLOGIAS_MERCADO = {

    "PLC Siemens": [
        "siemens",
        "s7-1200",
        "s7 1200",
        "s7-1500",
        "s7 1500",
        "s7-300",
        "s7 300",
        "s7-400",
        "s7 400",
        "tia portal",
        "step 7"
    ],

    "PLC Allen-Bradley": [
        "allen-bradley",
        "allen bradley",
        "rockwell",
        "studio 5000",
        "controllogix",
        "compactlogix",
        "micrologix"
    ],

    "PLC Schneider": [
        "schneider",
        "schneider electric",
        "modicon",
        "unity pro",
        "control expert"
    ],

    "PLC Mitsubishi": [
        "mitsubishi",
        "melsec"
    ],

    "PLC Omron": [
        "omron"
    ],

    "PLC genérico": [
        "plc",
        "controlador lógico programable"
    ],

    "HMI": [
        "hmi",
        "interfaz hombre máquina",
        "interfaz hombre-maquina"
    ],

    "SCADA": [
        "scada"
    ],

    "TIA Portal": [
        "tia portal"
    ],

    "P&ID": [
        "p&id",
        "p & id",
        "piping and instrumentation",
        "diagramas de tuberias e instrumentacion",
        "diagramas de tuberías e instrumentación"
    ],

    "Lectura de planos eléctricos": [
        "lectura de planos eléctricos",
        "lectura de planos electricos",
        "interpretación de planos eléctricos",
        "interpretacion de planos electricos",
        "planos eléctricos",
        "planos electricos"
    ],

    "Variadores de frecuencia": [
        "variador de frecuencia",
        "variadores de frecuencia",
        "vfd",
        "drive"
    ],

    "Instrumentación": [
        "instrumentación",
        "instrumentacion",
        "instrumentista",
        "instrumentación industrial",
        "instrumentacion industrial"
    ],

    "Sensores": [
        "sensores",
        "sensor industrial",
        "sensores industriales"
    ],

    "Neumática": [
        "neumática",
        "neumatica",
        "neumático",
        "neumatico"
    ],

    "Hidráulica": [
        "hidráulica",
        "hidraulica",
        "hidráulico",
        "hidraulico"
    ],

    "Motores eléctricos": [
        "motores eléctricos",
        "motores electricos",
        "motor eléctrico",
        "motor electrico"
    ],

    "Diagnóstico de fallas": [
        "diagnóstico de fallas",
        "diagnostico de fallas",
        "detección de fallas",
        "deteccion de fallas",
        "troubleshooting"
    ],

    "Mantenimiento preventivo": [
        "mantenimiento preventivo",
        "mantención preventiva"
    ],

    "Mantenimiento correctivo": [
        "mantenimiento correctivo",
        "mantención correctiva"
    ],

    "Puesta en marcha": [
        "puesta en marcha",
        "puesta en servicio",
        "commissioning"
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
# DETECTAR COMPETENCIAS
# ============================================================

def detectar_competencias(texto):

    texto = normalizar(texto)

    encontradas = []

    for nombre, variantes in COMPETENCIAS.items():

        for variante in variantes:

            if normalizar(variante) in texto:

                encontradas.append(nombre)
                break

    return encontradas


# ============================================================
# ANALIZAR TECNOLOGÍAS DEL MERCADO
#
# Una oferta = máximo 1 aparición por categoría.
# ============================================================

def detectar_tecnologias(texto):

    texto = normalizar(texto)

    encontradas = []

    for tecnologia, variantes in TECNOLOGIAS_MERCADO.items():

        for variante in variantes:

            if normalizar(variante) in texto:

                encontradas.append(tecnologia)
                break

    return encontradas


# ============================================================
# CONTAR MERCADO
#
# Cada oferta cuenta una sola vez.
# ============================================================

def analizar_mercado(ofertas):

    conteos = {
        tecnologia: 0
        for tecnologia in TECNOLOGIAS_MERCADO
    }

    ofertas_analizadas = 0

    for oferta in ofertas:

        texto = " ".join([
            str(oferta.get("titulo", "")),
            str(oferta.get("descripcion", "")),
            str(oferta.get("requisitos", ""))
        ])

        tecnologias = detectar_tecnologias(texto)

        # Una oferta cuenta una sola vez
        # para cada tecnología encontrada.

        for tecnologia in set(tecnologias):

            conteos[tecnologia] += 1

        ofertas_analizadas += 1

    # Eliminar tecnologías que no aparecieron.

    conteos = {
        nombre: cantidad
        for nombre, cantidad in conteos.items()
        if cantidad > 0
    }

    # Ordenar de mayor a menor.

    conteos = dict(
        sorted(
            conteos.items(),
            key=lambda x: x[1],
            reverse=True
        )
    )

    return {
        "ofertas_analizadas": ofertas_analizadas,
        "tecnologias_mas_solicitadas": conteos
    }


# ============================================================
# DETECTAR EXPERIENCIA
# ============================================================

def detectar_experiencia(texto):

    texto = normalizar(texto)

    patron_anos = r'(\d+(?:[.,]\d+)?)\s*a(?:n|ñ)o(?:s)?'
    patron_meses = r'(\d+(?:[.,]\d+)?)\s*mes(?:es)?'

    anos = re.findall(
        patron_anos,
        texto
    )

    meses = re.findall(
        patron_meses,
        texto
    )

    anos = [
        float(x.replace(",", "."))
        for x in anos
    ]

    meses = [
        float(x.replace(",", "."))
        for x in meses
    ]

    if anos:

        solicitado = max(anos)

        return {
            "anos": solicitado,
            "meses": solicitado * 12
        }

    if meses:

        solicitado = max(meses)

        return {
            "anos": solicitado / 12,
            "meses": solicitado
        }

    if (
        "sin experiencia" in texto
        or "no requiere experiencia" in texto
        or "sin experiencia previa" in texto
    ):

        return {
            "anos": 0,
            "meses": 0
        }

    return {
        "anos": None,
        "meses": None
    }


# ============================================================
# UBICACIÓN
# ============================================================

def analizar_ubicacion(ubicacion):

    ubicacion_original = str(ubicacion)

    ubicacion_normalizada = normalizar(
        ubicacion_original
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

        cargo_normalizado = normalizar(cargo)

        palabras = cargo_normalizado.split()

        coincidencias = 0

        for palabra in palabras:

            if len(palabra) >= 4 and palabra in titulo:

                coincidencias += 1

        if coincidencias >= 2:

            encontrados.append(cargo)

    return encontrados


# ============================================================
# COMPARAR EXPERIENCIA
# ============================================================

def comparar_experiencia(meses_solicitados):

    meses_perfil = PERFIL["experiencia_meses"]

    if meses_solicitados is None:

        return "no_especificada"

    if meses_solicitados <= meses_perfil:

        return "cumple"

    diferencia = meses_solicitados - meses_perfil

    if diferencia <= 6:

        return "brecha_pequena"

    if diferencia <= 12:

        return "brecha_moderada"

    return "brecha_alta"


# ============================================================
# PUNTAJE
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
# ANALIZAR OFERTA
# ============================================================

def analizar_oferta(oferta):

    texto = " ".join([
        str(oferta.get("titulo", "")),
        str(oferta.get("descripcion", "")),
        str(oferta.get("requisitos", ""))
    ])

    competencias = detectar_competencias(texto)

    experiencia_detectada = detectar_experiencia(
        oferta.get("requisitos", "")
    )

    meses_solicitados = experiencia_detectada["meses"]

    ajuste_experiencia = comparar_experiencia(
        meses_solicitados
    )

    ubicacion = analizar_ubicacion(
        oferta.get("ubicacion", "")
    )

    cargos = detectar_cargo(
        oferta.get("titulo", "")
    )

    puntaje = calcular_puntaje(
        competencias,
        ajuste_experiencia,
        ubicacion,
        cargos
    )

    fortalezas = []

    if competencias:

        fortalezas.append(
            "Coincide con: "
            + ", ".join(competencias)
        )

    if ubicacion["zona_prioritaria"]:

        fortalezas.append(
            "La ubicación está dentro de las zonas prioritarias."
        )

    if cargos:

        fortalezas.append(
            "El cargo coincide con el perfil."
        )

    fortalezas.append(
        "SEC Clase D en trámite."
    )

    brechas = []

    if meses_solicitados is not None:

        if meses_solicitados > PERFIL["experiencia_meses"]:

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
            "EVALUAR Y POSTULAR SI LOS "
            "REQUISITOS NO SON EXCLUYENTES"
        )

    else:

        recomendacion = "PRIORIZAR OTRAS OFERTAS"

    return {

        "competencias_detectadas": competencias,

        "experiencia_solicitada": {
            "anos": experiencia_detectada["anos"],
            "meses": experiencia_detectada["meses"]
        },

        "experiencia_perfil": {
            "meses": PERFIL["experiencia_meses"],
            "anos": round(
                PERFIL["experiencia_meses"] / 12,
                2
            )
        },

        "ajuste_experiencia": ajuste_experiencia,

        "ubicacion": ubicacion,

        "cargos_coincidentes": cargos,

        "compatibilidad": {

            "puntaje": puntaje,

            "nivel": nivel(puntaje),

            "prioridad": prioridad(puntaje),

            "recomendacion": recomendacion,

            "fortalezas": fortalezas,

            "brechas": list(
                dict.fromkeys(brechas)
            )
        }
    }


# ============================================================
# PROCESAR HISTORIAL
# ============================================================

def analizar_historial():

    try:

        with open(
            ARCHIVO_HISTORIAL,
            "r",
            encoding="utf-8"
        ) as archivo:

            historial = json.load(archivo)

    except FileNotFoundError:

        print(
            "No se encontró historial.json"
        )

        return

    ofertas = historial.get(
        "ofertas",
        []
    )

    # --------------------------------------------------------
    # ANALIZAR CADA OFERTA
    # --------------------------------------------------------

    for oferta in ofertas:

        oferta["analisis"] = analizar_oferta(
            oferta
        )

    # --------------------------------------------------------
    # ANALIZAR MERCADO
    # --------------------------------------------------------

    mercado = analizar_mercado(
        ofertas
    )

    historial["resumen_mercado"] = mercado

    # --------------------------------------------------------
    # PERFIL
    # --------------------------------------------------------

    historial["perfil"] = {

        "profesion": PERFIL["profesion"],

        "experiencia_meses":
            PERFIL["experiencia_meses"],

        "certificacion":
            PERFIL["certificacion"],

        "certificacion_estado":
            PERFIL["certificacion_estado"]
    }

    historial[
        "ultima_actualizacion"
    ] = "actualizado automáticamente"

    # --------------------------------------------------------
    # GUARDAR
    # --------------------------------------------------------

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
    # MOSTRAR RESULTADO
    # ========================================================

    print()
    print(
        "======================================"
    )
    print(
        "       ANÁLISIS DE MERCADO"
    )
    print(
        "======================================"
    )

    print(
        "Ofertas analizadas:",
        mercado["ofertas_analizadas"]
    )

    print()
    print(
        "TECNOLOGÍAS MÁS SOLICITADAS"
    )

    print(
        "--------------------------------------"
    )

    if mercado[
        "tecnologias_mas_solicitadas"
    ]:

        for tecnologia, cantidad in mercado[
            "tecnologias_mas_solicitadas"
        ].items():

            print(
                f"{tecnologia}: {cantidad}"
            )

    else:

        print(
            "No se detectaron tecnologías."
        )

    print()
    print(
        "======================================"
    )

    # ========================================================
    # COMPATIBILIDAD
    # ========================================================

    print()
    print(
        "======================================"
    )
    print(
        "       COMPATIBILIDAD CON PERFIL"
    )
    print(
        "======================================"
    )

    for oferta in ofertas:

        analisis = oferta[
            "analisis"
        ]

        compatibilidad = analisis[
            "compatibilidad"
        ]

        print()
        print(
            oferta.get(
                "titulo",
                "Sin título"
            )
        )

        print(
            "Puntaje:",
            compatibilidad["puntaje"]
        )

        print(
            "Nivel:",
            compatibilidad["nivel"]
        )

        print(
            "Prioridad:",
            compatibilidad["prioridad"]
        )

        print(
            "Recomendación:",
            compatibilidad["recomendacion"]
        )

    print()
    print(
        "======================================"
    )


# ============================================================
# EJECUTAR
# ============================================================

if __name__ == "__main__":

    analizar_historial()
