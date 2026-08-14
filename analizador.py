import json
import re
from collections import Counter


# ============================================================
# CONFIGURACIÓN
# ============================================================

ARCHIVO_HISTORIAL = "historial.json"
ARCHIVO_PERFIL = "perfil.json"


# ============================================================
# COMPETENCIAS Y FAMILIAS
# ============================================================

COMPETENCIAS = {
    "electricidad industrial": [
        "electricidad industrial",
        "eléctrica industrial",
        "electrico industrial",
        "electricista industrial",
        "instalaciones eléctricas industriales"
    ],

    "mantenimiento industrial": [
        "mantenimiento industrial",
        "mantención industrial"
    ],

    "mantenimiento preventivo": [
        "mantenimiento preventivo",
        "mantención preventiva",
        "mantenimiento programado",
        "mantención programada",
        "plan de mantenimiento",
        "planes de mantenimiento",
        "inspecciones preventivas"
    ],

    "mantenimiento correctivo": [
        "mantenimiento correctivo",
        "mantención correctiva"
    ],

    "tableros eléctricos": [
        "tablero eléctrico",
        "tableros eléctricos",
        "tablero electrico",
        "tableros electricos",
        "panel eléctrico",
        "paneles eléctricos",
        "panel electrico",
        "paneles electricos"
    ],

    "lectura de planos": [
        "lectura de planos",
        "interpretación de planos",
        "interpretacion de planos",
        "planos eléctricos",
        "planos electricos",
        "planos de control",
        "planos de fuerza"
    ],

    "PLC": [
        "plc",
        "controlador lógico programable",
        "controlador programable",
        "programación plc",
        "programacion plc"
    ],

    "variadores de frecuencia": [
        "variador de frecuencia",
        "variadores de frecuencia",
        "vfd",
        "drive",
        "variador"
    ],

    "automatización": [
        "automatización",
        "automatizacion",
        "control automático",
        "control automatico",
        "automatización industrial",
        "automatizacion industrial",
        "control industrial"
    ],

    "instrumentación": [
        "instrumentación",
        "instrumentacion",
        "instrumentista",
        "instrumentos industriales",
        "instrumentación industrial",
        "instrumentacion industrial"
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
        "diagnóstico eléctrico",
        "diagnostico electrico",
        "detección de averías",
        "deteccion de averias"
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
        "motores electricos",
        "motores"
    ],

    "seguridad eléctrica": [
        "seguridad eléctrica",
        "seguridad electrica",
        "procedimientos eléctricos",
        "procedimientos electricos"
    ]
}


# ============================================================
# EXPERIENCIA SOLICITADA
# ============================================================

