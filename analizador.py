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
        "lectura de planos eléctricos"
    ]
}


# ============================================================
# COMPETENCIAS GENERALES DEL MERCADO
#
# IMPORTANTE:
#
# Cada oferta cuenta UNA SOLA VEZ por competencia.
#
# Ejemplo:
#
# Oferta A:
# "PLC, PLC, PLC Siemens..."
#
# Resultado:
# PLC = 1 oferta
#
# No importa cuántas veces aparezca dentro de la publicación.
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
        "tablero electrico",
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

    "lectura de planos eléctricos": [
        "lectura de planos eléctricos",
        "lectura de planos electricos",
        "interpretación de planos eléctricos",
        "interpretacion de planos electricos"
    ],

    "planos eléctricos": [
        "planos eléctricos",
        "planos electricos",
        "esquemas eléctricos",
        "esquemas electricos"
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
        "puesta en servicio"
    ],

    "seguridad eléctrica": [
        "seguridad eléctrica",
        "seguridad electrica"
    ],

    "instrumentación y control": [
        "instrumentación y control",
        "instrumentacion y control"
    ]
}


# ============================================================
# TECNOLOGÍAS ESPECÍFICAS
#
# Estas permiten saber EXACTAMENTE qué tecnología pide
# el mercado.
#
# Cada publicación cuenta UNA SOLA VEZ por tecnología.
#
# Ejemplo:
#
# Una oferta dice:
# "PLC Siemens S7-1200, TIA Portal y HMI Siemens"
#
# Cuenta:
#
# PLC                    = 1
# PLC Siemens            = 1
# S7-1200                = 1
# TIA Portal             = 1
# HMI Siemens            = 1
#
# ============================================================

