import json
import re
from collections import Counter


# ============================================================
# CONFIGURACIÓN
# ============================================================

ARCHIVO_HISTORIAL = "historial.json"
ARCHIVO_PERFIL = "perfil.json"


# ============================================================
# CONOCIMIENTOS DEL PERFIL
#
# IMPORTANTE:
# - "practico": experiencia real en terreno
# - "formacion": conocimientos académicos / técnicos
# - "estudio": conocimientos que pueden reforzarse principalmente
#   mediante estudio, simulación o práctica guiada
# ============================================================

CONOCIMIENTOS_PRACTICOS = {
    "electricidad de baja tensión",
    "canalizaciones",
    "bandejas portacables",
    "cableado",
    "canaletas",
    "conexión de motores",
    "instalación de luminarias",
    "instalación eléctrica residencial",
    "herramientas eléctricas",
    "esmeril",
    "pinzas",
    "trabajos eléctricos",
}

CONOCIMIENTOS_FORMACION = {
    "electricidad industrial",
    "automatización",
    "control industrial",
    "tableros eléctricos",
    "PLC",
    "variadores de frecuencia",
    "HMI",
    "arranque directo",
    "estrella triángulo",
    "conductores de fuerza",
    "conductores de control",
    "lectura básica de planos",
    "mantenimiento industrial",
    "mantenimiento preventivo",
    "instrumentación",
    "sensores",
}

CONOCIMIENTOS_ESTUDIO = {
    "PLC",
    "Siemens",
    "instrumentación",
    "diagnóstico de fallas",
    "mantenimiento industrial",
    "mantenimiento preventivo",
    "SCADA",
    "HMI",
    "variadores de frecuencia",
    "automatización",
}


# ============================================================
# COMPETENCIAS DEL MERCADO
# ============================================================

COMPETENCIAS = {
    "electricidad industrial": [
        "electricidad industrial",
        "eléctrica industrial",
        "electrico industrial",
        "electricista industrial",
    ],

    "mantenimiento industrial": [
        "mantenimiento industrial",
        "mantención industrial",
    ],

    "mantenimiento preventivo": [
        "mantenimiento preventivo",
        "mantención preventiva",
    ],

    "mantenimiento correctivo": [
        "mantenimiento correctivo",
        "mantención correctiva",
    ],

    "tableros eléctricos": [
        "tablero eléctrico",
        "tableros eléctricos",
        "tableros electricos",
    ],

    "lectura de planos": [
        "lectura de planos",
        "interpretación de planos",
        "interpretacion de planos",
        "planos eléctricos",
        "planos electricos",
    ],

    "PLC": [
        "plc",
        "controlador lógico programable",
        "controlador programable",
    ],

    "Siemens": [
        "siemens",
        "s7-1200",
        "s7 1200",
        "s7-1500",
        "s7 1500",
        "tia portal",
    ],

    "variadores de frecuencia": [
        "variador de frecuencia",
        "variadores de frecuencia",
        "vfd",
        "drive",
    ],

    "automatización": [
        "automatización",
        "automatizacion",
        "control automático",
        "control automatico",
    ],

    "instrumentación": [
        "instrumentación",
        "instrumentacion",
        "instrumentista",
        "instrumentos industriales",
    ],

    "neumática": [
        "neumática",
        "neumatica",
        "sistemas neumáticos",
        "sistemas neumaticos",
    ],

    "hidráulica": [
        "hidráulica",
        "hidraulica",
        "sistemas hidráulicos",
        "sistemas hidraulicos",
    ],

    "diagnóstico de fallas": [
        "diagnóstico de fallas",
        "diagnostico de fallas",
        "detección de fallas",
        "deteccion de fallas",
        "resolución de fallas",
        "resolucion de fallas",
        "diagnosticar fallas",
    ],

    "HMI": [
        "hmi",
        "interfaz hombre máquina",
        "interfaz hombre maquina",
    ],

    "SCADA": [
        "scada",
    ],

    "sensores": [
        "sensores",
        "sensor industrial",
    ],

    "motores eléctricos": [
        "motor eléctrico",
        "motores eléctricos",
        "motor electrico",
        "motores electricos",
    ],

    "seguridad eléctrica": [
        "seguridad eléctrica",
        "seguridad electrica",
        "procedimientos eléctricos",
        "procedimientos electricos",
    ],

    "necesidad de terreno": [
        "experiencia en terreno",
        "trabajo en terreno",
        "experiencia práctica",
        "experiencia practica",
        "experiencia en planta",
        "experiencia industrial",
    ],
}


