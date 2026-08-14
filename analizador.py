import json
import re
from collections import Counter


# ============================================================
# CONFIGURACIÓN
# ============================================================

ARCHIVO_HISTORIAL = "historial.json"


# ============================================================
# PERFIL PROFESIONAL
# ============================================================

PERFIL = {
    "profesion": "Técnico en Automatización y Control Industrial",

    "certificacion_electrica": {
        "tipo": "SEC Clase D",
        "estado": "En trámite"
    },

    "experiencia": {
        "meses_aproximados": 6,
        "descripcion": (
            "Experiencia práctica como ayudante eléctrico en baja tensión, "
            "incluyendo canalizaciones, bandejas, cableado, canaletas, "
            "botones y conexiones de motores, instalación de luminarias "
            "UFO y LED, uso de herramientas eléctricas y apoyo en trabajos "
            "eléctricos."
        )
    },

    # --------------------------------------------------------
    # CONOCIMIENTOS PRÁCTICOS REALES
    # --------------------------------------------------------

    "competencias_practicas": [
        "electricidad industrial",
        "trabajos eléctricos en baja tensión",
        "canalizaciones",
        "bandejas eléctricas",
        "cableado",
        "canaletas",
        "instalación de luminarias",
        "luminarias led",
        "luminarias ufo",
        "motores eléctricos",
        "botones de motores",
        "herramientas eléctricas",
        "esmeril",
        "pinzas de corte",
        "instalaciones eléctricas"
    ],

    # --------------------------------------------------------
    # CONOCIMIENTOS ACADÉMICOS
    # --------------------------------------------------------

    "competencias_academicas": [
        "automatización",
        "control industrial",
        "PLC",
        "PLC Delta",
        "variadores de frecuencia",
        "HMI",
        "electricidad industrial",
        "tableros eléctricos",
        "motores eléctricos",
        "arranque directo",
        "estrella triángulo",
        "circuitos de fuerza",
        "circuitos de control",
        "lectura básica de planos",
        "control de motores",
        "instrumentación"
    ],

    # --------------------------------------------------------
    # CONOCIMIENTOS EN LOS QUE PUEDE AVANZAR RÁPIDAMENTE
    # --------------------------------------------------------

    "aprendizaje_rapido": [
        "PLC",
        "programación PLC",
        "HMI",
        "variadores de frecuencia",
        "automatización",
        "control industrial",
        "tableros eléctricos",
        "mantenimiento preventivo",
        "lectura de planos eléctricos",
        "sensores",
        "instrumentación básica",
        "SCADA"
    ],

    # --------------------------------------------------------
    # COMPETENCIAS QUE REQUIEREN ESPECIALMENTE PRÁCTICA
    # --------------------------------------------------------

    "requiere_practica": [
        "diagnóstico de fallas",
        "mantenimiento industrial",
        "mantenimiento correctivo",
        "mantenimiento preventivo en terreno",
        "instrumentación industrial",
        "conexionado de instrumentación",
        "puesta en marcha industrial",
        "diagnóstico de PLC en terreno",
        "diagnóstico de variadores en terreno",
        "diagnóstico de motores en terreno",
        "trabajo con tableros industriales reales"
    ],

    # --------------------------------------------------------
    # CARGOS OBJETIVO
    # --------------------------------------------------------

    "cargos_prioritarios": [
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

    # --------------------------------------------------------
    # ZONAS
    # --------------------------------------------------------

    "zonas_prioritarias": [
        "curico",
        "molina",
        "lontue",
        "talca",
        "linares"
    ]
}


# ============================================================
# COMPETENCIAS A DETECTAR
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

    "lectura de planos": [
        "lectura de planos",
        "interpretación de planos",
        "interpretacion de planos",
        "planos eléctricos",
        "planos electricos"
    ],

    "PLC": [
        "plc",
        "controlador lógico programable",
        "controlador programable"
    ],

    "variadores de frecuencia": [
        "variador de frecuencia",
        "variadores de frecuencia",
        "vfd",
        "drive"
    ],

    "automatización": [
        "automatización",
        "automatizacion",
        "control automático",
        "control automatico",
        "automatización industrial",
        "automatizacion industrial"
    ],

    "instrumentación": [
        "instrumentación",
        "instrumentacion",
        "instrumentista",
        "instrumentos industriales"
    ],

    "neumática": [
        "neumática",
        "neumatica",
        "sistemas neumáticos",
        "sistemas neumaticos"
    ],

    "hidráulica": [
        "hidráulica",
        "hidraulica",
        "sistemas hidráulicos",
        "sistemas hidraulicos"
    ],

    "diagnóstico de fallas": [
        "diagnóstico de fallas",
        "diagnostico de fallas",
        "detección de fallas",
        "deteccion de fallas",
        "resolución de fallas",
        "resolucion de fallas",
        "diagnostico de averias",
        "diagnóstico de averías"
    ],

    "HMI": [
        "hmi",
        "interfaz hombre máquina",
        "interfaz hombre maquina"
    ],

    "SCADA": [
        "scada"
    ],

    "sensores": [
        "sensores",
        "sensor industrial"
    ],

    "motores eléctricos": [
        "motor eléctrico",
        "motores eléctricos",
        "motor electrico",
        "motores electricos"
    ],

    "seguridad eléctrica": [
        "seguridad eléctrica",
        "seguridad electrica",
        "procedimientos eléctricos",
        "procedimientos electricos"
    ],

    "canalizaciones": [
        "canalización",
        "canalizaciones",
        "canaleta",
        "canaletas"
    ],

    "bandejas eléctricas": [
        "bandeja eléctrica",
        "bandejas eléctricas",
        "bandeja electrica",
        "bandejas electricas"
    ],

    "cableado": [
        "cableado",
        "cableados",
        "tendido de cables",
        "tendido de cable"
    ],

    "instalaciones eléctricas": [
        "instalaciones eléctricas",
        "instalacion electrica",
        "instalaciones electricas"
    ],

    "arranque directo": [
        "arranque directo",
        "partida directa"
    ],

    "estrella triángulo": [
        "estrella triángulo",
        "estrella triangulo",
        "estrella-triángulo",
        "estrella-triangulo"
    ]
}