TECNOLOGIAS = {

    # --------------------------------------------------------
    # SIEMENS
    # --------------------------------------------------------

    "PLC Siemens": [
        "plc siemens",
        "siemens plc",
        "siemens"
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

    "S7-400": [
        "s7-400",
        "s7 400"
    ],

    "LOGO! Siemens": [
        "logo siemens",
        "siemens logo",
        "logo!"
    ],

    "TIA Portal": [
        "tia portal"
    ],

    "WinCC": [
        "wincc"
    ],

    "HMI Siemens": [
        "hmi siemens",
        "siemens hmi"
    ],

    "SINAMICS": [
        "sinamics",
        "siemens sinamics"
    ],

    "G120": [
        "g120",
        "g120c"
    ],

    # --------------------------------------------------------
    # ALLEN-BRADLEY / ROCKWELL
    # --------------------------------------------------------

    "PLC Allen-Bradley": [
        "allen bradley",
        "allen-bradley",
        "rockwell automation"
    ],

    "ControlLogix": [
        "controllogix"
    ],

    "CompactLogix": [
        "compactlogix"
    ],

    "Studio 5000": [
        "studio 5000",
        "studio5000"
    ],

    # --------------------------------------------------------
    # SCHNEIDER
    # --------------------------------------------------------

    "PLC Schneider": [
        "plc schneider",
        "schneider electric"
    ],

    "Modicon": [
        "modicon"
    ],

    "EcoStruxure": [
        "ecostruxure"
    ],

    # --------------------------------------------------------
    # OMRON
    # --------------------------------------------------------

    "PLC Omron": [
        "plc omron",
        "omron plc"
    ],

    "Sysmac": [
        "sysmac"
    ],

    # --------------------------------------------------------
    # MITSUBISHI
    # --------------------------------------------------------

    "PLC Mitsubishi": [
        "plc mitsubishi",
        "mitsubishi plc"
    ],

    # --------------------------------------------------------
    # OTROS
    # --------------------------------------------------------

    "PLC Delta": [
        "plc delta",
        "delta plc"
    ],

    "Arduino": [
        "arduino"
    ],

    "Python": [
        "python"
    ],

    "AutoCAD": [
        "autocad"
    ],

    "EPLAN": [
        "eplan"
    ],

    "LabVIEW": [
        "labview"
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
# DETECTAR COMPETENCIAS
#
# Una oferta = máximo 1 aparición por competencia.
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
# DETECTAR TECNOLOGÍAS
#
# Una oferta = máximo 1 aparición por tecnología.
# ============================================================

def detectar_tecnologias(texto):

    texto = normalizar(texto)

    encontradas = []

    for nombre, variantes in TECNOLOGIAS.items():

        for variante in variantes:

            if normalizar(variante) in texto:

                encontradas.append(nombre)

                break

    return encontradas


# ============================================================
# DETECTAR EXPERIENCIA
# ============================================================

def detectar_experiencia(texto):

    texto = normalizar(texto)

    patron_anos = (
        r'(\d+(?:[.,]\d+)?)\s*'
        r'a(?:n|ñ)o(?:s)?'
    )

    patron_meses = (
        r'(\d+(?:[.,]\d+)?)\s*'
        r'mes(?:es)?'
    )

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

        palabras = normalizar(cargo).split()

        coincidencias = 0

        for palabra in palabras:

            if len(palabra) >= 4 and palabra in titulo:

                coincidencias += 1

        if coincidencias >= 2:

            encontrados.append(cargo)

    return encontrados


# ============================================================
# COMPARAR EXPERIENCIA CON EL PERFIL
# ============================================================

def comparar_experiencia(meses_solicitados):

    meses_perfil = PERFIL["experiencia_meses"]

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
#
# Esto sí depende de TU perfil.
# No afecta las estadísticas del mercado.
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

    competencias = detectar_competencias(
        texto
    )

    tecnologias = detectar_tecnologias(
        texto
    )

    experiencia_detectada = detectar_experiencia(
        oferta.get(
            "requisitos",
            ""
        )
        or texto
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

    fortalezas = []

    coincidencias_perfil = [
        competencia
        for competencia in competencias
        if competencia in PERFIL["competencias"]
    ]

    if coincidencias_perfil:

        fortalezas.append(
            "Coincide con: "
            + ", ".join(
                coincidencias_perfil
            )
        )

    if tecnologias:

        fortalezas.append(
            "Tecnologías detectadas: "
            + ", ".join(
                tecnologias
            )
        )

    if ubicacion["zona_prioritaria"]:

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

        "tecnologias_especificas":
            tecnologias,

        "experiencia_solicitada": {

            "anos":
                experiencia_detectada[
                    "anos"
                ],

            "meses":
                experiencia_detectada[
                    "meses"
                ]
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
# ANÁLISIS DEL MERCADO
#
# ESTA PARTE ES INDEPENDIENTE DEL PERFIL.
#
# Junior = 1 publicación
# Senior = 1 publicación
#
# Cada publicación cuenta máximo 1 vez por cada elemento.
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
        #
        # Una oferta = máximo 1.
        # ----------------------------------------------------

        competencias = detectar_competencias(
            texto
        )

        for competencia in set(
            competencias
        ):

            contador_competencias[
                competencia
            ] += 1

        # ----------------------------------------------------
        # TECNOLOGÍAS ESPECÍFICAS
        #
        # Una oferta = máximo 1.
        # ----------------------------------------------------

        tecnologias = detectar_tecnologias(
            texto
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
            oferta.get(
                "requisitos",
                ""
            )
            or texto
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
        #
        # Se usa el título real.
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

    # ========================================================
    # EXPERIENCIA
    # ========================================================

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

    # ========================================================
    # RESULTADOS
    #
    # SOLO CANTIDADES.
    # ========================================================

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
                contador_ubicaciones.most_common(
                    15
                )
            ),

        "cargos_mas_repetidos":
            dict(
                contador_cargos.most_common(
                    15
                )
            )
    }


# ============================================================
# PLAN DE DESARROLLO
#
# Muestra qué pide el mercado y que todavía no está
# registrado dentro de tu perfil.
# ============================================================

def generar_plan_desarrollo(
    mercado
):

    plan = {}

    # --------------------------------------------------------
    # COMPETENCIAS
    # --------------------------------------------------------

    competencias_perfil = set(
        normalizar(c)
        for c in PERFIL["competencias"]
    )

    for competencia, cantidad in (
        mercado[
            "competencias_mas_solicitadas"
        ].items()
    ):

        if normalizar(
            competencia
        ) not in competencias_perfil:

            plan[competencia] = cantidad

    # --------------------------------------------------------
    # TECNOLOGÍAS
    #
    # Las agregamos con el prefijo "TECNOLOGÍA:"
    # para diferenciarlas de competencias generales.
    # --------------------------------------------------------

    for tecnologia, cantidad in (
        mercado[
            "tecnologias_especificas"
        ].items()
    ):

        nombre = (
            "TECNOLOGÍA: "
            + tecnologia
        )

        plan[nombre] = cantidad

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
    # 2. ANALIZAR EL MERCADO
    # ========================================================

    mercado = analizar_mercado(
        ofertas
    )

    historial[
        "resumen_mercado"
    ] = mercado

    # ========================================================
    # 3. TENDENCIAS
    # ========================================================

    historial[
        "tendencias"
    ] = {

        "competencias":
            mercado[
                "competencias_mas_solicitadas"
            ],

        "tecnologias_especificas":
            mercado[
                "tecnologias_especificas"
            ],

        "experiencia_requerida":
            mercado[
                "experiencia_requerida"
            ],

        "ubicaciones":
            mercado[
                "ubicaciones_mas_repetidas"
            ],

        "cargos":
            mercado[
                "cargos_mas_repetidos"
            ]
    }

    # ========================================================
    # 4. PLAN DE DESARROLLO
    # ========================================================

    historial[
        "plan_desarrollo"
    ] = generar_plan_desarrollo(
        mercado
    )

    # ========================================================
    # 5. PERFIL
    # ========================================================

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
    ] = (
        "actualizado automáticamente"
    )

    # ========================================================
    # 6. GUARDAR
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
    # MOSTRAR RESULTADO
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

    for nombre, cantidad in list(
        mercado[
            "competencias_mas_solicitadas"
        ].items()
    )[:20]:

        print(
            f"- {nombre}: "
            f"{cantidad} ofertas"
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

        for nombre, cantidad in list(
            tecnologias.items()
        )[:30]:

            print(
                f"- {nombre}: "
                f"{cantidad} ofertas"
            )

    else:

        print(
            "No se detectaron tecnologías específicas."
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
    print("LO QUE EL MERCADO ESTÁ PIDIENDO")
    print("Y QUE NO ESTÁ EN TU PERFIL")
    print("======================================")

    plan = historial[
        "plan_desarrollo"
    ]

    if plan:

        for nombre, cantidad in list(
            plan.items()
        )[:20]:

            print(
                f"- {nombre}: "
                f"{cantidad} ofertas"
            )

    else:

        print(
            "No se detectaron elementos nuevos."
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
            "|",
            compatibilidad.get(
                "recomendacion",
                ""
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
