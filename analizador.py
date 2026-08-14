import json
import re
from collections import Counter


# ============================================================
# CONFIGURACIÓN
# ============================================================

ARCHIVO_HISTORIAL = "historial.json"
ARCHIVO_PERFIL = "perfil.json"


# ============================================================
# COMPETENCIAS DEL MERCADO
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
# COMPETENCIAS QUE REQUIEREN MÁS PRÁCTICA
# ============================================================

COMPETENCIAS_PRACTICAS = {
    "diagnóstico de fallas",
    "mantenimiento industrial",
    "mantenimiento correctivo",
    "instrumentación",
    "tableros eléctricos",
    "motores eléctricos",
    "variadores de frecuencia",
    "neumática",
    "hidráulica"
}


# ============================================================
# COMPETENCIAS QUE SE PUEDEN REFORZAR CON ESTUDIO/SIMULACIÓN
# ============================================================

COMPETENCIAS_APRENDIZAJE_RAPIDO = {
    "PLC",
    "HMI",
    "SCADA",
    "lectura de planos",
    "automatización",
    "seguridad eléctrica",
    "sensores"
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
        r"(\d+)\s*anos?\s*(?:de\s*)?experiencia",
        r"experiencia\s*(?:de|minima\s*de)?\s*(\d+)\s*anos?"
    ]

    numeros = []

    for patron in patrones:

        encontrados = re.findall(patron, texto_normalizado)

        for numero in encontrados:

            try:
                numeros.append(int(numero))
            except ValueError:
                pass

    if numeros:
        return max(numeros)

    if "mas de 3 anos" in texto_normalizado:
        return 4

    if "sin experiencia" in texto_normalizado:
        return 0

    return None


# ============================================================
# OBTENER TEXTO COMPLETO DE LA OFERTA
# ============================================================

def obtener_texto_oferta(oferta):

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

    return texto


# ============================================================
# DETECTAR CARGO COMPATIBLE
# ============================================================

def detectar_cargos(oferta, perfil):

    titulo = normalizar(oferta.get("titulo", ""))

    cargos = perfil.get("tipo_de_cargo_prioritario", [])

    encontrados = []

    for cargo in cargos:

        palabras = normalizar(cargo).split()

        coincidencias = 0

        for palabra in palabras:

            if len(palabra) >= 4 and palabra in titulo:
                coincidencias += 1

        if coincidencias >= 1:
            encontrados.append(cargo)

    return encontrados


# ============================================================
# ANALIZAR UBICACIÓN
# ============================================================

def analizar_ubicacion(oferta, perfil):

    ubicacion_oferta = str(oferta.get("ubicacion", "")).strip()

    zonas = perfil.get("objetivo", {}).get("zona_prioritaria", [])

    ubicacion_normalizada = normalizar(ubicacion_oferta)

    coincidencia = None

    for zona in zonas:

        if normalizar(zona) in ubicacion_normalizada:
            coincidencia = zona
            break

    return {
        "ubicacion_oferta": ubicacion_oferta,
        "zona_prioritaria": coincidencia is not None,
        "zona_coincidente": coincidencia
    }


# ============================================================
# COMPATIBILIDAD
# ============================================================