# ============================================================
# PATRONES DE EXPERIENCIA
# ============================================================

PATRONES_EXPERIENCIA = [

    (r"(\d+(?:[.,]\d+)?)\s*años?\s*(?:de\s*)?experiencia", "años"),
    (r"(\d+(?:[.,]\d+)?)\s*año\s*experiencia", "años"),
    (r"(\d+(?:[.,]\d+)?)\s*mes(?:es)?\s*(?:de\s*)?experiencia", "meses"),

    (r"mínimo\s*(?:de\s*)?(\d+(?:[.,]\d+)?)\s*años?", "años"),
    (r"minimo\s*(?:de\s*)?(\d+(?:[.,]\d+)?)\s*años?", "años"),

    (r"al menos\s*(\d+(?:[.,]\d+)?)\s*años?", "años"),
    (r"más de\s*(\d+(?:[.,]\d+)?)\s*años?", "años"),
    (r"mas de\s*(\d+(?:[.,]\d+)?)\s*años?", "años")
]


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

    for original, nuevo in reemplazos.items():
        texto = texto.replace(original, nuevo)

    return texto


# ============================================================
# DETECTAR COMPETENCIAS
# ============================================================

def detectar_competencias(texto):

    texto_normalizado = normalizar(texto)

    encontradas = []

    for competencia, patrones in COMPETENCIAS.items():

        for patron in patrones:

            if normalizar(patron) in texto_normalizado:

                encontradas.append(competencia)
                break

    return encontradas


# ============================================================
# DETECTAR EXPERIENCIA SOLICITADA
# ============================================================

def detectar_experiencia(texto):

    texto_normalizado = normalizar(texto)

    experiencias = []

    for patron, unidad in PATRONES_EXPERIENCIA:

        coincidencias = re.findall(
            patron,
            texto_normalizado
        )

        for valor in coincidencias:

            try:
                numero = float(valor.replace(",", "."))

                if unidad == "años":
                    meses = numero * 12
                else:
                    meses = numero

                experiencias.append(meses)

            except ValueError:
                pass

    if not experiencias:
        return {
            "meses": None,
            "anos": None
        }

    meses = max(experiencias)

    return {
        "meses": meses,
        "anos": round(meses / 12, 2)
    }


# ============================================================
# DETECTAR SI NO REQUIERE EXPERIENCIA
# ============================================================