# ============================================================
# EXPERIENCIA
# ============================================================

PATRONES_EXPERIENCIA = [
    r"(\d+(?:[.,]\d+)?)\s*(?:años|año)",
    r"(\d+)\s*(?:meses|mes)",
]


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
        "ñ": "n",
    }

    for original, nuevo in reemplazos.items():
        texto = texto.replace(original, nuevo)

    return texto


# ============================================================
# CARGAR PERFIL
# ============================================================

def cargar_perfil():

    try:

        with open(ARCHIVO_PERFIL, "r", encoding="utf-8") as archivo:
            return json.load(archivo)

    except FileNotFoundError:

        print("No se encontró perfil.json")
        return {}


# ============================================================
# EXPERIENCIA DEL PERFIL
# ============================================================

def obtener_experiencia_perfil(perfil):

    experiencia = perfil.get("experiencia", {})

    meses = experiencia.get("meses_aproximados", 0)

    try:
        meses = float(meses)
    except (ValueError, TypeError):
        meses = 0.0

    return {
        "meses_aproximados": meses,
        "anos_aproximados": round(meses / 12, 2),
    }


# ============================================================
# DETECTAR AÑOS SOLICITADOS
# ============================================================

def detectar_anos_experiencia(texto):

    texto_normalizado = normalizar(texto)

    encontrados = []

    for patron in PATRONES_EXPERIENCIA:

        coincidencias = re.findall(
            patron,
            texto_normalizado
        )

        for valor in coincidencias:

            try:
                numero = float(valor.replace(",", "."))

                if "mes" in patron:
                    numero = numero / 12

                encontrados.append(numero)

            except ValueError:
                pass

    if not encontrados:
        return None

    return max(encontrados)


# ============================================================
# DETECTAR COMPETENCIAS
# ============================================================

def detectar_competencias(texto):

    texto_normalizado = normalizar(texto)

    encontradas = []

    for competencia, palabras in COMPETENCIAS.items():

        for palabra in palabras:

            palabra_normalizada = normalizar(palabra)

            if palabra_normalizada in texto_normalizado:

                if competencia not in encontradas:
                    encontradas.append(competencia)

                break

    return encontradas


# ============================================================
# OBTENER UBICACIÓN
# ============================================================

def analizar_ubicacion(oferta, perfil):

    ubicacion_oferta = str(
        oferta.get("ubicacion", "")
    ).strip()

    zonas = perfil.get(
        "objetivo",
        {}
    ).get(
        "zona_prioritaria",
        []
    )

    zonas_normalizadas = {
        normalizar(zona): zona
        for zona in zonas
    }

    ubicacion_normalizada = normalizar(
        ubicacion_oferta
    )

    for zona_normalizada, zona_original in zonas_normalizadas.items():

        if (
            zona_normalizada in ubicacion_normalizada
            or ubicacion_normalizada in zona_normalizada
        ):

            return {
                "ubicacion_oferta": ubicacion_oferta,
                "zona_prioritaria": True,
                "zona_coincidente": zona_original,
            }

    return {
        "ubicacion_oferta": ubicacion_oferta,
        "zona_prioritaria": False,
        "zona_coincidente": None,
    }


# ============================================================
# OBTENER CARGOS COINCIDENTES
# ============================================================

def analizar_cargos(oferta, perfil):

    titulo = normalizar(
        oferta.get("titulo", "")
    )

    cargos = perfil.get(
        "tipo_de_cargo_prioritario",
        []
    )

    coincidencias = []

    for cargo in cargos:

        palabras = normalizar(cargo).split()

        coincidencias_palabras = 0

        for palabra in palabras:

            if len(palabra) >= 4 and palabra in titulo:
                coincidencias_palabras += 1

        if coincidencias_palabras >= 1:

            coincidencias.append(cargo)

    return coincidencias


