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
        "mantención industrial"
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
    ],

    "contactores": [
        "contactor",
        "contactores"
    ],

    "protecciones eléctricas": [
        "protecciones eléctricas",
        "protecciones electricas",
        "interruptores automáticos",
        "disyuntores",
        "guardamotores"
    ],

    "arranque de motores": [
        "arranque directo",
        "arranque de motor",
        "estrella triángulo",
        "estrella triangulo"
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

    "6 meses": [
        "6 meses de experiencia",
        "6 meses experiencia",
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
# COMPETENCIAS QUE REQUIEREN MÁS EXPERIENCIA PRÁCTICA
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
    "hidráulica",
    "contactores",
    "protecciones eléctricas"
}


# ============================================================
# COMPETENCIAS QUE PUEDEN REFORZARSE MÁS RÁPIDAMENTE
# ============================================================

COMPETENCIAS_APRENDIZAJE_RAPIDO = {
    "PLC",
    "HMI",
    "SCADA",
    "lectura de planos",
    "automatización",
    "seguridad eléctrica",
    "sensores",
    "arranque de motores"
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
# CONVERTIR EXPERIENCIA A AÑOS
# ============================================================

def experiencia_a_anos(experiencias):

    if not experiencias:
        return None

    valores = []

    for experiencia in experiencias:

        if experiencia == "sin experiencia":
            valores.append(0)

        elif experiencia == "6 meses":
            valores.append(0.5)

        elif experiencia == "1 año":
            valores.append(1)

        elif experiencia == "2 años":
            valores.append(2)

        elif experiencia == "3 años o más":
            valores.append(3)

    if not valores:
        return None

    return max(valores)


# ============================================================
# OBTENER MESES DE EXPERIENCIA DEL PERFIL
# ============================================================

def obtener_meses_perfil(perfil):

    experiencia = perfil.get("experiencia", {})

    meses = experiencia.get("meses_aproximados", 0)

    try:
        return float(meses)
    except (TypeError, ValueError):
        return 0


# ============================================================
# OBTENER NOMBRE DE PROFESIÓN
# ============================================================

def obtener_profesion(perfil):

    profesion = perfil.get("profesion", "")

    if isinstance(profesion, dict):
        return str(profesion.get("nombre", ""))

    return str(profesion)


# ============================================================
# INFORMACIÓN SEC
# ============================================================

def analizar_sec(perfil):

    certificacion = perfil.get("certificacion_electrica", "")

    if isinstance(certificacion, dict):

        tipo = certificacion.get("tipo", "")
        estado = certificacion.get("estado", "")
        observacion = certificacion.get("observacion", "")

        return {
            "tipo": tipo,
            "estado": estado,
            "observacion": observacion
        }

    return {
        "tipo": str(certificacion),
        "estado": "No especificado",
        "observacion": ""
    }


# ============================================================
# UBICACIÓN
# ============================================================

def analizar_ubicacion(oferta, perfil):

    ubicacion_oferta = str(oferta.get("ubicacion", "")).strip()

    objetivo = perfil.get("objetivo", {})

    zonas = objetivo.get("zona_prioritaria", [])

    if not isinstance(zonas, list):
        zonas = []

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
# DETECTAR CARGOS COMPATIBLES
# ============================================================

def detectar_cargos(oferta, perfil):

    titulo = normalizar(oferta.get("titulo", ""))

    cargos_prioritarios = perfil.get(
        "tipo_de_cargo_prioritario",
        []
    )

    encontrados = []

    palabras_relacionadas = {
        "electrico": [
            "eléctrico",
            "electrico",
            "electricista"
        ],

        "mantenimiento": [
            "mantenimiento",
            "mantención"
        ],

        "automatizacion": [
            "automatización",
            "automatizacion"
        ],

        "instrumentacion": [
            "instrumentación",
            "instrumentacion",
            "instrumentista"
        ],

        "electromecanico": [
            "electromecánico",
            "electromecanico"
        ],

        "ayudante": [
            "ayudante"
        ]
    }

    for cargo in cargos_prioritarios:

        cargo_normalizado = normalizar(cargo)

        if cargo_normalizado in titulo:
            encontrados.append(cargo)
            continue

        for palabra_clave, variantes in palabras_relacionadas.items():

            if palabra_clave in cargo_normalizado:

                for variante in variantes:

                    if normalizar(variante) in titulo:
                        encontrados.append(cargo)
                        break

                break

    return encontrados


# ============================================================
# PERFIL TÉCNICO RELACIONADO CON LA OFERTA
# ============================================================

def obtener_prioridades_tecnicas(perfil):

    prioridades = perfil.get("priorizar", [])

    if not isinstance(prioridades, list):
        return []

    resultado = []

    for item in prioridades:

        texto = normalizar(item)

        for competencia in COMPETENCIAS:

            if normalizar(competencia) in texto:
                resultado.append(competencia)

    return list(dict.fromkeys(resultado))


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

    anos_solicitados = experiencia_a_anos(experiencia)

    meses_perfil = obtener_meses_perfil(perfil)

    anos_perfil = meses_perfil / 12

    ubicacion = analizar_ubicacion(
        oferta,
        perfil
    )

    cargos = detectar_cargos(
        oferta,
        perfil
    )

    prioridades_tecnicas = obtener_prioridades_tecnicas(
        perfil
    )

    coincidencias_tecnicas = [
        competencia
        for competencia in competencias
        if competencia in prioridades_tecnicas
    ]

    fortalezas = []
    conocimientos_relacionados = []
    brechas = []
    aprendizaje_rapido = []
    brechas_practicas = []

    # --------------------------------------------------------
    # FORMACIÓN
    # --------------------------------------------------------

    profesion = obtener_profesion(perfil)

    if profesion:

        fortalezas.append(
            "La formación técnica está relacionada con automatización, control y electricidad."
        )

    # --------------------------------------------------------
    # EXPERIENCIA PRÁCTICA
    # --------------------------------------------------------

    if meses_perfil > 0:

        fortalezas.append(
            f"El perfil registra aproximadamente {int(meses_perfil)} meses de experiencia práctica."
        )

    # --------------------------------------------------------
    # SEC
    # --------------------------------------------------------

    sec = analizar_sec(perfil)

    if sec["tipo"]:

        if normalizar(sec["estado"]) == "en tramite":

            fortalezas.append(
                f"{sec['tipo']}: en trámite. La certificación aún no se considera obtenida."
            )

        else:

            fortalezas.append(
                f"El perfil cuenta con referencia a {sec['tipo']}."
            )

    # --------------------------------------------------------
    # COINCIDENCIAS TÉCNICAS
    # --------------------------------------------------------

    for competencia in coincidencias_tecnicas:

        fortalezas.append(
            f"El perfil presenta conocimientos relacionados con {competencia}."
        )

    # --------------------------------------------------------
    # UBICACIÓN
    # --------------------------------------------------------

    if ubicacion["zona_prioritaria"]:

        fortalezas.append(
            f"La ubicación ({ubicacion['ubicacion_oferta']}) está dentro de las zonas prioritarias."
        )

    # --------------------------------------------------------
    # CARGO
    # --------------------------------------------------------

    if cargos:

        fortalezas.append(
            "El tipo de cargo coincide con uno o más cargos prioritarios del perfil."
        )

    # --------------------------------------------------------
    # BRECHAS POR COMPETENCIA
    # --------------------------------------------------------

    for competencia in competencias:

        if competencia not in prioridades_tecnicas:

            if competencia in COMPETENCIAS_PRACTICAS:

                brechas_practicas.append(
                    f"{competencia}: conviene desarrollarla mediante experiencia práctica en terreno."
                )

            elif competencia in COMPETENCIAS_APRENDIZAJE_RAPIDO:

                aprendizaje_rapido.append(
                    f"{competencia}: puede reforzarse mediante estudio, simulación y práctica guiada."
                )

            else:

                brechas.append(competencia)

        else:

            if competencia in COMPETENCIAS_PRACTICAS:

                conocimientos_relacionados.append(
                    competencia
                )

    # --------------------------------------------------------
    # EXPERIENCIA REQUERIDA
    # --------------------------------------------------------

    diferencia_experiencia = None

    if anos_solicitados is not None:

        diferencia_experiencia = (
            anos_solicitados - anos_perfil
        )

        if diferencia_experiencia > 0:

            brechas.append(
                f"La oferta solicita aproximadamente {anos_solicitados:g} año(s) de experiencia; "
                f"el perfil registra aproximadamente {meses_perfil:g} meses."
            )

            if diferencia_experiencia <= 1:

                aprendizaje_rapido.append(
                    "La diferencia de experiencia no es demasiado grande; conviene postular igualmente si el resto de los requisitos encaja."
                )

    # ========================================================
    # CALCULAR PUNTAJE
    # ========================================================

    puntaje = 45

    # Formación
    if profesion:
        puntaje += 10

    # Competencias
    if competencias:

        porcentaje_coincidencia = (
            len(coincidencias_tecnicas) /
            len(competencias)
        )

        puntaje += round(
            porcentaje_coincidencia * 20
        )

    # Ubicación
    if ubicacion["zona_prioritaria"]:
        puntaje += 10

    # Cargo
    if cargos:
        puntaje += 8

    # Experiencia
    if anos_solicitados is not None:

        if anos_solicitados == 0:
            puntaje += 7

        elif diferencia_experiencia is not None:

            if diferencia_experiencia <= 0:
                puntaje += 7

            elif diferencia_experiencia <= 0.5:
                puntaje += 5

            elif diferencia_experiencia <= 1:
                puntaje += 2

            elif diferencia_experiencia <= 2:
                puntaje -= 5

            else:
                puntaje -= 15

    puntaje = max(
        0,
        min(100, puntaje)
    )

    # ========================================================
    # AJUSTE REALISTA DE PROBABILIDAD
    # ========================================================

    if puntaje >= 75:

        probabilidad = "ALTA"

    elif puntaje >= 55:

        probabilidad = "MEDIA"

    else:

        probabilidad = "BAJA"

    # Una exigencia importante de experiencia evita
    # clasificar automáticamente como alta.

    if anos_solicitados is not None:

        if anos_solicitados >= 2 and diferencia_experiencia > 1:

            if probabilidad == "ALTA":
                probabilidad = "MEDIA"

        if anos_solicitados >= 3 and diferencia_experiencia > 2:

            probabilidad = "BAJA"

    # ========================================================
    # RECOMENDACIÓN
    # ========================================================

    if probabilidad == "ALTA":

        recomendacion = "POSTULAR"
        prioridad = "ALTA"

    elif probabilidad == "MEDIA":

        recomendacion = "POSTULAR SI EL CARGO ACEPTA PERFILES JUNIOR O EN DESARROLLO"
        prioridad = "MEDIA-ALTA"

    else:

        recomendacion = "POSTULAR SOLO COMO OPCIÓN DE DESARROLLO SI EL REQUISITO DE EXPERIENCIA ES NEGOCIABLE"
        prioridad = "BAJA"

    # ========================================================
    # DEVOLVER ANÁLISIS
    # ========================================================

    return {
        "competencias_detectadas": competencias,
        "experiencia_detectada": experiencia,
        "anos_experiencia_solicitados": anos_solicitados,
        "experiencia_perfil": {
            "meses_aproximados": meses_perfil,
            "anos_aproximados": round(anos_perfil, 2)
        },
        "ubicacion": ubicacion,
        "cargos_coincidentes": cargos,

        "compatibilidad": {
            "puntaje": puntaje,
            "probabilidad_ajuste": probabilidad,
            "prioridad_postulacion": prioridad,
            "recomendacion": recomendacion,

            "fortalezas": fortalezas,

            "conocimientos_relacionados": conocimientos_relacionados,

            "brechas": brechas,

            "aprendizaje_rapido": aprendizaje_rapido,

            "brechas_practicas": brechas_practicas
        }
    }


# ============================================================
# ANALIZAR HISTORIAL COMPLETO
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

        # Competencias
        for competencia in resultado[
            "competencias_detectadas"
        ]:

            contador_competencias[
                competencia
            ] += 1

        # Experiencia
        for experiencia in resultado[
            "experiencia_detectada"
        ]:

            contador_experiencia[
                experiencia
            ] += 1

        # Ubicación
        ubicacion = oferta.get(
            "ubicacion",
            ""
        )

        if ubicacion:
            contador_ubicaciones[
                ubicacion
            ] += 1

        # Cargo
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

    historial[
        "resumen_mercado"
    ] = {

        "ofertas_analizadas":
            ofertas_analizadas,

        "competencias_mas_solicitadas":
            dict(
                contador_competencias.most_common(15)
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

    # --------------------------------------------------------
    # ACTUALIZACIÓN
    # --------------------------------------------------------

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
    print("==========================================")
    print("       INVESTIGADOR LABORAL")
    print("==========================================")

    print(
        f"Ofertas analizadas: {ofertas_analizadas}"
    )

    print()
    print("COMPETENCIAS MÁS SOLICITADAS:")

    for competencia, cantidad in (
        contador_competencias.most_common()
    ):

        print(
            f"- {competencia}: {cantidad} ofertas"
        )

    print()
    print("EXPERIENCIA SOLICITADA:")

    for nivel, cantidad in (
        contador_experiencia.most_common()
    ):

        print(
            f"- {nivel}: {cantidad} ofertas"
        )

    print()
    print("UBICACIONES MÁS REPETIDAS:")

    for ubicacion, cantidad in (
        contador_ubicaciones.most_common()
    ):

        print(
            f"- {ubicacion}: {cantidad} ofertas"
        )

    print()
    print("CARGOS MÁS REPETIDOS:")

    for cargo, cantidad in (
        contador_cargos.most_common()
    ):

        print(
            f"- {cargo}: {cantidad} ofertas"
        )

    print()
    print("==========================================")
    print("Análisis completado correctamente.")
    print("==========================================")


# ============================================================
# EJECUTAR
# ============================================================

if __name__ == "__main__":

    analizar_historial()