def no_requiere_experiencia(texto):

    texto = normalizar(texto)

    patrones = [
        "sin experiencia",
        "no requiere experiencia",
        "no se requiere experiencia",
        "sin requerir experiencia",
        "recién egresado",
        "recien egresado",
        "aceptamos recién egresados",
        "aceptamos recien egresados"
    ]

    return any(
        patron in texto
        for patron in patrones
    )


# ============================================================
# OBTENER EXPERIENCIA SOLICITADA
# ============================================================

def obtener_experiencia_solicitada(texto):

    if no_requiere_experiencia(texto):

        return {
            "meses": 0,
            "anos": 0,
            "requiere_experiencia": False
        }

    resultado = detectar_experiencia(texto)

    return {
        "meses": resultado["meses"],
        "anos": resultado["anos"],
        "requiere_experiencia": resultado["meses"] is not None
    }


# ============================================================
# ANALIZAR UBICACIÓN
# ============================================================

def analizar_ubicacion(ubicacion):

    ubicacion_normalizada = normalizar(ubicacion)

    for zona in PERFIL["zonas_prioritarias"]:

        if normalizar(zona) in ubicacion_normalizada:

            return {
                "ubicacion_oferta": ubicacion,
                "zona_prioritaria": True,
                "zona_coincidente": zona
            }

    return {
        "ubicacion_oferta": ubicacion,
        "zona_prioritaria": False,
        "zona_coincidente": None
    }


# ============================================================
# ANALIZAR CARGO
# ============================================================

def analizar_cargo(titulo):

    titulo_normalizado = normalizar(titulo)

    coincidencias = []

    for cargo in PERFIL["cargos_prioritarios"]:

        palabras = normalizar(cargo).split()

        palabras_importantes = [
            palabra
            for palabra in palabras
            if len(palabra) > 3
        ]

        coincidencias_palabras = sum(
            palabra in titulo_normalizado
            for palabra in palabras_importantes
        )

        if coincidencias_palabras >= max(
            1,
            len(palabras_importantes) // 2
        ):

            coincidencias.append(cargo)

    return coincidencias


# ============================================================
# CLASIFICAR CONOCIMIENTO
# ============================================================

def clasificar_conocimiento(competencia):

    competencia_normalizada = normalizar(competencia)

    practicas = [
        normalizar(x)
        for x in PERFIL["competencias_practicas"]
    ]

    academicas = [
        normalizar(x)
        for x in PERFIL["competencias_academicas"]
    ]

    aprendizaje = [
        normalizar(x)
        for x in PERFIL["aprendizaje_rapido"]
    ]

    practica_requerida = [
        normalizar(x)
        for x in PERFIL["requiere_practica"]
    ]

    if competencia_normalizada in practicas:
        return "practico"

    if competencia_normalizada in practica_requerida:
        return "requiere_practica"

    if competencia_normalizada in academicas:
        return "academico"

    if competencia_normalizada in aprendizaje:
        return "aprendizaje_rapido"

    return "no_confirmado"


# ============================================================
# MAPEAR COMPETENCIA DEL MERCADO AL PERFIL
# ============================================================

def clasificar_competencia_para_perfil(competencia):

    resultado = clasificar_conocimiento(competencia)

    # Algunas competencias son parte directa de conocimientos
    # prácticos aunque tengan diferentes nombres.

    equivalencias_practicas = {
        "electricidad industrial": "practico",
        "motores eléctricos": "practico",
        "canalizaciones": "practico",
        "bandejas eléctricas": "practico",
        "cableado": "practico",
        "instalaciones eléctricas": "practico"
    }

    if competencia in equivalencias_practicas:
        return equivalencias_practicas[competencia]

    equivalencias_academicas = {
        "PLC": "academico",
        "variadores de frecuencia": "academico",
        "HMI": "academico",
        "automatización": "academico",
        "arranque directo": "academico",
        "estrella triángulo": "academico",
        "lectura de planos": "academico"
    }

    if competencia in equivalencias_academicas:
        return equivalencias_academicas[competencia]

    equivalencias_practica_futura = {
        "mantenimiento industrial": "requiere_practica",
        "mantenimiento preventivo": "requiere_practica",
        "mantenimiento correctivo": "requiere_practica",
        "diagnóstico de fallas": "requiere_practica",
        "instrumentación": "requiere_practica"
    }

    if competencia in equivalencias_practica_futura:
        return equivalencias_practica_futura[competencia]

    return resultado


