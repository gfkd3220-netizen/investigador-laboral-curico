import json
import re
from collections import Counter


# ============================================================
# CONFIGURACIÓN
# ============================================================

ARCHIVO_HISTORIAL = "historial.json"
ARCHIVO_PERFIL = "perfil.json"


# ============================================================
# COMPETENCIAS
# ============================================================

COMPETENCIAS = {
    "electricidad industrial": [
        "electricidad industrial",
        "eléctrica industrial",
        "electrico industrial",
        "electricista industrial",
        "instalaciones electricas"
    ],

    "mantenimiento industrial": [
        "mantenimiento industrial",
        "mantención industrial",
        "mantenimiento",
        "mantención"
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
        "control automatico"
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
        "resolucion de fallas"
    ],

    "mantenimiento preventivo": [
        "mantenimiento preventivo",
        "mantención preventiva"
    ],

    "mantenimiento correctivo": [
        "mantenimiento correctivo",
        "mantención correctiva"
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
    ]
}


# ============================================================
# EXPERIENCIA
# ============================================================

PATRONES_EXPERIENCIA = {
    "sin experiencia": [
        "sin experiencia",
        "no requiere experiencia",
        "recién egresado",
        "recien egresado",
        "sin requerir experiencia",
        "no se requiere experiencia"
    ],

    "menos de 1 año": [
        "6 meses de experiencia",
        "6 meses experiencia",
        "menos de 1 año",
        "menos de un año",
        "experiencia de 6 meses",
        "experiencia 6 meses"
    ],

    "1 año": [
        "1 año de experiencia",
        "1 año experiencia",
        "un año de experiencia",
        "experiencia de 1 año",
        "experiencia 1 año",
        "experiencia mínima de 1 año",
        "experiencia minima de 1 año"
    ],

    "2 años": [
        "2 años de experiencia",
        "2 años experiencia",
        "dos años de experiencia",
        "experiencia de 2 años",
        "experiencia 2 años",
        "experiencia mínima de 2 años",
        "experiencia minima de 2 años"
    ],

    "3 años o más": [
        "3 años de experiencia",
        "4 años de experiencia",
        "5 años de experiencia",
        "3 años experiencia",
        "4 años experiencia",
        "5 años experiencia",
        "experiencia de 3 años",
        "experiencia de 4 años",
        "experiencia de 5 años",
        "más de 3 años",
        "mas de 3 años",
        "experiencia mínima de 3 años",
        "experiencia minima de 3 años"
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

    for original, nuevo in reemplazos.items():
        texto = texto.replace(original, nuevo)

    return texto


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
# DETECTAR EXPERIENCIA
# ============================================================

def detectar_experiencia(texto):

    texto_normalizado = normalizar(texto)

    resultados = []

    for nivel, patrones in PATRONES_EXPERIENCIA.items():

        for patron in patrones:

            if normalizar(patron) in texto_normalizado:
                resultados.append(nivel)
                break

    return resultados


# ============================================================
# EXTRAER AÑOS DE EXPERIENCIA
# ============================================================

def extraer_anos_experiencia(texto):

    texto_normalizado = normalizar(texto)

    patrones = [
        r"(\d+)\s+anos?\s+de\s+experiencia",
        r"(\d+)\s+anos?\s+experiencia",
        r"experiencia\s+(?:de\s+)?(\d+)\s+anos?",
        r"experiencia\s+minima\s+de\s+(\d+)\s+anos?"
    ]

    numeros = []

    for patron in patrones:

        coincidencias = re.findall(
            patron,
            texto_normalizado
        )

        for numero in coincidencias:

            numero = int(numero)

            if numero not in numeros:
                numeros.append(numero)

    if numeros:
        return max(numeros)

    if "dos anos de experiencia" in texto_normalizado:
        return 2

    if "un ano de experiencia" in texto_normalizado:
        return 1

    return None


# ============================================================
# EXTRAER TEXTO DE UNA OFERTA
# ============================================================

def texto_oferta(oferta):

    partes = []

    for campo in [
        "titulo",
        "empresa",
        "ubicacion",
        "descripcion",
        "requisitos"
    ]:

        valor = oferta.get(campo, "")

        if valor:
            partes.append(str(valor))

    return " ".join(partes)


# ============================================================
# CARGAR PERFIL
# ============================================================

def cargar_perfil():

    try:

        with open(
            ARCHIVO_PERFIL,
            "r",
            encoding="utf-8"
        ) as archivo:

            return json.load(archivo)

    except FileNotFoundError:

        print("No se encontró perfil.json")

        return {}


# ============================================================
# OBTENER DATOS DEL PERFIL
# ============================================================

def datos_perfil(perfil):

    profesion = perfil.get(
        "profesion",
        "Técnico en Automatización Industrial"
    )

    certificacion = perfil.get(
        "certificacion_electrica",
        ""
    )

    experiencia = perfil.get(
        "experiencia",
        {}
    )

    meses_experiencia = experiencia.get(
        "meses_aproximados",
        0
    )

    conocimientos = perfil.get(
        "priorizar",
        []
    )

    cargos = perfil.get(
        "tipo_de_cargo_prioritario",
        []
    )

    zonas = perfil.get(
        "objetivo",
        {}
    ).get(
        "zona_prioritaria",
        []
    )

    return {
        "profesion": profesion,
        "certificacion": certificacion,
        "meses_experiencia": meses_experiencia,
        "conocimientos": conocimientos,
        "cargos": cargos,
        "zonas": zonas
    }


# ============================================================
# COMPARAR CARGO
# ============================================================

def cargos_coincidentes(titulo, cargos):

    titulo_normalizado = normalizar(titulo)

    encontrados = []

    for cargo in cargos:

        palabras = normalizar(cargo).split()

        coincidencias = 0

        for palabra in palabras:

            if len(palabra) >= 4 and palabra in titulo_normalizado:
                coincidencias += 1

        if coincidencias >= 1:
            encontrados.append(cargo)

    return encontrados


# ============================================================
# COMPARAR UBICACIÓN
# ============================================================

def analizar_ubicacion(ubicacion, zonas):

    ubicacion_normalizada = normalizar(ubicacion)

    for zona in zonas:

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
# ANALIZAR COMPATIBILIDAD
# ============================================================

def calcular_compatibilidad(
    oferta,
    competencias,
    anos_solicitados,
    perfil
):

    datos = datos_perfil(perfil)

    fortalezas = []
    conocimientos_relacionados = []
    brechas = []
    brechas_practicas = []
    aprendizaje_rapido = []

    puntaje = 0

    titulo = oferta.get("titulo", "")
    ubicacion = oferta.get("ubicacion", "")

    # --------------------------------------------------------
    # FORMACIÓN
    # --------------------------------------------------------

    fortalezas.append(
        "La formación técnica está relacionada con automatización, control y electricidad."
    )

    puntaje += 20

    # --------------------------------------------------------
    # CERTIFICACIÓN ELÉCTRICA
    # --------------------------------------------------------

    if datos["certificacion"]:

        fortalezas.append(
            f"El perfil cuenta con referencia a {datos['certificacion']}."
        )

        puntaje += 10

    # --------------------------------------------------------
    # COMPETENCIAS
    # --------------------------------------------------------

    competencias_perfil = [
        normalizar(x)
        for x in datos["conocimientos"]
    ]

    for competencia in competencias:

        if normalizar(competencia) in competencias_perfil:

            fortalezas.append(
                f"El perfil prioriza conocimientos relacionados con {competencia}."
            )

            puntaje += 6

        else:

            conocimientos_relacionados.append(
                competencia
            )

    # --------------------------------------------------------
    # UBICACIÓN
    # --------------------------------------------------------

    ubicacion_info = analizar_ubicacion(
        ubicacion,
        datos["zonas"]
    )

    if ubicacion_info["zona_prioritaria"]:

        fortalezas.append(
            f"La ubicación ({ubicacion}) está dentro de las zonas prioritarias."
        )

        puntaje += 10

    else:

        brechas.append(
            "La ubicación no coincide con las zonas prioritarias del perfil."
        )

    # --------------------------------------------------------
    # CARGO
    # --------------------------------------------------------

    cargos = cargos_coincidentes(
        titulo,
        datos["cargos"]
    )

    if cargos:

        fortalezas.append(
            "El tipo de cargo coincide con uno de los cargos prioritarios."
        )

        puntaje += 10

    # --------------------------------------------------------
    # EXPERIENCIA
    # --------------------------------------------------------

    meses_perfil = datos["meses_experiencia"]

    if anos_solicitados is not None:

        meses_solicitados = anos_solicitados * 12

        if meses_perfil >= meses_solicitados:

            fortalezas.append(
                "La experiencia registrada alcanza el mínimo solicitado."
            )

            puntaje += 15

        else:

            diferencia = meses_solicitados - meses_perfil

            brechas.append(
                f"La oferta solicita aproximadamente {anos_solicitados} año(s) de experiencia; "
                f"el perfil registra aproximadamente {meses_perfil} meses."
            )

            if diferencia <= 12:

                aprendizaje_rapido.append(
                    "La diferencia de experiencia es relativamente pequeña; "
                    "conviene postular igualmente si el resto de los requisitos encaja."
                )

            else:

                brechas_practicas.append(
                    "La principal diferencia es experiencia práctica acumulada en terreno."
                )

    else:

        puntaje += 10

    # --------------------------------------------------------
    # CLASIFICACIÓN
    # --------------------------------------------------------

    if puntaje >= 75:
        probabilidad = "ALTA"

    elif puntaje >= 50:
        probabilidad = "MEDIA"

    else:
        probabilidad = "BAJA"

    # --------------------------------------------------------
    # BRECHAS PRÁCTICAS
    # --------------------------------------------------------

    competencias_practicas = [
        "diagnóstico de fallas",
        "instrumentación",
        "mantenimiento industrial",
        "mantenimiento correctivo",
        "neumática",
        "hidráulica"
    ]

    for competencia in competencias:

        if competencia in competencias_practicas:

            if competencia not in brechas_practicas:

                brechas_practicas.append(
                    f"{competencia.capitalize()}: "
                    "conviene desarrollarla mediante experiencia práctica en terreno."
                )

    # --------------------------------------------------------
    # APRENDIZAJE AUTODIDACTA
    # --------------------------------------------------------

    competencias_teoricas = [
        "PLC",
        "HMI",
        "SCADA",
        "automatización",
        "variadores de frecuencia",
        "lectura de planos",
        "seguridad eléctrica"
    ]

    for competencia in competencias:

        if competencia in competencias_teoricas:

            aprendizaje_rapido.append(
                f"{competencia}: puede reforzarse mediante estudio, "
                "simulación y práctica guiada."
            )

    # --------------------------------------------------------
    # ELIMINAR DUPLICADOS
    # --------------------------------------------------------

    conocimientos_relacionados = list(
        dict.fromkeys(conocimientos_relacionados)
    )

    brechas = list(
        dict.fromkeys(brechas)
    )

    brechas_practicas = list(
        dict.fromkeys(brechas_practicas)
    )

    aprendizaje_rapido = list(
        dict.fromkeys(aprendizaje_rapido)
    )

    return {
        "puntaje": min(puntaje, 100),
        "probabilidad_ajuste": probabilidad,
        "fortalezas": fortalezas,
        "conocimientos_relacionados": conocimientos_relacionados,
        "brechas": brechas,
        "aprendizaje_rapido": aprendizaje_rapido,
        "brechas_practicas": brechas_practicas
    }, ubicacion_info, cargos


# ============================================================
# ANALIZAR UNA OFERTA
# ============================================================

def analizar_oferta(oferta, perfil):

    texto = texto_oferta(oferta)

    competencias = detectar_competencias(texto)

    experiencia_detectada = detectar_experiencia(texto)

    anos_solicitados = extraer_anos_experiencia(texto)

    compatibilidad, ubicacion_info, cargos = calcular_compatibilidad(
        oferta,
        competencias,
        anos_solicitados,
        perfil
    )

    return {
        "competencias_detectadas": competencias,
        "experiencia_detectada": experiencia_detectada,
        "anos_experiencia_solicitados": anos_solicitados,
        "ubicacion": ubicacion_info,
        "cargos_coincidentes": cargos,
        "compatibilidad": compatibilidad
    }


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

            historial = json.load(archivo)

    except FileNotFoundError:

        print("No se encontró historial.json")
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

        # Competencias
        for competencia in resultado["competencias_detectadas"]:

            contador_competencias[competencia] += 1

        # Experiencia
        for experiencia in resultado["experiencia_detectada"]:

            contador_experiencia[experiencia] += 1

        # Ubicación
        ubicacion = oferta.get(
            "ubicacion",
            ""
        )

        if ubicacion:

            contador_ubicaciones[ubicacion] += 1

        # Cargo
        titulo = oferta.get(
            "titulo",
            ""
        )

        if titulo:

            contador_cargos[titulo] += 1

        ofertas_analizadas += 1

    # --------------------------------------------------------
    # TENDENCIAS
    # --------------------------------------------------------

    historial.setdefault(
        "tendencias",
        {}
    )

    historial["tendencias"]["competencias"] = dict(
        contador_competencias.most_common()
    )

    historial["tendencias"]["experiencia_requerida"] = dict(
        contador_experiencia.most_common()
    )

    historial["tendencias"]["ubicaciones"] = dict(
        contador_ubicaciones.most_common()
    )

    historial["tendencias"]["cargos"] = dict(
        contador_cargos.most_common()
    )

    # --------------------------------------------------------
    # INFORMACIÓN GENERAL
    # --------------------------------------------------------

    historial["resumen_mercado"] = {
        "ofertas_analizadas": ofertas_analizadas,
        "competencias_mas_solicitadas": dict(
            contador_competencias.most_common(10)
        ),
        "experiencia_mas_solicitada": dict(
            contador_experiencia.most_common()
        ),
        "ubicaciones_mas_repetidas": dict(
            contador_ubicaciones.most_common(10)
        ),
        "cargos_mas_repetidos": dict(
            contador_cargos.most_common(10)
        )
    }

    historial["ultima_actualizacion"] = (
        "actualizado automáticamente"
    )

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

    # --------------------------------------------------------
    # MOSTRAR RESULTADO
    # --------------------------------------------------------

    print("==========================================")
    print("ANÁLISIS LABORAL")
    print("==========================================")

    print(
        f"Ofertas analizadas: {ofertas_analizadas}"
    )

    print("\nCOMPETENCIAS MÁS REPETIDAS:")

    for competencia, cantidad in (
        contador_competencias.most_common()
    ):

        print(
            f"- {competencia}: {cantidad} ofertas"
        )

    print("\nEXPERIENCIA SOLICITADA:")

    for nivel, cantidad in (
        contador_experiencia.most_common()
    ):

        print(
            f"- {nivel}: {cantidad} ofertas"
        )

    print("\nUBICACIONES MÁS REPETIDAS:")

    for ubicacion, cantidad in (
        contador_ubicaciones.most_common()
    ):

        print(
            f"- {ubicacion}: {cantidad} ofertas"
        )

    print("\nCARGOS MÁS REPETIDOS:")

    for cargo, cantidad in (
        contador_cargos.most_common()
    ):

        print(
            f"- {cargo}: {cantidad} ofertas"
        )

    print("==========================================")


# ============================================================
# EJECUTAR
# ============================================================

if __name__ == "__main__":

    analizar_historial()