# ============================================================
# CLASIFICAR CONOCIMIENTO
# ============================================================

def clasificar_conocimiento(competencia):

    competencia_normalizada = normalizar(
        competencia
    )

    for conocimiento in CONOCIMIENTOS_PRACTICOS:

        if normalizar(conocimiento) == competencia_normalizada:
            return "practico"

    for conocimiento in CONOCIMIENTOS_FORMACION:

        if normalizar(conocimiento) == competencia_normalizada:
            return "formacion"

    for conocimiento in CONOCIMIENTOS_ESTUDIO:

        if normalizar(conocimiento) == competencia_normalizada:
            return "estudio"

    return "desconocido"


# ============================================================
# ANALIZAR CONOCIMIENTOS
# ============================================================

def analizar_conocimientos(competencias):

    relacionados = []
    aprendizaje_rapido = []
    brechas_practicas = []

    for competencia in competencias:

        tipo = clasificar_conocimiento(
            competencia
        )

        if tipo == "practico":

            relacionados.append(competencia)

        elif tipo == "formacion":

            relacionados.append(competencia)

        elif tipo == "estudio":

            aprendizaje_rapido.append(
                competencia
            )

        else:

            brechas_practicas.append(
                competencia
            )

    return {
        "conocimientos_relacionados": relacionados,
        "aprendizaje_rapido": aprendizaje_rapido,
        "brechas_practicas": brechas_practicas,
    }


# ============================================================
# DETERMINAR BRECHA DE EXPERIENCIA
# ============================================================

def analizar_brecha_experiencia(
    anos_solicitados,
    experiencia_perfil
):

    if anos_solicitados is None:
        return None

    anos_perfil = experiencia_perfil[
        "anos_aproximados"
    ]

    diferencia = max(
        0,
        anos_solicitados - anos_perfil
    )

    return {
        "anos_solicitados": anos_solicitados,
        "anos_perfil": anos_perfil,
        "diferencia_anos": round(
            diferencia,
            2
        ),
        "diferencia_meses": round(
            diferencia * 12,
            1
        ),
    }


# ============================================================
# GENERAR FORTALEZAS
# ============================================================

def generar_fortalezas(
    perfil,
    competencias,
    ubicacion,
    cargos
):

    fortalezas = []

    profesion = perfil.get(
        "profesion",
        ""
    )

    if profesion:
        fortalezas.append(
            "La formación técnica está relacionada con el área del cargo."
        )

    certificacion = perfil.get(
        "certificacion_electrica",
        ""
    )

    if certificacion:

        if isinstance(
            certificacion,
            dict
        ):

            tipo = certificacion.get(
                "tipo",
                "certificación eléctrica"
            )

            estado = certificacion.get(
                "estado",
                ""
            )

            if normalizar(estado) == "en tramite":

                fortalezas.append(
                    f"{tipo}: en trámite. "
                    "La certificación todavía no se considera obtenida."
                )

            else:

                fortalezas.append(
                    f"El perfil cuenta con {tipo}."
                )

        else:

            fortalezas.append(
                f"El perfil contempla {certificacion}."
            )

    for competencia in competencias:

        tipo = clasificar_conocimiento(
            competencia
        )

        if tipo in [
            "practico",
            "formacion"
        ]:

            fortalezas.append(
                f"El perfil presenta conocimientos relacionados con {competencia}."
            )

    if ubicacion["zona_prioritaria"]:

        fortalezas.append(
            f"La ubicación ({ubicacion['ubicacion_oferta']}) "
            "está dentro de las zonas prioritarias."
        )

    if cargos:

        fortalezas.append(
            "El tipo de cargo coincide con uno o más "
            "cargos prioritarios del perfil."
        )

    return fortalezas


# ============================================================
# GENERAR RECOMENDACIÓN
# ============================================================