# ============================================================
# ANALIZAR COMPETENCIAS CONTRA EL PERFIL
# ============================================================

def analizar_ajuste_competencias(competencias):

    practicas = []
    academicas = []
    aprendizaje = []
    requieren_practica = []
    no_confirmadas = []

    for competencia in competencias:

        categoria = clasificar_competencia_para_perfil(
            competencia
        )

        if categoria == "practico":
            practicas.append(competencia)

        elif categoria == "academico":
            academicas.append(competencia)

        elif categoria == "aprendizaje_rapido":
            aprendizaje.append(competencia)

        elif categoria == "requiere_practica":
            requieren_practica.append(competencia)

        else:
            no_confirmadas.append(competencia)

    return {
        "conocimientos_practicos": practicas,
        "conocimientos_academicos": academicas,
        "aprendizaje_rapido": aprendizaje,
        "requieren_practica": requieren_practica,
        "no_confirmados": no_confirmadas
    }


# ============================================================
# CALCULAR COMPATIBILIDAD
# ============================================================

def calcular_compatibilidad(
    competencias,
    experiencia_solicitada,
    ubicacion,
    cargos_coincidentes
):

    experiencia_perfil_meses = PERFIL["experiencia"]["meses_aproximados"]

    clasificacion = analizar_ajuste_competencias(
        competencias
    )

    practicas = clasificacion["conocimientos_practicos"]
    academicas = clasificacion["conocimientos_academicos"]
    aprendizaje = clasificacion["aprendizaje_rapido"]
    requieren_practica = clasificacion["requieren_practica"]

    # --------------------------------------------------------
    # PUNTAJE BASE
    # --------------------------------------------------------

    puntaje = 35

    fortalezas = []
    brechas = []
    aprendizaje_rapido = []
    brechas_practicas = []

    # --------------------------------------------------------
    # FORMACIÓN
    # --------------------------------------------------------

    puntaje += 10

    fortalezas.append(
        "La formación técnica está relacionada con automatización, "
        "control industrial y electricidad."
    )

    # --------------------------------------------------------
    # SEC
    # --------------------------------------------------------

    fortalezas.append(
        "SEC Clase D: en trámite. La certificación todavía no "
        "se considera obtenida."
    )

    # --------------------------------------------------------
    # COMPETENCIAS PRÁCTICAS
    # --------------------------------------------------------

    for competencia in practicas:

        puntaje += 6

        fortalezas.append(
            f"Cuenta con experiencia práctica relacionada con "
            f"{competencia}."
        )

    # --------------------------------------------------------
    # CONOCIMIENTOS ACADÉMICOS
    # --------------------------------------------------------

    for competencia in academicas:

        puntaje += 2

    # --------------------------------------------------------
    # APRENDIZAJE RÁPIDO
    # --------------------------------------------------------

    for competencia in aprendizaje:

        aprendizaje_rapido.append(
            competencia
        )

    # --------------------------------------------------------
    # COMPETENCIAS QUE REQUIEREN TERRENO
    # --------------------------------------------------------

    for competencia in requieren_practica:

        brechas_practicas.append(
            competencia
        )

    # --------------------------------------------------------
    # EXPERIENCIA
    # --------------------------------------------------------

    meses_solicitados = experiencia_solicitada["meses"]

    if meses_solicitados is None:

        experiencia_ajuste = "no_especificada"

        fortalezas.append(
            "La oferta no especifica claramente una cantidad "
            "mínima de años de experiencia."
        )

        puntaje += 8

    elif meses_solicitados == 0:

        experiencia_ajuste = "sin_experiencia"

        fortalezas.append(
            "La oferta no exige experiencia previa."
        )

        puntaje += 12

    else:

        diferencia = meses_solicitados - experiencia_perfil_meses

        if diferencia <= 0:

            experiencia_ajuste = "cumple"

            fortalezas.append(
                "La experiencia disponible alcanza el mínimo "
                "indicado por la oferta."
            )

            puntaje += 15

        elif diferencia <= 6:

            experiencia_ajuste = "brecha_pequena"

            puntaje -= 5

            brechas.append(
                f"La oferta solicita aproximadamente "
                f"{round(meses_solicitados / 12, 1)} año(s) de experiencia; "
                f"el perfil registra aproximadamente "
                f"{experiencia_perfil_meses} meses."
            )

        elif diferencia <= 12:

            experiencia_ajuste = "brecha_moderada"

            puntaje -= 12

            brechas.append(
                f"La oferta solicita aproximadamente "
                f"{round(meses_solicitados / 12, 1)} año(s) de experiencia; "
                f"el perfil registra aproximadamente "
                f"{experiencia_perfil_meses} meses."
            )

        else:

            experiencia_ajuste = "brecha_grande"

            puntaje -= 22

            brechas.append(
                f"La oferta solicita aproximadamente "
                f"{round(meses_solicitados / 12, 1)} año(s) de experiencia; "
                f"el perfil registra aproximadamente "
                f"{experiencia_perfil_meses} meses."
            )

        if diferencia > 0:

            brechas_practicas.insert(
                0,
                "experiencia práctica acumulada en terreno"
            )

    # --------------------------------------------------------
    # UBICACIÓN
    # --------------------------------------------------------

    if ubicacion["zona_prioritaria"]:

        puntaje += 10

        fortalezas.append(
            f"La ubicación ({ubicacion['ubicacion_oferta']}) "
            f"está dentro de las zonas prioritarias."
        )

    else:

        puntaje -= 3

    # --------------------------------------------------------
    # CARGO
    # --------------------------------------------------------

    if cargos_coincidentes:

        puntaje += 8

        fortalezas.append(
            "El tipo de cargo coincide con uno o más cargos "
            "prioritarios del perfil."
        )

    # --------------------------------------------------------
    # LIMITAR PUNTAJE
    # --------------------------------------------------------

    puntaje = max(0, min(100, puntaje))

    # --------------------------------------------------------
    # CLASIFICACIÓN
    # --------------------------------------------------------

    if puntaje >= 75:

        probabilidad = "ALTA"

    elif puntaje >= 55:

        probabilidad = "MEDIA"

    else:

        probabilidad = "BAJA"

    # --------------------------------------------------------
    # PRIORIDAD
    # --------------------------------------------------------

    if puntaje >= 80:

        prioridad = "MUY ALTA"

    elif puntaje >= 70:

        prioridad = "ALTA"

    elif puntaje >= 55:

        prioridad = "MEDIA"

    elif puntaje >= 40:

        prioridad = "BAJA"

    else:

        prioridad = "MUY BAJA"

    # --------------------------------------------------------
    # RECOMENDACIÓN
    # --------------------------------------------------------

    if puntaje >= 80:

        recomendacion = "POSTULAR PRIORITARIAMENTE"

    elif puntaje >= 70:

        recomendacion = (
            "POSTULAR; EL PERFIL TIENE BUEN ENCAJE"
        )

    elif puntaje >= 55:

        recomendacion = (
            "POSTULAR SI LOS REQUISITOS NO SON EXCLUYENTES"
        )

    elif puntaje >= 40:

        recomendacion = (
            "POSTULAR SOLO SI EL CARGO ACEPTA PERFILES JUNIOR "
            "O EN DESARROLLO"
        )

    else:

        recomendacion = (
            "PRIORIZAR OTRAS OFERTAS CON MAYOR COMPATIBILIDAD"
        )

    # --------------------------------------------------------
    # MENSAJE ESPECIAL POR BRECHA PEQUEÑA
    # --------------------------------------------------------

    if experiencia_solicitada["meses"] is not None:

        diferencia = (
            experiencia_solicitada["meses"]
            - experiencia_perfil_meses
        )

        if 0 < diferencia <= 6:

            aprendizaje_rapido.insert(
                0,
                "La diferencia de experiencia es relativamente "
                "pequeña; conviene postular igualmente si el resto "
                "de los requisitos encaja."
            )

    return {
        "puntaje": puntaje,
        "probabilidad_ajuste": probabilidad,
        "prioridad_postulacion": prioridad,
        "recomendacion": recomendacion,

        "fortalezas": fortalezas,

        "conocimientos_practicos": practicas,

        "conocimientos_academicos": academicas,

        "conocimientos_relacionados": (
            practicas +
            academicas
        ),

        "brechas": brechas + requieren_practica,

        "aprendizaje_rapido": aprendizaje_rapido,

        "brechas_practicas": brechas_practicas,

        "experiencia": {
            "ajuste": experiencia_ajuste,
            "meses_perfil": experiencia_perfil_meses,
            "meses_solicitados": meses_solicitados
        }
    }


