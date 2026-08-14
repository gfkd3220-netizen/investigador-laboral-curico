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
        "técnico eléctrico",
        "técnico de mantenimiento",
        "técnico en automatización",
        "ayudante eléctrico",
        "ayudante de mantenimiento",
        "técnico electromecánico",
        "técnico de instrumentación"
    ]
}


# ============================================================
# CONOCIMIENTOS ESPECÍFICOS
#
# Aquí NO buscamos solamente "PLC".
# Buscamos tecnologías y conocimientos concretos.
# ============================================================

CONOCIMIENTOS = {

    "PLC Siemens": [
        "plc siemens",
        "siemens plc"
    ],

    "S7-1200": [
        "s7-1200",
        "s7 1200"
    ],

    "S7-1500": [
        "s7-1500",
        "s7 1500"
    ],

    "S7-300": [
        "s7-300",
        "s7 300"
    ],

    "LOGO! Siemens": [
        "logo siemens",
        "siemens logo",
        "logo!"
    ],

    "TIA Portal": [
        "tia portal",
        "tia"
    ],

    "WinCC / HMI Siemens": [
        "wincc",
        "hmi siemens",
        "siemens hmi"
    ],

    "PLC Allen-Bradley": [
        "allen bradley",
        "allen-bradley",
        "rockwell automation"
    ],

    "Lectura de planos eléctricos": [
        "lectura de planos eléctricos",
        "lectura de planos electricos",
        "interpretación de planos eléctricos",
        "interpretacion de planos electricos",
        "planos eléctricos",
        "planos electricos"
    ],

    "Tableros eléctricos": [
        "tableros eléctricos",
        "tableros electricos",
        "tablero eléctrico",
        "tablero electrico",
        "armado de tableros"
    ],

    "Variadores de frecuencia": [
        "variador de frecuencia",
        "variadores de frecuencia",
        "vfd"
    ],

    "Variadores Siemens / SINAMICS": [
        "sinamics",
        "siemens sinamics",
        "g120",
        "g120c"
    ],

    "Motores eléctricos": [
        "motores eléctricos",
        "motores electricos",
        "motor eléctrico",
        "motor electrico"
    ],

    "Contactores y relés": [
        "contactores",
        "contactor",
        "relés",
        "reles",
        "relé",
        "rele"
    ],

    "Sensores": [
        "sensores",
        "sensor inductivo",
        "sensor capacitivo",
        "sensor fotoeléctrico",
        "sensor fotoelectrico"
    ],

    "Instrumentación 4-20 mA": [
        "4-20 ma",
        "4…20 ma",
        "4 a 20 ma"
    ],

    "Instrumentación industrial": [
        "instrumentación industrial",
        "instrumentacion industrial",
        "instrumentación",
        "instrumentacion"
    ],

    "Neumática": [
        "neumática",
        "neumatica",
        "circuitos neumáticos",
        "circuitos neumaticos"
    ],

    "Hidráulica": [
        "hidráulica",
        "hidraulica",
        "circuitos hidráulicos",
        "circuitos hidraulicos"
    ],

    "Mantenimiento preventivo": [
        "mantenimiento preventivo",
        "mantención preventiva"
    ],

    "Mantenimiento correctivo": [
        "mantenimiento correctivo",
        "mantención correctiva"
    ],

    "Diagnóstico de fallas": [
        "diagnóstico de fallas",
        "diagnostico de fallas",
        "detección de fallas",
        "deteccion de fallas",
        "troubleshooting"
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
# CONTAR CONOCIMIENTOS
#
# Devuelve cuántas veces aparece cada conocimiento.
# ============================================================

def detectar_conocimientos(texto):

    texto = normalizar(texto)

    resultados = {}

    for nombre, variantes in CONOCIMIENTOS.items():

        cantidad = 0

        for variante in variantes:

            variante = normalizar(variante)

            if variante:
                cantidad += texto.count(variante)

        if cantidad > 0:
            resultados[nombre] = cantidad

    return resultados


# ============================================================
# EXPERIENCIA
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

    ubicacion = normalizar(
        ubicacion
    )

    for zona in PERFIL["zonas"]:

        if normalizar(zona) in ubicacion:

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

        cargo = normalizar(cargo)

        palabras = cargo.split()

        coincidencias = 0

        for palabra in palabras:

            if len(palabra) >= 4 and palabra in titulo:
                coincidencias += 1

        if coincidencias >= 2:

            encontrados.append(cargo)

    return encontrados


# ============================================================
# EXPERIENCIA
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
#
# Es un número, no un porcentaje.
# ============================================================

def calcular_puntaje(
    conocimientos,
    experiencia,
    ubicacion,
    cargos
):

    puntaje = 0

    # Cada conocimiento encontrado suma 3 puntos.
    puntaje += len(conocimientos) * 3

    # Máximo por conocimientos: 45 puntos.
    puntaje = min(puntaje, 45)

    # Zona
    if ubicacion["zona_prioritaria"]:
        puntaje += 20

    # Cargo
    if cargos:
        puntaje += 20

    # Experiencia
    if experiencia == "cumple":
        puntaje += 15

    elif experiencia == "no_especificada":
        puntaje += 10

    elif experiencia == "brecha_pequena":
        puntaje += 5

    return min(puntaje, 100)


# ============================================================
# NIVEL
# ============================================================

def nivel(puntaje):

    if puntaje >= 75:
        return "ALTA"

    if puntaje >= 50:
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

    conocimientos = detectar_conocimientos(
        texto
    )

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
        conocimientos,
        ajuste_experiencia,
        ubicacion,
        cargos
    )

    if puntaje >= 75:
        recomendacion = "POSTULAR"

    elif puntaje >= 50:
        recomendacion = "EVALUAR"

    else:
        recomendacion = "BAJA PRIORIDAD"

    return {

        "conocimientos_detectados": conocimientos,

        "cantidad_conocimientos": len(
            conocimientos
        ),

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

            "recomendacion": recomendacion
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

        print("No se encontró historial.json")
        return

    ofertas = historial.get(
        "ofertas",
        []
    )

    for oferta in ofertas:

        oferta["analisis"] = analizar_oferta(
            oferta
        )

    historial["perfil"] = {
        "profesion": PERFIL["profesion"],
        "experiencia_meses": PERFIL["experiencia_meses"],
        "certificacion": PERFIL["certificacion"],
        "certificacion_estado": PERFIL["certificacion_estado"]
    }

    historial[
        "ultima_actualizacion"
    ] = "actualizado automáticamente"

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
    print("       ANÁLISIS DE OFERTAS")
    print("======================================")

    print(
        "Ofertas analizadas:",
        len(ofertas)
    )

    for oferta in ofertas:

        analisis = oferta["analisis"]

        compatibilidad = analisis[
            "compatibilidad"
        ]

        print()
        print("--------------------------------------")

        print(
            oferta.get(
                "titulo",
                "Sin título"
            )
        )

        print(
            "Puntaje:",
            compatibilidad["puntaje"],
            "/ 100"
        )

        print(
            "Nivel:",
            compatibilidad["nivel"]
        )

        print(
            "Recomendación:",
            compatibilidad["recomendacion"]
        )


        # ----------------------------------------------------
        # CONOCIMIENTOS ESPECÍFICOS
        # ----------------------------------------------------

        print()
        print("CONOCIMIENTOS DETECTADOS:")

        conocimientos = analisis[
            "conocimientos_detectados"
        ]

        if conocimientos:

            for nombre, cantidad in conocimientos.items():

                print(
                    " -",
                    nombre + ":",
                    cantidad
                )

        else:

            print(
                " - Ninguno"
            )


        print()
        print(
            "Total de categorías técnicas:",
            analisis["cantidad_conocimientos"]
        )


        # ----------------------------------------------------
        # EXPERIENCIA
        # ----------------------------------------------------

        experiencia = analisis[
            "experiencia_solicitada"
        ]

        if experiencia["anos"] is not None:

            print(
                "Experiencia solicitada:",
                experiencia["anos"],
                "años"
            )

        else:

            print(
                "Experiencia solicitada:",
                "No especificada"
            )

        print(
            "Experiencia del perfil:",
            PERFIL["experiencia_meses"],
            "meses"
        )


        # ----------------------------------------------------
        # UBICACIÓN
        # ----------------------------------------------------

        print(
            "Ubicación:",
            oferta.get(
                "ubicacion",
                ""
            )
        )

    print()
    print("======================================")


# ============================================================
# EJECUTAR
# ============================================================

if __name__ == "__main__":

    analizar_historial()