def calcular_compatibilidad(
    oferta,
    perfil,
    competencias,
    experiencia,
    anos_experiencia_solicitados,
    cargos_coincidentes,
    ubicacion
):

    puntaje = 0

    fortalezas = []
    brechas = []
    aprendizaje_rapido = []
    brechas_practicas = []
    conocimientos_relacionados = []

    # --------------------------------------------------------
    # FORMACIÓN
    # --------------------------------------------------------

    profesion = perfil.get("profesion", "")

    if profesion:
        puntaje += 15

        fortalezas.append(
            "La formación técnica está relacionada con el área del cargo."
        )

    # --------------------------------------------------------
    # CERTIFICACIÓN ELÉCTRICA
    # --------------------------------------------------------

    certificacion = perfil.get("certificacion_electrica", "")

    if isinstance(certificacion, dict):

        tipo = certificacion.get("tipo", "")
        estado = certificacion.get("estado", "")

        if tipo:

            if normalizar(estado) == "obtenida":
                puntaje += 10

                fortalezas.append(
                    f"Cuenta con {tipo} obtenida."
                )

            else:

                puntaje += 5

                fortalezas.append(
                    f"Cuenta con {tipo} {normalizar(estado)}."
                )

    elif certificacion:

        puntaje += 5

        fortalezas.append(
            f"Cuenta con referencia a {certificacion}."
        )

    # --------------------------------------------------------
    # COMPETENCIAS
    # --------------------------------------------------------

    priorizar = perfil.get("priorizar", [])

    priorizar_normalizado = {
        normalizar(item): item
        for item in priorizar
    }

    for competencia in competencias:

        if normalizar(competencia) in priorizar_normalizado:

            puntaje += 7

            fortalezas.append(
                f"El perfil prioriza conocimientos relacionados con {competencia}."
            )

        else:

            conocimientos_relacionados.append(
                competencia
            )

    # --------------------------------------------------------
    # UBICACIÓN
    # --------------------------------------------------------

    if ubicacion["zona_prioritaria"]:

        puntaje += 10

        fortalezas.append(
            f"La ubicación ({ubicacion['ubicacion_oferta']}) está dentro de las zonas prioritarias."
        )

    # --------------------------------------------------------
    # CARGO
    # --------------------------------------------------------

    if cargos_coincidentes:

        puntaje += 10

        fortalezas.append(
            "El tipo de cargo coincide con uno de los cargos prioritarios."
        )

    # --------------------------------------------------------
    # EXPERIENCIA
    # --------------------------------------------------------

    meses_perfil = (
        perfil.get("experiencia", {})
        .get("meses_aproximados", 0)
    )

    if anos_experiencia_solicitados is not None:

        meses_solicitados = anos_experiencia_solicitados * 12

        diferencia = max(
            0,
            meses_solicitados - meses_perfil
        )

        if diferencia == 0:

            puntaje += 15

            fortalezas.append(
                "La experiencia indicada por la oferta es compatible con la experiencia registrada en el perfil."
            )

        elif diferencia <= 12:

            puntaje += 5

            brechas.append(
                f"La oferta solicita aproximadamente {anos_experiencia_solicitados} año(s) de experiencia; "
                f"el perfil registra aproximadamente {meses_perfil} meses."
            )

        else:

            brechas.append(
                f"La oferta solicita aproximadamente {anos_experiencia_solicitados} año(s) de experiencia; "
                f"el perfil registra aproximadamente {meses_perfil} meses."
            )

    else:

        puntaje += 15

        fortalezas.append(
            "La oferta no presenta un requisito numérico claro de experiencia."
        )

    # --------------------------------------------------------
    # ANALIZAR BRECHAS TÉCNICAS
    # --------------------------------------------------------

    conocimientos_perfil = set()

    for item in perfil.get("priorizar", []):

        conocimientos_perfil.add(
            normalizar(item)
        )

    for competencia in competencias:

        competencia_normalizada = normalizar(competencia)

        if competencia_normalizada not in conocimientos_perfil:

            brechas.append(competencia)

        if competencia in COMPETENCIAS_APRENDIZAJE_RAPIDO:

            aprendizaje_rapido.append(
                f"{competencia}: puede reforzarse mediante estudio, simulación y práctica guiada."
            )

        if competencia in COMPETENCIAS_PRACTICAS:

            brechas_practicas.append(
                f"{competencia}: conviene desarrollarla mediante experiencia práctica en terreno."
            )

    # --------------------------------------------------------
    # INTERPRETACIÓN DE EXPERIENCIA
    # --------------------------------------------------------

    if (
        anos_experiencia_solicitados is not None
        and meses_perfil < anos_experiencia_solicitados * 12
    ):

        diferencia_anios = (
            anos_experiencia_solicitados * 12 - meses_perfil
        ) / 12

        if diferencia_anios <= 1:

            aprendizaje_rapido.insert(
                0,
                "La diferencia de experiencia es relativamente pequeña; conviene postular igualmente si el resto de los requisitos encaja."
            )

        else:

            brechas_practicas.insert(
                0,
                "La principal diferencia es experiencia práctica acumulada en terreno."
            )

    # --------------------------------------------------------
    # LIMITAR PUNTAJE
    # --------------------------------------------------------

    puntaje = min(100, puntaje)

    # --------------------------------------------------------
    # PROBABILIDAD
    # --------------------------------------------------------

    if puntaje >= 75:
        probabilidad = "ALTA"

    elif puntaje >= 55:
        probabilidad = "MEDIA"

    else:
        probabilidad = "BAJA"

    return {
        "puntaje": puntaje,
        "probabilidad_ajuste": probabilidad,
        "fortalezas": fortalezas,
        "conocimientos_relacionados": conocimientos_relacionados,
        "brechas": brechas,
        "aprendizaje_rapido": aprendizaje_rapido,
        "brechas_practicas": brechas_practicas
    }