def generar_recomendacion(
    puntaje,
    anos_solicitados,
    diferencia_meses,
    cargos,
    ubicacion
):

    if puntaje >= 80:

        prioridad = "ALTA"
        probabilidad = "ALTA"

    elif puntaje >= 65:

        prioridad = "MEDIA-ALTA"
        probabilidad = "MEDIA"

    elif puntaje >= 50:

        prioridad = "MEDIA"
        probabilidad = "MEDIA"

    else:

        prioridad = "BAJA"
        probabilidad = "BAJA"

    if not ubicacion["zona_prioritaria"]:

        if prioridad == "ALTA":
            prioridad = "MEDIA-ALTA"

        elif prioridad == "MEDIA-ALTA":
            prioridad = "MEDIA"

    if cargos and prioridad == "BAJA":

        prioridad = "MEDIA"

    if anos_solicitados is not None:

        if diferencia_meses <= 6:

            recomendacion = (
                "POSTULAR. La diferencia de experiencia "
                "es relativamente pequeña."
            )

        elif diferencia_meses <= 12:

            recomendacion = (
                "POSTULAR SI EL CARGO ACEPTA PERFILES "
                "JUNIOR O EXPERIENCIA EQUIVALENTE."
            )

        else:

            recomendacion = (
                "CONSIDERAR COMO POSTULACIÓN SECUNDARIA "
                "SI EL EMPLEADOR ES FLEXIBLE CON LA EXPERIENCIA."
            )

    else:

        recomendacion = (
            "POSTULAR SI EL RESTO DE LOS REQUISITOS ENCAJA."
        )

    return {
        "probabilidad_ajuste": probabilidad,
        "prioridad_postulacion": prioridad,
        "recomendacion": recomendacion,
    }


# ============================================================
# CALCULAR COMPATIBILIDAD
# ============================================================

def calcular_compatibilidad(
    perfil,
    competencias,
    ubicacion,
    cargos,
    anos_solicitados
):

    experiencia_perfil = obtener_experiencia_perfil(
        perfil
    )

    anos_perfil = experiencia_perfil[
        "anos_aproximados"
    ]

    puntaje = 0

    # --------------------------------------------------------
    # FORMACIÓN
    # --------------------------------------------------------

    if perfil.get("profesion"):

        puntaje += 20

    # --------------------------------------------------------
    # UBICACIÓN
    # --------------------------------------------------------

    if ubicacion["zona_prioritaria"]:

        puntaje += 15

    # --------------------------------------------------------
    # CARGO
    # --------------------------------------------------------

    if cargos:

        puntaje += 15

    # --------------------------------------------------------
    # COMPETENCIAS
    # --------------------------------------------------------

    for competencia in competencias:

        tipo = clasificar_conocimiento(
            competencia
        )

        if tipo == "practico":

            puntaje += 8

        elif tipo == "formacion":

            puntaje += 5

        elif tipo == "estudio":

            puntaje += 2

    # --------------------------------------------------------
    # EXPERIENCIA
    # --------------------------------------------------------

    if anos_solicitados is not None:

        if anos_solicitados <= anos_perfil:

            puntaje += 20

        elif anos_solicitados - anos_perfil <= 0.5:

            puntaje += 12

        elif anos_solicitados - anos_perfil <= 1:

            puntaje += 6

        else:

            puntaje += 0

    else:

        puntaje += 10

    # Limitar
    puntaje = min(
        100,
        puntaje
    )

    brecha = analizar_brecha_experiencia(
        anos_solicitados,
        experiencia_perfil
    )

    diferencia_meses = (
        brecha["diferencia_meses"]
        if brecha
        else 0
    )

    recomendacion = generar_recomendacion(
        puntaje,
        anos_solicitados,
        diferencia_meses,
        cargos,
        ubicacion
    )

    return {
        "puntaje": puntaje,
        **recomendacion,
        "experiencia": brecha,
    }


# ============================================================
# ANALIZAR UNA OFERTA
# ============================================================

