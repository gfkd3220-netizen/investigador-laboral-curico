import json
import re
from collections import Counter


# ============================================================
# CONFIGURACIÓN
# ============================================================

ARCHIVO_HISTORIAL = "historial.json"


# ============================================================
# PERFIL REAL DEL USUARIO
# ============================================================

PERFIL = {
    "profesion": "Técnico en Automatización y Control Industrial",

    "experiencia_meses": 6,

    "certificacion_electrica": {
        "tipo": "SEC Clase D",
        "estado": "En trámite"
    },

    "zona_prioritaria": [
        "Curicó",
        "Molina",
        "Lontué",
        "Talca",
        "Linares"
    ],

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

    # ========================================================
    # EXPERIENCIA PRÁCTICA REAL
    # ========================================================

    "conocimientos_practicos": [
        "electricidad industrial",
        "cableado",
        "canalizaciones",
        "bandejas portacables",
        "canaletas",
        "cableado eléctrico",
        "instalación de luminarias",
        "lámparas UFO",
        "luminarias LED",
        "botones de motores",
        "motores eléctricos",
        "herramientas eléctricas",
        "esmeril",
        "pinzas",
        "corte de conductores",
        "trabajo eléctrico en baja tensión"
    ],

    # ========================================================
    # CONOCIMIENTOS ACADÉMICOS
    # ========================================================

    "conocimientos_academicos": [
        "electricidad industrial",
        "automatización",
        "control industrial",
        "PLC",
        "PLC Delta",
        "variadores de frecuencia",
        "HMI",
        "arranque directo",
        "estrella triángulo",
        "circuitos de control",
        "circuitos de fuerza",
        "lectura básica de planos",
        "tableros eléctricos"
    ],

    # ========================================================
    # CONOCIMIENTOS QUE PUEDEN REFORZARSE RÁPIDAMENTE
    # ========================================================

    "aprendizaje_rapido": [
        "PLC",
        "HMI",
        "variadores de frecuencia",
        "automatización",
        "control industrial",
        "lectura de planos",
        "tableros eléctricos",
        "mantenimiento preventivo",
        "instrumentación básica",
        "sensores"
    ],

    # ========================================================
    # ÁREAS QUE REQUIEREN EXPERIENCIA PRÁCTICA
    # ========================================================

    "requieren_practica": [
        "mantenimiento industrial",
        "mantenimiento preventivo",
        "mantenimiento correctivo",
        "diagnóstico de fallas",
        "diagnóstico eléctrico",
        "detección de fallas",
        "instrumentación industrial",
        "puesta en marcha",
        "troubleshooting",
        "intervención de maquinaria industrial"
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
        "mantención industrial",
        "mantenimiento",
        "mantención"
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
        "control industrial"
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
        "troubleshooting"
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
        "sensor industrial",
        "sensor"
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

    "puesta en marcha": [
        "puesta en marcha",
        "puesta en servicio",
        "commissioning"
    ]
}


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

    for original, nuevo in reemplazos.items():
        texto = texto.replace(original, nuevo)

    return texto


# ============================================================
# EXTRAER AÑOS / MESES DE EXPERIENCIA
# ============================================================

def extraer_experiencia(texto):

    texto = normalizar(texto)

    candidatos_meses = []
    candidatos_anos = []

    patrones_meses = [
        r'(\d+(?:[.,]\d+)?)\s*mes(?:es)?\s*(?:de\s*)?(?:experiencia)?',
        r'experiencia\s*(?:de\s*)?(\d+(?:[.,]\d+)?)\s*mes(?:es)?'
    ]

    patrones_anos = [
        r'(\d+(?:[.,]\d+)?)\s*a(?:ñ|n)o(?:s)?\s*(?:de\s*)?(?:experiencia)?',
        r'experiencia\s*(?:de\s*)?(\d+(?:[.,]\d+)?)\s*a(?:ñ|n)o(?:s)?'
    ]

    for patron in patrones_meses:

        for coincidencia in re.findall(patron, texto):

            try:
                candidatos_meses.append(
                    float(coincidencia.replace(",", "."))
                )
            except ValueError:
                pass

    for patron in patrones_anos:

        for coincidencia in re.findall(patron, texto):

            try:
                candidatos_anos.append(
                    float(coincidencia.replace(",", "."))
                )
            except ValueError:
                pass

    # --------------------------------------------------------
    # También detectamos "un año", "dos años", etc.
    # --------------------------------------------------------

    palabras_anos = {
        "un ano": 1,
        "dos anos": 2,
        "tres anos": 3,
        "cuatro anos": 4,
        "cinco anos": 5
    }

    for expresion, cantidad in palabras_anos.items():

        if expresion in texto:
            candidatos_anos.append(cantidad)

    meses = max(candidatos_meses) if candidatos_meses else None
    anos = max(candidatos_anos) if candidatos_anos else None

    return {
        "meses": meses,
        "anos": anos
    }


# ============================================================
# DETECTAR EXPERIENCIA NO REQUERIDA
# ============================================================

def experiencia_no_requerida(texto):

    texto = normalizar(texto)

    patrones = [
        "sin experiencia",
        "no requiere experiencia",
        "no se requiere experiencia",
        "sin requerir experiencia",
        "recien egresado",
        "recién egresado",
        "acepta recien egresados",
        "acepta recien egresado",
        "sin experiencia previa"
    ]

    return any(patron in texto for patron in patrones)


# ============================================================
# DETECTAR COMPETENCIAS
# ============================================================

def detectar_competencias(texto):

    texto_normalizado = normalizar(texto)

    encontradas = []

    for competencia, palabras in COMPETENCIAS.items():

        for palabra in palabras:

            if normalizar(palabra) in texto_normalizado:

                encontradas.append(competencia)
                break

    return encontradas


# ============================================================
# CLASIFICAR CONOCIMIENTOS
# ============================================================

def clasificar_conocimientos(competencias):

    practicos = []
    academicos = []
    aprendizaje = []
    requieren_practica = []
    no_confirmados = []

    practicos_norm = [
        normalizar(x)
        for x in PERFIL["conocimientos_practicos"]
    ]

    academicos_norm = [
        normalizar(x)
        for x in PERFIL["conocimientos_academicos"]
    ]

    aprendizaje_norm = [
        normalizar(x)
        for x in PERFIL["aprendizaje_rapido"]
    ]

    practica_norm = [
        normalizar(x)
        for x in PERFIL["requieren_practica"]
    ]

    for competencia in competencias:

        competencia_norm = normalizar(competencia)

        # Primero manda la experiencia práctica.
        if competencia_norm in practicos_norm:

            practicos.append(competencia)
            continue

        # Luego conocimiento académico.
        if competencia_norm in academicos_norm:

            academicos.append(competencia)

        # Luego capacidad de aprendizaje.
        if competencia_norm in aprendizaje_norm:

            aprendizaje.append(competencia)

        # Finalmente competencias que requieren práctica.
        if competencia_norm in practica_norm:

            requieren_practica.append(competencia)

        # Si no tenemos evidencia suficiente.
        if (
            competencia_norm not in practicos_norm
            and competencia_norm not in academicos_norm
            and competencia_norm not in aprendizaje_norm
            and competencia_norm not in practica_norm
        ):

            no_confirmados.append(competencia)

    return {
        "practicos": practicos,
        "academicos": academicos,
        "aprendizaje_rapido": aprendizaje,
        "requieren_practica": requieren_practica,
        "no_confirmados": no_confirmados
    }


# ============================================================
# UBICACIÓN
# ============================================================

def analizar_ubicacion(ubicacion):

    ubicacion_original = str(ubicacion).strip()

    ubicacion_normalizada = normalizar(ubicacion_original)

    for zona in PERFIL["zona_prioritaria"]:

        if normalizar(zona) in ubicacion_normalizada:

            return {
                "ubicacion_oferta": ubicacion_original,
                "zona_prioritaria": True,
                "zona_coincidente": normalizar(zona)
            }

    return {
        "ubicacion_oferta": ubicacion_original,
        "zona_prioritaria": False,
        "zona_coincidente": None
    }


# ============================================================
# CARGOS COINCIDENTES
# ============================================================

def detectar_cargos(titulo):

    titulo_normalizado = normalizar(titulo)

    encontrados = []

    for cargo in PERFIL["cargos_prioritarios"]:

        cargo_normalizado = normalizar(cargo)

        # Comparación flexible por palabras relevantes.
        palabras = [
            palabra
            for palabra in cargo_normalizado.split()
            if len(palabra) >= 4
        ]

        coincidencias = sum(
            1
            for palabra in palabras
            if palabra in titulo_normalizado
        )

        if coincidencias >= max(1, len(palabras) // 2):

            encontrados.append(cargo)

    return encontrados


# ============================================================
# CALCULAR AJUSTE DE EXPERIENCIA
# ============================================================

def calcular_ajuste_experiencia(experiencia_solicitada, sin_experiencia):

    experiencia_usuario = PERFIL["experiencia_meses"]

    if sin_experiencia:

        return {
            "ajuste": "favorable",
            "meses_perfil": experiencia_usuario,
            "meses_solicitados": 0,
            "diferencia_meses": experiencia_usuario
        }

    if experiencia_solicitada is None:

        return {
            "ajuste": "no_especificada",
            "meses_perfil": experiencia_usuario,
            "meses_solicitados": None,
            "diferencia_meses": None
        }

    diferencia = experiencia_solicitada - experiencia_usuario

    if diferencia <= 0:

        ajuste = "cumple"

    elif diferencia <= 6:

        ajuste = "brecha_pequena"

    elif diferencia <= 12:

        ajuste = "brecha_moderada"

    elif diferencia <= 24:

        ajuste = "brecha_alta"

    else:

        ajuste = "brecha_muy_alta"

    return {
        "ajuste": ajuste,
        "meses_perfil": experiencia_usuario,
        "meses_solicitados": experiencia_solicitada,
        "diferencia_meses": diferencia
    }


# ============================================================
# CALCULAR PUNTAJE
# ============================================================

def calcular_puntaje(
    titulo,
    competencias,
    clasificacion,
    experiencia,
    ubicacion,
    cargos
):

    puntaje = 0

    # --------------------------------------------------------
    # FORMACIÓN
    # --------------------------------------------------------

    titulo_norm = normalizar(titulo)

    palabras_formacion = [
        "tecnico",
        "automatizacion",
        "electrico",
        "electricidad",
        "mantenimiento",
        "electromecanico",
        "instrumentacion"
    ]

    coincidencias_formacion = sum(
        1
        for palabra in palabras_formacion
        if palabra in titulo_norm
    )

    if coincidencias_formacion >= 2:

        puntaje += 20

    elif coincidencias_formacion == 1:

        puntaje += 15

    # --------------------------------------------------------
    # CONOCIMIENTOS PRÁCTICOS
    # --------------------------------------------------------

    puntaje += min(
        len(clasificacion["practicos"]) * 10,
        30
    )

    # --------------------------------------------------------
    # CONOCIMIENTOS ACADÉMICOS
    # --------------------------------------------------------

    puntaje += min(
        len(clasificacion["academicos"]) * 5,
        15
    )

    # --------------------------------------------------------
    # APRENDIZAJE RÁPIDO
    # --------------------------------------------------------

    puntaje += min(
        len(clasificacion["aprendizaje_rapido"]) * 3,
        9
    )

    # --------------------------------------------------------
    # UBICACIÓN
    # --------------------------------------------------------

    if ubicacion["zona_prioritaria"]:

        puntaje += 10

    # --------------------------------------------------------
    # CARGO
    # --------------------------------------------------------

    if cargos:

        puntaje += 10

    # --------------------------------------------------------
    # PENALIZACIÓN POR EXPERIENCIA
    # --------------------------------------------------------

    ajuste = experiencia["ajuste"]

    if ajuste == "cumple":

        puntaje += 5

    elif ajuste == "brecha_pequena":

        puntaje -= 5

    elif ajuste == "brecha_moderada":

        puntaje -= 10

    elif ajuste == "brecha_alta":

        puntaje -= 20

    elif ajuste == "brecha_muy_alta":

        puntaje -= 30

    puntaje = max(0, min(100, puntaje))

    return puntaje


# ============================================================
# PROBABILIDAD
# ============================================================

def determinar_probabilidad(puntaje):

    if puntaje >= 80:

        return "ALTA"

    if puntaje >= 60:

        return "MEDIA"

    return "BAJA"


# ============================================================
# PRIORIDAD DE POSTULACIÓN
# ============================================================

def determinar_prioridad(
    puntaje,
    experiencia,
    ubicacion,
    cargos
):

    ajuste = experiencia["ajuste"]

    if (
        puntaje >= 85
        and ajuste in ["cumple", "favorable", "no_especificada", "brecha_pequena"]
    ):

        return "MUY ALTA"

    if (
        puntaje >= 75
        and ajuste != "brecha_muy_alta"
    ):

        return "ALTA"

    if (
        puntaje >= 60
        and ajuste not in ["brecha_alta", "brecha_muy_alta"]
    ):

        return "MEDIA-ALTA"

    if puntaje >= 45:

        return "MEDIA"

    return "BAJA"


# ============================================================
# RECOMENDACIÓN
# ============================================================

def generar_recomendacion(
    prioridad,
    experiencia,
    competencias,
    clasificacion
):

    ajuste = experiencia["ajuste"]

    if prioridad == "MUY ALTA":

        return "POSTULAR PRIORITARIAMENTE"

    if prioridad == "ALTA":

        return "POSTULAR"

    if prioridad == "MEDIA-ALTA":

        return "POSTULAR SI EL CARGO ACEPTA PERFILES JUNIOR O EN DESARROLLO"

    if prioridad == "MEDIA":

        if ajuste in ["brecha_pequena", "no_especificada"]:

            return "POSTULAR SI LOS REQUISITOS NO SON EXCLUYENTES"

        return "POSTULAR COMO OPCIÓN SECUNDARIA"

    return "PRIORIZAR OTRAS OFERTAS CON MAYOR COMPATIBILIDAD"


# ============================================================
# GENERAR FORTALEZAS
# ============================================================

def generar_fortalezas(
    clasificacion,
    ubicacion,
    cargos,
    experiencia
):

    fortalezas = []

    fortalezas.append(
        "La formación técnica está relacionada con automatización, control industrial y electricidad."
    )

    fortalezas.append(
        "SEC Clase D: en trámite. La certificación todavía no se considera obtenida."
    )

    if clasificacion["practicos"]:

        fortalezas.append(
            "Cuenta con experiencia práctica relacionada con "
            + ", ".join(clasificacion["practicos"]) + "."
        )

    if clasificacion["academicos"]:

        fortalezas.append(
            "Cuenta con conocimientos académicos relacionados con "
            + ", ".join(clasificacion["academicos"]) + "."
        )

    if ubicacion["zona_prioritaria"]:

        fortalezas.append(
            f"La ubicación ({ubicacion['ubicacion_oferta']}) está dentro de las zonas prioritarias."
        )

    if cargos:

        fortalezas.append(
            "El tipo de cargo coincide con uno o más cargos prioritarios del perfil."
        )

    if experiencia["ajuste"] == "no_especificada":

        fortalezas.append(
            "La oferta no especifica claramente una cantidad mínima de experiencia."
        )

    return fortalezas


# ============================================================
# GENERAR BRECHAS
# ============================================================

def generar_brechas(
    competencias,
    clasificacion,
    experiencia
):

    brechas = []

    if experiencia["ajuste"] in [
        "brecha_pequena",
        "brecha_moderada",
        "brecha_alta",
        "brecha_muy_alta"
    ]:

        meses_solicitados = experiencia["meses_solicitados"]

        if meses_solicitados is not None:

            anos = meses_solicitados / 12

            if anos.is_integer():

                anos_texto = str(int(anos))

            else:

                anos_texto = f"{anos:.1f}"

            brechas.append(
                f"La oferta solicita aproximadamente {anos_texto} año(s) "
                f"de experiencia; el perfil registra aproximadamente "
                f"{experiencia['meses_perfil']} meses."
            )

    brechas.extend(
        clasificacion["requieren_practica"]
    )

    return list(dict.fromkeys(brechas))


# ============================================================
# GENERAR APRENDIZAJE RÁPIDO
# ============================================================

def generar_aprendizaje_rapido(
    clasificacion,
    experiencia
):

    resultados = list(
        clasificacion["aprendizaje_rapido"]
    )

    if experiencia["ajuste"] == "brecha_pequena":

        resultados.insert(
            0,
            "La diferencia de experiencia no es demasiado grande; "
            "conviene postular igualmente si el resto de los requisitos encaja."
        )

    return resultados


# ============================================================
# ANALIZAR OFERTA
# ============================================================

def analizar_oferta(oferta):

    texto = ""

    for campo in [
        "titulo",
        "empresa",
        "ubicacion",
        "descripcion",
        "requisitos"
    ]:

        valor = oferta.get(campo, "")

        if valor:

            texto += " " + str(valor)

    competencias = detectar_competencias(texto)

    experiencia_detectada = extraer_experiencia(texto)

    sin_experiencia = experiencia_no_requerida(texto)

    # --------------------------------------------------------
    # PRIORIDAD: si dice sin experiencia, usamos 0 meses.
    # --------------------------------------------------------

    if sin_experiencia:

        meses_solicitados = 0

    elif experiencia_detectada["meses"] is not None:

        meses_solicitados = experiencia_detectada["meses"]

    elif experiencia_detectada["anos"] is not None:

        meses_solicitados = experiencia_detectada["anos"] * 12

    else:

        meses_solicitados = None

    experiencia = calcular_ajuste_experiencia(
        meses_solicitados,
        sin_experiencia
    )

    ubicacion = analizar_ubicacion(
        oferta.get("ubicacion", "")
    )

    cargos = detectar_cargos(
        oferta.get("titulo", "")
    )

    clasificacion = clasificar_conocimientos(
        competencias
    )

    puntaje = calcular_puntaje(
        oferta.get("titulo", ""),
        competencias,
        clasificacion,
        experiencia,
        ubicacion,
        cargos
    )

    probabilidad = determinar_probabilidad(
        puntaje
    )

    prioridad = determinar_prioridad(
        puntaje,
        experiencia,
        ubicacion,
        cargos
    )

    recomendacion = generar_recomendacion(
        prioridad,
        experiencia,
        competencias,
        clasificacion
    )

    fortalezas = generar_fortalezas(
        clasificacion,
        ubicacion,
        cargos,
        experiencia
    )

    brechas = generar_brechas(
        competencias,
        clasificacion,
        experiencia
    )

    aprendizaje = generar_aprendizaje_rapido(
        clasificacion,
        experiencia
    )

    return {

        "competencias_detectadas": competencias,

        "experiencia_detectada": {
            "meses": experiencia_detectada["meses"],
            "anos": experiencia_detectada["anos"]
        },

        "anos_experiencia_solicitados": (
            meses_solicitados / 12
            if meses_solicitados is not None
            else None
        ),

        "experiencia_perfil": {
            "meses_aproximados": PERFIL["experiencia_meses"],
            "anos_aproximados": round(
                PERFIL["experiencia_meses"] / 12,
                2
            )
        },

        "ubicacion": ubicacion,

        "cargos_coincidentes": cargos,

        "clasificacion_conocimientos": clasificacion,

        "compatibilidad": {

            "puntaje": puntaje,

            "probabilidad_ajuste": probabilidad,

            "prioridad_postulacion": prioridad,

            "recomendacion": recomendacion,

            "fortalezas": fortalezas,

            "conocimientos_practicos": (
                clasificacion["practicos"]
            ),

            "conocimientos_academicos": (
                clasificacion["academicos"]
            ),

            "conocimientos_relacionados": (
                clasificacion["practicos"]
                + clasificacion["academicos"]
                + clasificacion["aprendizaje_rapido"]
            ),

            "brechas": brechas,

            "aprendizaje_rapido": aprendizaje,

            "brechas_practicas": (
                clasificacion["requieren_practica"]
            ),

            "experiencia": {
                "ajuste": experiencia["ajuste"],
                "meses_perfil": experiencia["meses_perfil"],
                "meses_solicitados": experiencia["meses_solicitados"],
                "diferencia_meses": experiencia["diferencia_meses"]
            }
        }
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

            contador_competencias[competencia] += 1

        experiencia = analisis.get(
            "experiencia_detectada",
            {}
        )

        if experiencia.get("anos") is not None:

            anos = experiencia["anos"]

            if float(anos).is_integer():

                etiqueta = f"{int(anos)} año(s)"

            else:

                etiqueta = f"{anos} año(s)"

            contador_experiencia[etiqueta] += 1

        elif experiencia.get("meses") is not None:

            meses = experiencia["meses"]

            contador_experiencia[
                f"{meses} mes(es)"
            ] += 1

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
# PLAN DE DESARROLLO
# ============================================================

def generar_plan_desarrollo(ofertas):

    contador = Counter()

    for oferta in ofertas:

        analisis = oferta.get(
            "analisis",
            {}
        )

        clasificacion = analisis.get(
            "clasificacion_conocimientos",
            {}
        )

        for competencia in clasificacion.get(
            "requieren_practica",
            []
        ):

            contador[competencia] += 1

    return dict(
        contador.most_common()
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

    plan_desarrollo = generar_plan_desarrollo(
        ofertas
    )

    historial["tendencias"] = tendencias

    historial["resumen_mercado"] = {

        "ofertas_analizadas": ofertas_analizadas,

        "competencias_mas_solicitadas":
            tendencias["competencias"],

        "experiencia_mas_solicitada":
            tendencias["experiencia_requerida"],

        "ubicaciones_mas_repetidas":
            tendencias["ubicaciones"],

        "cargos_mas_repetidos":
            tendencias["cargos"]
    }

    historial["plan_desarrollo"] = (
        plan_desarrollo
    )

    historial["perfil_analizado"] = {

        "profesion":
            PERFIL["profesion"],

        "experiencia_meses":
            PERFIL["experiencia_meses"],

        "certificacion_electrica":
            PERFIL["certificacion_electrica"],

        "objetivo":
            "Conseguir experiencia práctica en terreno y crecer hacia automatización y mantenimiento industrial."
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
    # RESULTADO EN CONSOLA
    # ========================================================

    print()
    print("==============================================")
    print("       ANÁLISIS LABORAL DEL PERFIL")
    print("==============================================")

    print(
        f"Ofertas analizadas: {ofertas_analizadas}"
    )

    print()
    print("COMPETENCIAS MÁS SOLICITADAS")

    for competencia, cantidad in (
        tendencias["competencias"].items()
    ):

        print(
            f"  - {competencia}: {cantidad}"
        )

    print()
    print("EXPERIENCIA SOLICITADA")

    if tendencias["experiencia_requerida"]:

        for nivel, cantidad in (
            tendencias["experiencia_requerida"].items()
        ):

            print(
                f"  - {nivel}: {cantidad}"
            )

    else:

        print(
            "  - No se detectó experiencia explícita."
        )

    print()
    print("PLAN DE DESARROLLO")

    if plan_desarrollo:

        for competencia, cantidad in (
            plan_desarrollo.items()
        ):

            print(
                f"  - {competencia}: "
                f"aparece como brecha práctica en "
                f"{cantidad} oferta(s)"
            )

    else:

        print(
            "  - No se detectaron brechas prácticas."
        )

    print()
    print("OFERTAS Y PRIORIDAD")

    for oferta in ofertas:

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
            f"  {oferta.get('titulo', 'Sin título')}"
        )

        print(
            f"  Puntaje: "
            f"{compatibilidad.get('puntaje')}"
        )

        print(
            f"  Ajuste: "
            f"{compatibilidad.get('probabilidad_ajuste')}"
        )

        print(
            f"  Prioridad: "
            f"{compatibilidad.get('prioridad_postulacion')}"
        )

        print(
            f"  Recomendación: "
            f"{compatibilidad.get('recomendacion')}"
        )

    print()
    print("==============================================")


# ============================================================
# EJECUTAR
# ============================================================

if __name__ == "__main__":

    analizar_historial()