# ============================================================
# ANALIZAR UNA OFERTA
# ============================================================

def analizar_oferta(oferta, perfil):

    texto = obtener_texto_oferta(oferta)

    competencias = detectar_competencias(texto)

    experiencia = detectar_experiencia(texto)

    anos_experiencia = extraer_anos_experiencia(texto)

    ubicacion = analizar_ubicacion(
        oferta,
        perfil
    )

    cargos_coincidentes = detectar_cargos(
        oferta,
        perfil
    )

    compatibilidad = calcular_compatibilidad(
        oferta,
        perfil,
        competencias,
        experiencia,
        anos_experiencia,
        cargos_coincidentes,
        ubicacion
    )

    return {
        "competencias_detectadas": competencias,
        "experiencia_detectada": experiencia,
        "anos_experiencia_solicitados": anos_experiencia,
        "ubicacion": ubicacion,
        "cargos_coincidentes": cargos_coincidentes,
        "compatibilidad": compatibilidad
    }


# ============================================================
# ANALIZAR HISTORIAL
# ============================================================

def analizar_historial():

    # --------------------------------------------------------
    # CARGAR HISTORIAL
    # --------------------------------------------------------

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

    # --------------------------------------------------------
    # CARGAR PERFIL
    # --------------------------------------------------------

    try:

        with open(
            ARCHIVO_PERFIL,
            "r",
            encoding="utf-8"
        ) as archivo:

            perfil = json.load(archivo)

    except FileNotFoundError:

        print("No se encontró perfil.json")
        return

    ofertas = historial.get(
        "ofertas",
        []
    )

    contador_competencias = Counter()
    contador_experiencia = Counter()
    contador_ubicaciones = Counter()
    contador_cargos = Counter()

    ofertas_analizadas = 0

    # --------------------------------------------------------
    # ANALIZAR OFERTAS
    # --------------------------------------------------------

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

        ofertas_analizadas += 1

    # --------------------------------------------------------
    # TENDENCIAS
    # --------------------------------------------------------

    historial.setdefault(
        "tendencias",
        {}
    )

    historial["tendencias"][
        "competencias"
    ] = dict(
        contador_competencias.most_common()
    )

    historial["tendencias"][
        "experiencia_requerida"
    ] = dict(
        contador_experiencia.most_common()
    )

    historial["tendencias"][
        "ubicaciones"
    ] = dict(
        contador_ubicaciones.most_common()
    )

    historial["tendencias"][
        "cargos"
    ] = dict(
        contador_cargos.most_common()
    )

    # --------------------------------------------------------
    # RESUMEN DEL MERCADO
    # --------------------------------------------------------

    historial["resumen_mercado"] = {
        "ofertas_analizadas": ofertas_analizadas,

        "competencias_mas_solicitadas":
            dict(
                contador_competencias.most_common()
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
            )
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

    print("\nUBICACIONES:")

    for ubicacion, cantidad in (
        contador_ubicaciones.most_common()
    ):

        print(
            f"- {ubicacion}: {cantidad} ofertas"
        )

    print("\nCARGOS:")

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