# ============================================================
# ANALIZAR UNA OFERTA
# ============================================================

def analizar_oferta(oferta):

    campos = [
        "titulo",
        "empresa",
        "ubicacion",
        "descripcion",
        "requisitos"
    ]

    texto = ""

    for campo in campos:

        valor = oferta.get(campo, "")

        if valor:

            texto += " " + str(valor)

    competencias = detectar_competencias(texto)

    experiencia_solicitada = obtener_experiencia_solicitada(
        texto
    )

    ubicacion = analizar_ubicacion(
        oferta.get("ubicacion", "")
    )

    cargos = analizar_cargo(
        oferta.get("titulo", "")
    )

    compatibilidad = calcular_compatibilidad(
        competencias,
        experiencia_solicitada,
        ubicacion,
        cargos
    )

    clasificacion = analizar_ajuste_competencias(
        competencias
    )

    return {

        "competencias_detectadas": competencias,

        "experiencia_detectada": (
            detectar_experiencia(texto)
        ),

        "anos_experiencia_solicitados":
            experiencia_solicitada["anos"],

        "experiencia_perfil": {
            "meses_aproximados":
                PERFIL["experiencia"]["meses_aproximados"],

            "anos_aproximados":
                round(
                    PERFIL["experiencia"]["meses_aproximados"]
                    / 12,
                    2
                )
        },

        "ubicacion": ubicacion,

        "cargos_coincidentes": cargos,

        "clasificacion_conocimientos": {

            "practicos": clasificacion[
                "conocimientos_practicos"
            ],

            "academicos": clasificacion[
                "conocimientos_academicos"
            ],

            "aprendizaje_rapido": clasificacion[
                "aprendizaje_rapido"
            ],

            "requieren_practica": clasificacion[
                "requieren_practica"
            ],

            "no_confirmados": clasificacion[
                "no_confirmados"
            ]
        },

        "compatibilidad": compatibilidad
    }