def analizar_oferta(
    oferta,
    perfil
):

    texto = ""

    for campo in [
        "titulo",
        "empresa",
        "ubicacion",
        "descripcion",
        "requisitos",
    ]:

        valor = oferta.get(
            campo,
            ""
        )

        if valor:

            texto += " " + str(valor)

    competencias = detectar_competencias(
        texto
    )

    experiencia_detectada = []

    anos_solicitados = detectar_anos_experiencia(
        oferta.get(
            "requisitos",
            ""
        )
    )

    if anos_solicitados is not None:

        if anos_solicitados == 1:

            experiencia_detectada.append(
                "1 año"
            )

        elif anos_solicitados == 2:

            experiencia_detectada.append(
                "2 años"
            )

        elif anos_solicitados >= 3:

            experiencia_detectada.append(
                "3 años o más"
            )

        else:

            experiencia_detectada.append(
                f"{anos_solicitados} años"
            )

    ubicacion = analizar_ubicacion(
        oferta,
        perfil
    )

    cargos = analizar_cargos(
        oferta,
        perfil
    )

    conocimientos = analizar_conocimientos(
        competencias
    )

    compatibilidad = calcular_compatibilidad(
        perfil,
        competencias,
        ubicacion,
        cargos,
        anos_solicitados
    )

    fortalezas = generar_fortalezas(
        perfil,
        competencias,
        ubicacion,
        cargos
    )

    brechas = []

    # --------------------------------------------------------
    # BRECHA DE EXPERIENCIA
    # --------------------------------------------------------

    if compatibilidad["experiencia"]:

        diferencia = compatibilidad[
            "experiencia"
        ]

        if diferencia["diferencia_meses"] > 0:

            brechas.append(
                f"La oferta solicita aproximadamente "
                f"{diferencia['anos_solicitados']} año(s) "
                f"de experiencia; el perfil registra "
                f"aproximadamente "
                f"{diferencia['anos_perfil'] * 12:g} meses."
            )

    # --------------------------------------------------------
    # COMPETENCIAS NO PRACTICADAS
    # --------------------------------------------------------

    for competencia in competencias:

        tipo = clasificar_conocimiento(
            competencia
        )

        if tipo == "estudio":

            if competencia not in brechas:

                brechas.append(
                    f"{competencia}: conviene reforzarla."
                )

        elif tipo == "desconocido":

            if competencia not in brechas:

                brechas.append(
                    competencia
                )

    # --------------------------------------------------------
    # DETALLE DE EXPERIENCIA PRÁCTICA
    # --------------------------------------------------------

    brechas_practicas = list(
        conocimientos[
            "brechas_practicas"
        ]
    )

    for competencia in competencias:

        if competencia in [
            "mantenimiento industrial",
            "mantenimiento preventivo",
            "diagnóstico de fallas",
            "instrumentación",
        ]:

            if competencia not in brechas_practicas:

                tipo = clasificar_conocimiento(
                    competencia
                )

                if tipo != "practico":

                    brechas_practicas.append(
                        competencia
                    )

    # --------------------------------------------------------
    # APRENDIZAJE RÁPIDO
    # --------------------------------------------------------

    aprendizaje_rapido = list(
        conocimientos[
            "aprendizaje_rapido"
        ]
    )

    # --------------------------------------------------------
    # EXPERIENCIA PRÁCTICA DEL PERFIL
    # --------------------------------------------------------

    experiencia_perfil = obtener_experiencia_perfil(
        perfil
    )

    # --------------------------------------------------------
    # RESULTADO
    # --------------------------------------------------------

    return {

        "competencias_detectadas":
            competencias,

        "experiencia_detectada":
            experiencia_detectada,

        "anos_experiencia_solicitados":
            anos_solicitados,

        "experiencia_perfil":
            experiencia_perfil,

        "ubicacion":
            ubicacion,

        "cargos_coincidentes":
            cargos,

        "conocimientos_relacionados":
            conocimientos[
                "conocimientos_relacionados"
            ],

        "aprendizaje_rapido":
            aprendizaje_rapido,

        "brechas_practicas":
            brechas_practicas,

        "compatibilidad": {

            "puntaje":
                compatibilidad["puntaje"],

            "probabilidad_ajuste":
                compatibilidad[
                    "probabilidad_ajuste"
                ],

            "prioridad_postulacion":
                compatibilidad[
                    "prioridad_postulacion"
                ],

            "recomendacion":
                compatibilidad[
                    "recomendacion"
                ],

            "fortalezas":
                fortalezas,

            "conocimientos_relacionados":
                conocimientos[
                    "conocimientos_relacionados"
                ],

            "brechas":
                brechas,

            "aprendizaje_rapido":
                aprendizaje_rapido,

            "brechas_practicas":
                brechas_practicas,
        },
    }


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

    perfil = cargar_perfil()

    ofertas = historial.get(
        "ofertas",
        []
    )

    contador_competencias = Counter()
    contador_experiencia = Counter()
    contador_ubicaciones = Counter()
    contador_cargos = Counter()

    ofertas_analizadas = 0

    for oferta in ofertas:

        resultado = analizar_oferta(
            oferta,
            perfil
        )

        oferta["analisis"] = resultado

        for competencia in resultado[
            "competencias_detectadas"
        ]:

            contador_competencias[
                competencia
            ] += 1

        for experiencia in resultado[
            "experiencia_detectada"
        ]:

            contador_experiencia[
                experiencia
            ] += 1

        ubicacion = oferta.get(
            "ubicacion"
        )

        if ubicacion:

            contador_ubicaciones[
                ubicacion
            ] += 1

        titulo = oferta.get(
            "titulo"
        )

        if titulo:

            contador_cargos[
                titulo
            ] += 1

        ofertas_analizadas += 1

    # ========================================================
    # TENDENCIAS
    # ========================================================

    historial.setdefault(
        "tendencias",
        {}
    )

    historial[
        "tendencias"
    ][
        "competencias"
    ] = dict(
        contador_competencias.most_common()
    )

    historial[
        "tendencias"
    ][
        "experiencia_requerida"
    ] = dict(
        contador_experiencia.most_common()
    )

    historial[
        "tendencias"
    ][
        "ubicaciones"
    ] = dict(
        contador_ubicaciones.most_common()
    )

    historial[
        "tendencias"
    ][
        "cargos"
    ] = dict(
        contador_cargos.most_common()
    )

    # ========================================================
    # RESUMEN DEL MERCADO
    # ========================================================

    historial[
        "resumen_mercado"
    ] = {

        "ofertas_analizadas":
            ofertas_analizadas,

        "competencias_mas_solicitadas":
            dict(
                contador_competencias.most_common(
                    15
                )
            ),

        "experiencia_mas_solicitada":
            dict(
                contador_experiencia.most_common()
            ),

        "ubicaciones_mas_repetidas":
            dict(
                contador_ubicaciones.most_common()
            ),

        "cargos_mas_repetidos":
            dict(
                contador_cargos.most_common()
            ),
    }

    # ========================================================
    # ACTUALIZAR FECHA
    # ========================================================

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
    # MOSTRAR RESULTADO
    # ========================================================

    print(
        "=========================================="
    )

    print(
        "ANÁLISIS LABORAL"
    )

    print(
        "=========================================="
    )

    print(
        f"Ofertas analizadas: "
        f"{ofertas_analizadas}"
    )

    print(
        "\nCOMPETENCIAS MÁS SOLICITADAS:"
    )

    for competencia, cantidad in (
        contador_competencias.most_common()
    ):

        print(
            f"- {competencia}: "
            f"{cantidad} ofertas"
        )

    print(
        "\nEXPERIENCIA SOLICITADA:"
    )

    for nivel, cantidad in (
        contador_experiencia.most_common()
    ):

        print(
            f"- {nivel}: "
            f"{cantidad} ofertas"
        )

    print(
        "\nUBICACIONES:"
    )

    for ubicacion, cantidad in (
        contador_ubicaciones.most_common()
    ):

        print(
            f"- {ubicacion}: "
            f"{cantidad} ofertas"
        )

    print(
        "\nCARGOS:"
    )

    for cargo, cantidad in (
        contador_cargos.most_common()
    ):

        print(
            f"- {cargo}: "
            f"{cantidad} ofertas"
        )

    print(
        "=========================================="
    )


# ============================================================
# EJECUTAR
# ============================================================

if __name__ == "__main__":

    analizar_historial()
