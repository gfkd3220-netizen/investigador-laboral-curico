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
# COMPETENCIAS ESPECÍFICAS DEL MERCADO
#
# Cada competencia se cuenta como MÁXIMO 1 vez por oferta.
#
# Ejemplo:
#
# Si una oferta menciona TIA Portal 10 veces:
# TIA Portal = 1
#
# Si menciona PLC Siemens y TIA Portal:
# PLC Siemens = 1
# TIA Portal = 1
#
# Esto permite saber cuántas OFERTAS distintas solicitan
# cada conocimiento.
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

    "diagnóstico de fallas": [
        "diagnóstico de fallas",
        "diagnostico de fallas",
        "detección de fallas",
        "deteccion de fallas",
        "troubleshooting"
    ],

    "tableros eléctricos": [
        "tablero eléctrico",
        "tableros eléctricos",
        "tablero electrico",
        "tableros electricos"
    ],

    "lectura de planos eléctricos": [
        "lectura de planos eléctricos",
        "lectura de planos electricos",
        "interpretación de planos eléctricos",
        "interpretacion de planos electricos",
        "planos eléctricos",
        "planos electricos"
    ],

    "PLC": [
        "plc",
        "controlador lógico programable",
        "controlador logico programable"
    ],

    "PLC Siemens": [
        "plc siemens",
        "siemens plc"
    ],

    "TIA Portal": [
        "tia portal"
    ],

    "S7-1200": [
        "s7-1200",
        "s7 1200"
    ],

    "S7-1500": [
        "s7-1500",
        "s7 1500"
    ],

    "LOGO! Siemens": [
        "logo! siemens",
        "logo siemens",
        "siemens logo"
    ],

    "HMI": [
        "hmi",
        "interfaz hombre maquina",
        "interfaz hombre-máquina"
    ],

    "SCADA": [
        "scada"
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

    "motores eléctricos": [
        "motor eléctrico",
        "motores eléctricos",
        "motor electrico",
        "motores electricos"
    ],

    "sensores": [
        "sensores",
        "sensor industrial",
        "sensores industriales"
    ],

    "instrumentación industrial": [
        "instrumentación industrial",
        "instrumentacion industrial"
    ],

    "neumática": [
        "neumática",
        "neumatica",
        "neumática industrial",
        "neumatica industrial"
    ],

    "hidráulica": [
        "hidráulica",
        "hidraulica",
        "hidráulica industrial",
        "hidraulica industrial"
    ],

    "puesta en marcha": [
        "puesta en marcha",
        "puesta en servicio",
        "comisionamiento"
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
#
# IMPORTANTE:
# Cada competencia aparece como máximo UNA vez.
# ============================================================

def detectar_competencias(texto):

    texto = normalizar(texto)

    encontradas = []

    for nombre, variantes in COMPETENCIAS.items():

        for variante in variantes:

            if normalizar(variante) in texto:

                encontradas.append(nombre)

                # Una vez encontrada la competencia,
                # no seguimos contando repeticiones.
                break

    return encontradas


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

    ubicacion_original = str(
        ubicacion
    )

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

        cargo_normalizado = normalizar(
            cargo
        )

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

def comparar_experiencia(
    meses_solicitados
):

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
# PUNTAJE
# ============================================================

def calcular_puntaje(
    competencias,
    experiencia,
    ubicacion,
    cargos
):

    puntaje = 0

    # Máximo 40 puntos por competencias.
    # Cada competencia encontrada cuenta una sola vez.

    for competencia in competencias:

        if competencia in PERFIL[
            "competencias"
        ]:

            puntaje += 8

    puntaje = min(
        puntaje,
        40
    )

    # Ubicación

    if ubicacion[
        "zona_prioritaria"
    ]:

        puntaje += 20

    # Cargo

    if cargos:

        puntaje += 20

    # Experiencia

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

    competencias = detectar_competencias(
        texto
    )

    experiencia_detectada = detectar_experiencia(
        oferta.get("requisitos", "")
    )

    meses_solicitados = (
        experiencia_detectada["meses"]
    )

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

    if ubicacion[
        "zona_prioritaria"
    ]:

        fortalezas.append(
            "La ubicación está dentro "
            "de las zonas prioritarias."
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

        if meses_solicitados > PERFIL[
            "experiencia_meses"
        ]:

            brechas.append(
                f"Solicita {meses_solicitados:g} meses "
                f"de experiencia y el perfil tiene "
                f"{PERFIL['experiencia_meses']} meses."
            )

    # ========================================================
    # COMPETENCIAS DE LA OFERTA QUE NO ESTÁN EN EL PERFIL
    # ========================================================

    for competencia in competencias:

        if competencia not in PERFIL[
            "competencias"
        ]:

            brechas.append(
                competencia
            )

    # ========================================================
    # RECOMENDACIÓN
    # ========================================================

    if puntaje >= 80:

        recomendacion = "POSTULAR"

    elif puntaje >= 60:

        recomendacion = (
            "EVALUAR Y POSTULAR SI LOS "
            "REQUISITOS NO SON EXCLUYENTES"
        )

    else:

        recomendacion = (
            "PRIORIZAR OTRAS OFERTAS"
        )

    return {

        "competencias_detectadas":
            competencias,

        "experiencia_solicitada": {

            "anos": (
                experiencia_detectada["anos"]
                if experiencia_detectada[
                    "anos"
                ] is not None
                else None
            ),

            "meses": (
                experiencia_detectada["meses"]
                if experiencia_detectada[
                    "meses"
                ] is not None
                else None
            )
        },

        "experiencia_perfil": {

            "meses":
                PERFIL[
                    "experiencia_meses"
                ],

            "anos":
                round(
                    PERFIL[
                        "experiencia_meses"
                    ] / 12,
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
# TENDENCIAS DEL MERCADO
#
# AQUÍ ESTÁ EL CAMBIO PRINCIPAL.
#
# Si una oferta menciona TIA Portal 20 veces,
# solamente suma 1 oferta para TIA Portal.
#
# Por ejemplo:
#
# TIA Portal: 35
# PLC Siemens: 28
# S7-1200: 17
#
# Significa que esas cantidades de OFERTAS distintas
# mencionaron cada conocimiento.
# ============================================================

def analizar_tendencias(ofertas):

    competencias = {}

    experiencia = {}

    ubicaciones = {}

    cargos = {}

    for oferta in ofertas:

        texto = " ".join([
            str(oferta.get("titulo", "")),
            str(oferta.get("descripcion", "")),
            str(oferta.get("requisitos", ""))
        ])

        # ----------------------------------------------------
        # COMPETENCIAS
        # ----------------------------------------------------

        competencias_oferta = detectar_competencias(
            texto
        )

        for competencia in competencias_oferta:

            competencias[competencia] = (
                competencias.get(
                    competencia,
                    0
                ) + 1
            )

        # ----------------------------------------------------
        # EXPERIENCIA
        # ----------------------------------------------------

        experiencia_detectada = detectar_experiencia(
            oferta.get("requisitos", "")
        )

        anos = experiencia_detectada[
            "anos"
        ]

        if anos is not None:

            clave = f"{anos:g} año(s)"

            experiencia[clave] = (
                experiencia.get(
                    clave,
                    0
                ) + 1
            )

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

            ubicaciones[ubicacion] = (
                ubicaciones.get(
                    ubicacion,
                    0
                ) + 1
            )

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

            cargos[titulo] = (
                cargos.get(
                    titulo,
                    0
                ) + 1
            )

    # Ordenar de mayor a menor

    competencias = dict(
        sorted(
            competencias.items(),
            key=lambda x: x[1],
            reverse=True
        )
    )

    experiencia = dict(
        sorted(
            experiencia.items(),
            key=lambda x: x[1],
            reverse=True
        )
    )

    ubicaciones = dict(
        sorted(
            ubicaciones.items(),
            key=lambda x: x[1],
            reverse=True
        )
    )

    cargos = dict(
        sorted(
            cargos.items(),
            key=lambda x: x[1],
            reverse=True
        )
    )

    return {

        "competencias":
            competencias,

        "experiencia_requerida":
            experiencia,

        "ubicaciones":
            ubicaciones,

        "cargos":
            cargos
    }


# ============================================================
# PLAN DE DESARROLLO
#
# Muestra solamente las competencias detectadas
# en el mercado que todavía no están en el perfil.
# ============================================================

def generar_plan_desarrollo(
    tendencias
):

    plan = {}

    for competencia, cantidad in tendencias[
        "competencias"
    ].items():

        if competencia not in PERFIL[
            "competencias"
        ]:

            plan[competencia] = cantidad

    return dict(
        sorted(
            plan.items(),
            key=lambda x: x[1],
            reverse=True
        )
    )


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

    # --------------------------------------------------------
    # ANALIZAR CADA OFERTA
    # --------------------------------------------------------

    for oferta in ofertas:

        oferta["analisis"] = analizar_oferta(
            oferta
        )

    # --------------------------------------------------------
    # ANALIZAR MERCADO COMPLETO
    # --------------------------------------------------------

    tendencias = analizar_tendencias(
        ofertas
    )

    plan_desarrollo = generar_plan_desarrollo(
        tendencias
    )

    # --------------------------------------------------------
    # GUARDAR PERFIL
    # --------------------------------------------------------

    historial["perfil"] = {

        "profesion":
            PERFIL["profesion"],

        "experiencia_meses":
            PERFIL["experiencia_meses"],

        "certificacion":
            PERFIL["certificacion"],

        "certificacion_estado":
            PERFIL[
                "certificacion_estado"
            ]
    }

    # --------------------------------------------------------
    # GUARDAR TENDENCIAS
    # --------------------------------------------------------

    historial["tendencias"] = tendencias

    # --------------------------------------------------------
    # RESUMEN DEL MERCADO
    # --------------------------------------------------------

    historial["resumen_mercado"] = {

        "ofertas_analizadas":
            len(ofertas),

        "competencias_mas_solicitadas":
            tendencias[
                "competencias"
            ],

        "experiencia_mas_solicitada":
            tendencias[
                "experiencia_requerida"
            ],

        "ubicaciones_mas_repetidas":
            tendencias[
                "ubicaciones"
            ],

        "cargos_mas_repetidos":
            tendencias[
                "cargos"
            ]
    }

    # --------------------------------------------------------
    # PLAN DE DESARROLLO
    # --------------------------------------------------------

    historial["plan_desarrollo"] = (
        plan_desarrollo
    )

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
        "       ANÁLISIS DE OFERTAS"
    )
    print(
        "======================================"
    )

    print(
        "Ofertas analizadas:",
        len(ofertas)
    )

    print()
    print(
        "========== MERCADO =========="
    )

    print()
    print(
        "COMPETENCIAS MÁS SOLICITADAS:"
    )

    if tendencias[
        "competencias"
    ]:

        for nombre, cantidad in tendencias[
            "competencias"
        ].items():

            print(
                f"  {nombre}: {cantidad} oferta(s)"
            )

    else:

        print(
            "  No se detectaron competencias."
        )

    print()
    print(
        "EXPERIENCIA SOLICITADA:"
    )

    for nombre, cantidad in tendencias[
        "experiencia_requerida"
    ].items():

        print(
            f"  {nombre}: {cantidad} oferta(s)"
        )

    print()
    print(
        "UBICACIONES:"
    )

    for nombre, cantidad in tendencias[
        "ubicaciones"
    ].items():

        print(
            f"  {nombre}: {cantidad} oferta(s)"
        )

    print()
    print(
        "CARGOS:"
    )

    for nombre, cantidad in tendencias[
        "cargos"
    ].items():

        print(
            f"  {nombre}: {cantidad} oferta(s)"
        )

    print()
    print(
        "========== PLAN DE DESARROLLO =========="
    )

    if plan_desarrollo:

        for nombre, cantidad in plan_desarrollo.items():

            print(
                f"  {nombre}: aparece en "
                f"{cantidad} oferta(s)"
            )

    else:

        print(
            "  No se detectaron brechas."
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