# ============================================================
# ANALIZAR TENDENCIAS
# ============================================================

def analizar_tendencias(ofertas):

    contador_competencias = Counter()
    contador_experiencia = Counter()
    contador_ubicaciones = Counter()
    contador_cargos = Counter()

    for oferta in ofertas:

        analisis = oferta.get("analisis", {})

        for competencia in analisis.get(
            "competencias_detectadas",
            []
        ):

            contador_competencias[
                competencia
            ] += 1

        experiencia = analisis.get(
            "anos_experiencia_solicitados"
        )

        if experiencia is not None:

            if experiencia == 0:

                clave = "sin experiencia"

            elif experiencia < 1:

                clave = "menos de 1 año"

            elif experiencia == 1:

                clave = "1 año"

            elif experiencia == 2:

                clave = "2 años"

            elif experiencia >= 3:

                clave = "3 años o más"

            else:

                clave = f"{experiencia} años"

            contador_experiencia[clave] += 1

        ubicacion = oferta.get(
            "ubicacion",
            ""
        )

        if ubicacion:

            contador_ubicaciones[
                ubicacion
            ] += 1

        titulo = oferta.get(
            "titulo",
            ""
        )

        if titulo:

            contador_cargos[
                titulo
            ] += 1

    return {

        "competencias": dict(
            contador_competencias.most_common()
        ),

        "experiencia_requerida": dict(
            contador_experiencia.most_common()
        ),

        "ubicaciones": dict(
            contador_ubicaciones.most_common()
        ),

        "cargos": dict(
            contador_cargos.most_common()
        )
    }


# ============================================================
# RESUMEN DEL MERCADO
# ============================================================

def generar_resumen_mercado(
    ofertas,
    tendencias
):

    total = len(ofertas)

    return {

        "ofertas_analizadas": total,

        "competencias_mas_solicitadas":
            tendencias["competencias"],

        "experiencia_mas_solicitada":
            tendencias["experiencia_requerida"],

        "ubicaciones_mas_repetidas":
            tendencias["ubicaciones"],

        "cargos_mas_repetidos":
            tendencias["cargos"]
    }