PATRONES_EXPERIENCIA = {
    "sin experiencia": [
        "sin experiencia",
        "no requiere experiencia",
        "recién egresado",
        "recien egresado",
        "sin requerir experiencia",
        "no se requiere experiencia",
        "no requiere de experiencia"
    ],

    "experiencia menor a 1 año": [
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

            palabra_normalizada = normalizar(palabra)

            if palabra_normalizada in texto_normalizado:
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
# EXTRAER AÑOS DE EXPERIENCIA SOLICITADOS
# ============================================================

def extraer_anos_experiencia(texto):

    texto_normalizado = normalizar(texto)

    patrones = [
        r"(\d+(?:[.,]\d+)?)\s*anos?\s*(?:de\s*)?experiencia",
        r"experiencia\s*(?:minima\s*)?(?:de\s*)?(\d+(?:[.,]\d+)?)\s*anos?",
        r"(\d+(?:[.,]\d+)?)\s*ano\s*de\s*experiencia"
    ]

    valores = []

    for patron in patrones:

        coincidencias = re.findall(patron, texto_normalizado)

        for valor in coincidencias:

            try:
                valores.append(float(valor.replace(",", ".")))
            except ValueError:
                pass

    if valores:
        return max(valores)

    if "dos anos de experiencia" in texto_normalizado:
        return 2.0

    if "un ano de experiencia" in texto_normalizado:
        return 1.0

    if "tres anos de experiencia" in texto_normalizado:
        return 3.0

    return None


# ============================================================
# LEER PERFIL
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

def obtener_meses_experiencia(perfil):

    experiencia = perfil.get("experiencia", {})

    try:
        return float(experiencia.get("meses_aproximados", 0))
    except (TypeError, ValueError):
        return 0.0


# ============================================================
# OBTENER TEXTO DEL PERFIL
# ============================================================

def obtener_texto_perfil(perfil):

    partes = []

    profesion = perfil.get("profesion", "")
    certificacion = perfil.get("certificacion_electrica", "")

    partes.append(str(profesion))
    partes.append(str(certificacion))

    experiencia = perfil.get("experiencia", {})

    partes.extend(experiencia.get("tipo", []))

    partes.extend(perfil.get("priorizar", []))
    partes.extend(perfil.get("tipo_de_cargo_prioritario", []))

    conocimientos = perfil.get("conocimientos", [])

    if isinstance(conocimientos, list):
        partes.extend(conocimientos)

    return " ".join(str(x) for x in partes)


# ============================================================
# DETECTAR UBICACIÓN
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
# DETECTAR CARGOS COINCIDENTES
# ============================================================

def analizar_cargo(oferta, perfil):

    titulo = normalizar(oferta.get("titulo", ""))

    cargos = perfil.get("tipo_de_cargo_prioritario", [])

    coincidencias = []

    for cargo in cargos:

        palabras = normalizar(cargo).split()

        palabras_utiles = [
            palabra
            for palabra in palabras
            if len(palabra) > 3
        ]

        if palabras_utiles:

            coincidencias_utiles = sum(
                1 for palabra in palabras_utiles
                if palabra in titulo
            )

            if coincidencias_utiles >= max(1, len(palabras_utiles) // 2):
                coincidencias.append(cargo)

    return coincidencias


# ============================================================
# CLASIFICAR COMPETENCIA SEGÚN EL PERFIL
# ============================================================

def clasificar_competencias(competencias_oferta, perfil):

    texto_perfil = obtener_texto_perfil(perfil)

    priorizar = perfil.get("priorizar", [])

    texto_priorizado = normalizar(" ".join(priorizar))

    experiencia_real = normalizar(
        " ".join(
            perfil.get("experiencia", {}).get("tipo", [])
        )
    )

    formacion = normalizar(texto_perfil)

    conocimientos = []
    aprendizaje_rapido = []
    brechas_practicas = []

    for competencia in competencias_oferta:

        competencia_normalizada = normalizar(competencia)

        aparece_formacion = (
            competencia_normalizada in formacion
            or competencia_normalizada in texto_priorizado
        )

        aparece_experiencia = (
            competencia_normalizada in experiencia_real
        )

        # ----------------------------------------------------
        # EXPERIENCIA PRÁCTICA REAL
        # ----------------------------------------------------

        if aparece_experiencia:

            conocimientos.append(competencia)
            continue

        # ----------------------------------------------------
        # CONOCIMIENTO / FORMACIÓN
        # ----------------------------------------------------

        if aparece_formacion:

            conocimientos.append(competencia)

            # Estas áreas suelen permitir refuerzo
            # mediante estudio y simulación.
            if competencia in [
                "PLC",
                "HMI",
                "SCADA",
                "automatización",
                "variadores de frecuencia",
                "lectura de planos"
            ]:
                aprendizaje_rapido.append(competencia)

            # Estas áreas requieren normalmente
            # más exposición práctica.
            if competencia in [
                "mantenimiento industrial",
                "diagnóstico de fallas",
                "instrumentación",
                "neumática",
                "hidráulica"
            ]:
                brechas_practicas.append(competencia)

            continue

        # ----------------------------------------------------
        # COMPETENCIA NO RESPALDADA POR EL PERFIL
        # ----------------------------------------------------

        if competencia in [
            "PLC",
            "HMI",
            "SCADA",
            "automatización",
            "variadores de frecuencia",
            "lectura de planos"
        ]:

            aprendizaje_rapido.append(competencia)

        else:

            brechas_practicas.append(competencia)

    return {
        "conocimientos_relacionados": conocimientos,
        "aprendizaje_rapido": aprendizaje_rapido,
        "brechas_practicas": brechas_practicas
    }


# ============================================================
# ANALIZAR UNA OFERTA
# ============================================================

def analizar_oferta(oferta, perfil):

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

    experiencia = detectar_experiencia(texto)

    anos_solicitados = extraer_anos_experiencia(texto)

    meses_perfil = obtener_meses_experiencia(perfil)

    clasificacion = clasificar_competencias(
        competencias,
        perfil
    )

    ubicacion = analizar_ubicacion(
        oferta,
        perfil
    )

    cargos = analizar_cargo(
        oferta,
        perfil
    )

    return {
        "competencias_detectadas": competencias,
        "experiencia_detectada": experiencia,
        "anos_experiencia_solicitados": anos_solicitados,
        "experiencia_perfil": {
            "meses_aproximados": meses_perfil,
            "anos_aproximados": round(meses_perfil / 12, 2)
        },
        "ubicacion": ubicacion,
        "cargos_coincidentes": cargos,
        **clasificacion
    }


# ============================================================
# CALCULAR COMPATIBILIDAD
# ============================================================

def calcular_compatibilidad(oferta, analisis, perfil):

    puntaje = 0

    fortalezas = []
    brechas = []

    competencias = analisis["competencias_detectadas"]

    conocimientos = analisis["conocimientos_relacionados"]

    aprendizaje = analisis["aprendizaje_rapido"]

    brechas_practicas = analisis["brechas_practicas"]

    # --------------------------------------------------------
    # FORMACIÓN
    # --------------------------------------------------------

    profesion = normalizar(
        perfil.get("profesion", "")
    )

    titulo = normalizar(
        oferta.get("titulo", "")
    )

    if any(
        palabra in titulo
        for palabra in [
            "electrico",
            "automatizacion",
            "mantenimiento",
            "instrumentacion",
            "electromecanico"
        ]
    ):

        puntaje += 15

        fortalezas.append(
            "La formación técnica está relacionada con el tipo de cargo."
        )

    elif profesion:

        puntaje += 8

        fortalezas.append(
            "El perfil cuenta con formación técnica relacionada."
        )

    # --------------------------------------------------------
    # SEC
    # --------------------------------------------------------

    certificacion = perfil.get(
        "certificacion_electrica",
        ""
    )

    if certificacion:

        texto_certificacion = normalizar(
            str(certificacion)
        )

        if "clase d" in texto_certificacion:

            puntaje += 5

            fortalezas.append(
                "El perfil cuenta con preparación para SEC Clase D; "
                "la certificación todavía está en trámite."
            )

    # --------------------------------------------------------
    # COMPETENCIAS
    # --------------------------------------------------------

    for competencia in conocimientos:

        if competencia in competencias:

            puntaje += 8

            fortalezas.append(
                f"El perfil presenta conocimientos relacionados con {competencia}."
            )

    # --------------------------------------------------------
    # UBICACIÓN
    # --------------------------------------------------------

    if analisis["ubicacion"]["zona_prioritaria"]:

        puntaje += 10

        fortalezas.append(
            f"La ubicación ({analisis['ubicacion']['ubicacion_oferta']}) "
            "está dentro de las zonas prioritarias."
        )

    # --------------------------------------------------------
    # CARGO
    # --------------------------------------------------------

    if analisis["cargos_coincidentes"]:

        puntaje += 10

        fortalezas.append(
            "El tipo de cargo coincide con uno o más cargos "
            "prioritarios del perfil."
        )

    # --------------------------------------------------------
    # EXPERIENCIA
    # --------------------------------------------------------

    meses_perfil = analisis["experiencia_perfil"][
        "meses_aproximados"
    ]

    anos_solicitados = analisis[
        "anos_experiencia_solicitados"
    ]

    if anos_solicitados is not None:

        meses_solicitados = anos_solicitados * 12

        if meses_perfil >= meses_solicitados:

            puntaje += 15

            fortalezas.append(
                "La experiencia disponible cumple aproximadamente "
                "con la experiencia solicitada."
            )

        else:

            diferencia = meses_solicitados - meses_perfil

            brechas.append(
                f"La oferta solicita aproximadamente "
                f"{anos_solicitados:g} año(s) de experiencia; "
                f"el perfil registra aproximadamente "
                f"{meses_perfil:g} meses."
            )

            # Penalización progresiva.
            if diferencia <= 6:
                puntaje -= 5

            elif diferencia <= 12:
                puntaje -= 12

            elif diferencia <= 24:
                puntaje -= 20

            else:
                puntaje -= 30

    # --------------------------------------------------------
    # BRECHAS PRÁCTICAS
    # --------------------------------------------------------

    for competencia in brechas_practicas:

        brechas.append(competencia)

    # --------------------------------------------------------
    # APRENDIZAJE RÁPIDO
    # --------------------------------------------------------

    if anos_solicitados is not None:

        diferencia_meses = (
            anos_solicitados * 12
        ) - meses_perfil

        if 0 < diferencia_meses <= 12:

            aprendizaje.insert(
                0,
                "La diferencia de experiencia no es demasiado grande; "
                "conviene postular igualmente si el resto de los "
                "requisitos encaja."
            )

    # --------------------------------------------------------
    # LIMITAR PUNTAJE
    # --------------------------------------------------------

    puntaje = max(
        0,
        min(100, puntaje)
    )

    # --------------------------------------------------------
    # PROBABILIDAD
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

        prioridad = "ALTA"
        recomendacion = "POSTULAR"

    elif puntaje >= 65:

        prioridad = "MEDIA-ALTA"
        recomendacion = (
            "POSTULAR SI EL CARGO ACEPTA PERFILES JUNIOR "
            "O EN DESARROLLO"
        )

    elif puntaje >= 50:

        prioridad = "MEDIA"
        recomendacion = (
            "POSTULAR SI LOS REQUISITOS NO SON EXCLUYENTES"
        )

    else:

        prioridad = "BAJA"
        recomendacion = (
            "PRIORIZAR OTRAS OFERTAS CON MAYOR COMPATIBILIDAD"
        )

    # --------------------------------------------------------
    # DEVOLVER RESULTADO
    # --------------------------------------------------------

    return {
        "puntaje": puntaje,
        "probabilidad_ajuste": probabilidad,
        "prioridad_postulacion": prioridad,
        "recomendacion": recomendacion,
        "fortalezas": fortalezas,
        "conocimientos_relacionados": conocimientos,
        "brechas": brechas,
        "aprendizaje_rapido": aprendizaje,
        "brechas_practicas": brechas_practicas
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

        analisis = analizar_oferta(
            oferta,
            perfil
        )

        compatibilidad = calcular_compatibilidad(
            oferta,
            analisis,
            perfil
        )

        analisis["compatibilidad"] = compatibilidad

        oferta["analisis"] = analisis

        # ----------------------------------------------------
        # TENDENCIAS
        # ----------------------------------------------------

        for competencia in analisis[
            "competencias_detectadas"
        ]:

            contador_competencias[
                competencia
            ] += 1

        for experiencia in analisis[
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

    # ========================================================
    # GUARDAR TENDENCIAS
    # ========================================================

    historial.setdefault(
        "tendencias",
        {}
    )

    historial[
        "tendencias"
    ]["competencias"] = dict(
        contador_competencias.most_common()
    )

    historial[
        "tendencias"
    ]["experiencia_requerida"] = dict(
        contador_experiencia.most_common()
    )

    historial[
        "tendencias"
    ]["ubicaciones"] = dict(
        contador_ubicaciones.most_common()
    )

    historial[
        "tendencias"
    ]["cargos"] = dict(
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
                contador_competencias.most_common(10)
            ),

        "experiencia_mas_solicitada":
            dict(
                contador_experiencia.most_common()
            ),

        "ubicaciones_mas_repetidas":
            dict(
                contador_ubicaciones.most_common(10)
            ),

        "cargos_mas_repetidos":
            dict(
                contador_cargos.most_common(10)
            )
    }

    historial[
        "ultima_actualizacion"
    ] = "actualizado automáticamente"

    # ========================================================
    # GUARDAR JSON
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
        f"Ofertas analizadas: {ofertas_analizadas}"
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