# ============================================================
# GENERAR PLAN DE DESARROLLO
# ============================================================

def generar_plan_desarrollo(ofertas):

    contador = Counter()

    for oferta in ofertas:

        analisis = oferta.get(
            "analisis",
            {}
        )

        compatibilidad = analisis.get(
            "compatibilidad",
            {}
        )

        for competencia in compatibilidad.get(
            "brechas_practicas",
            []
        ):

            contador[
                competencia
            ] += 1

        for competencia in compatibilidad.get(
            "aprendizaje_rapido",
            []
        ):

            if (
                competencia !=
                "La diferencia de experiencia es relativamente pequeña; "
                "conviene postular igualmente si el resto de los requisitos encaja."
            ):

                contador[
                    competencia
                ] += 1

    return dict(
        contador.most_common()
    )


# ============================================================
# ANALIZAR HISTORIAL COMPLETO
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

    ofertas_analizadas = 0

    for oferta in ofertas:

        resultado = analizar_oferta(
            oferta
        )

        oferta["analisis"] = resultado

        ofertas_analizadas += 1

    tendencias = analizar_tendencias(
        ofertas
    )

    historial["tendencias"] = tendencias

    historial["resumen_mercado"] = (
        generar_resumen_mercado(
            ofertas,
            tendencias
        )
    )

    historial["plan_desarrollo"] = (
        generar_plan_desarrollo(
            ofertas
        )
    )

    historial["perfil_analizado"] = {

        "profesion":
            PERFIL["profesion"],

        "experiencia_meses":
            PERFIL["experiencia"][
                "meses_aproximados"
            ],

        "certificacion_electrica":
            PERFIL[
                "certificacion_electrica"
            ],

        "objetivo":
            "Conseguir experiencia práctica en terreno "
            "y crecer hacia automatización y mantenimiento industrial."
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
    # MOSTRAR RESULTADOS
    # ========================================================

    print()
    print("=" * 60)
    print("ANÁLISIS LABORAL")
    print("=" * 60)

    print(
        f"Ofertas analizadas: {ofertas_analizadas}"
    )

    print(
        f"Experiencia del perfil: "
        f"{PERFIL['experiencia']['meses_aproximados']} meses"
    )

    print(
        "SEC Clase D: EN TRÁMITE"
    )

    print()
    print("COMPATIBILIDAD DE OFERTAS")
    print("-" * 60)

    for oferta in ofertas:

        analisis = oferta.get(
            "analisis",
            {}
        )

        compatibilidad = analisis.get(
            "compatibilidad",
            {}
        )

        print(
            f"\n{oferta.get('titulo', 'Sin título')}"
        )

        print(
            f"Puntaje: "
            f"{compatibilidad.get('puntaje', 0)}/100"
        )

        print(
            f"Ajuste: "
            f"{compatibilidad.get('probabilidad_ajuste', '')}"
        )

        print(
            f"Prioridad: "
            f"{compatibilidad.get('prioridad_postulacion', '')}"
        )

        print(
            f"Recomendación: "
            f"{compatibilidad.get('recomendacion', '')}"
        )

    print()
    print("COMPETENCIAS MÁS SOLICITADAS")
    print("-" * 60)

    for competencia, cantidad in (
        tendencias["competencias"].items()
    ):

        print(
            f"- {competencia}: "
            f"{cantidad} ofertas"
        )

    print()
    print("EXPERIENCIA SOLICITADA")
    print("-" * 60)

    for nivel, cantidad in (
        tendencias[
            "experiencia_requerida"
        ].items()
    ):

        print(
            f"- {nivel}: "
            f"{cantidad} ofertas"
        )

    print()
    print("PLAN DE DESARROLLO")
    print("-" * 60)

    plan = historial.get(
        "plan_desarrollo",
        {}
    )

    for competencia, cantidad in (
        plan.items()
    ):

        print(
            f"- {competencia}: "
            f"aparece como área de desarrollo "
            f"en {cantidad} análisis"
        )

    print()
    print("=" * 60)
    print("ANÁLISIS COMPLETADO")
    print("=" * 60)


# ============================================================
# EJECUTAR
# ============================================================

if __name__ == "__main__":

    analizar_historial()
