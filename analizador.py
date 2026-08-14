import json
import re
import unicodedata
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
        "electrica industrial",
        "electrico industrial",
        "electricista industrial",
        "electricidad"
    ],

    "mantenimiento industrial": [
        "mantenimiento industrial",
        "mantencion industrial",
        "mantenimiento"
    ],

    "mantenimiento preventivo": [
        "mantenimiento preventivo",
        "mantencion preventiva"
    ],

    "mantenimiento correctivo": [
        "mantenimiento correctivo",
        "mantencion correctiva"
    ],

    "tableros eléctricos": [
        "tablero electrico",
        "tableros electricos",
        "tableros eléctricos"
    ],

    "lectura de planos": [
        "lectura de planos",
        "interpretacion de planos",
        "interpretación de planos",
        "planos electricos",
        "planos eléctricos"
    ],

    "PLC": [
        "plc",
        "controlador logico programable",
        "controlador programable"
    ],

    "variadores de frecuencia": [
        "variador de frecuencia",
        "variadores de frecuencia",
        "vfd",
        "drive"
    ],

    "automatización": [
        "automatizacion",
        "automatización",
        "control automatico",
        "control automático"
    ],

    "instrumentación": [
        "instrumentacion",
        "instrumentación",
        "instrumentista",
        "instrumentos industriales"
    ],

    "neumática": [
        "neumatica",
        "neumática",
        "sistemas neumaticos",
        "sistemas neumáticos"
    ],

    "hidráulica": [
        "hidraulica",
        "hidráulica",
        "sistemas hidraulicos",
        "sistemas hidráulicos"
    ],

    "diagnóstico de fallas": [
        "diagnostico de fallas",
        "diagnóstico de fallas",
        "deteccion de fallas",
        "detección de fallas",
        "resolucion de fallas",
        "resolución de fallas"
    ],

    "HMI": [
        "hmi",
        "interfaz hombre maquina",
        "interfaz hombre máquina"
    ],

    "SCADA": [
        "scada"
    ],

    "sensores": [
        "sensores",
        "sensor industrial"
    ],

    "motores eléctricos": [
        "motor electrico",
        "motor eléctrico",
        "motores electricos",
        "motores eléctricos"
    ],

    "seguridad eléctrica": [
        "seguridad electrica",
        "seguridad eléctrica",
        "procedimientos electricos",
        "procedimientos eléctricos"
    ],

    "canalizaciones": [
        "canalizacion",
        "canalizaciones",
        "canaleta",
        "canaletas",
        "bandeja",
        "bandejas"
    ],

    "cableado": [
        "cableado",
        "cables",
        "conexionado",
        "conexionado electrico"
    ],

    "fuerza y control": [
        "fuerza y control",
        "circuitos de fuerza",
        "circuitos de control",
        "circuito de fuerza",
        "circuito de control"
    ],

    "arranque de motores": [
        "arranque directo",
        "arranque estrella triangulo",
        "estrella triangulo",
        "estrella-triangulo",
        "arranque de motores"
    ]
}


# ============================================================
# EXPERIENCIA SOLICITADA
# ============================================================

def detectar_experiencia_solicitada(texto):
    """
    Busca la experiencia solicitada en una oferta.
    Devuelve el máximo de años detectado.
    """

    texto = normalizar(texto)

    # Casos de "sin experiencia"
    patrones_sin_experiencia = [
        "sin experiencia",
        "no requiere experiencia",
        "no se requiere experiencia",
        "sin requerir experiencia",
        "recien egresado",
        "recién egresado"
    ]

    for patron in patrones_sin_experiencia:
        if normalizar(patron) in texto:
            return 0

    # Buscar expresiones como:
    # 1 año
    # 2 años
    # 3 años
    # experiencia de 2 años
    # experiencia mínima de 2 años
    encontrados = re.findall(
        r"(?:(?:experiencia|experiencia minima de|experiencia mínima de)\s*)?"
        r"(\d+(?:[.,]\d+)?)\s*(?:años?|anos?)",
        texto
    )

    if encontrados:
        valores = []

        for numero in encontrados:
            try:
                valores.append(float(numero.replace(",", ".")))
            except ValueError:
                pass

        if valores:
            return max(valores)

    # Buscar "6 meses"
    meses = re.findall(
        r"(\d+(?:[.,]\d+)?)\s*mes(?:es)?",
        texto
    )

    if meses:
        valores_meses = []

        for numero in meses:
            try:
                valores_meses.append(
                    float(numero.replace(",", ".")) / 12
                )
            except ValueError:
                pass

        if valores_meses:
            return max(valores_meses)

    # Casos escritos con palabras
    palabras_experiencia = {
        "un año": 1,
        "dos años": 2,
        "tres años": 3,
        "cuatro años": 4,
        "cinco años": 5
    }

    for patron, valor in palabras_experiencia.items():
        if patron in texto:
            return valor

    return None


# ============================================================
# NORMALIZAR TEXTO
# ============================================================

def normalizar(texto):

    texto = str(texto).lower()

    texto = unicodedata.normalize(
        "NFD",
        texto
    )

    texto = "".join(
        caracter
        for caracter in texto
        if unicodedata.category(caracter) != "Mn"
    )

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
# EXTRAER TEXTO DE UNA OFERTA
# ============================================================

def texto_oferta(oferta):

    campos = [
        "titulo",
        "empresa",
        "ubicacion",
        "descripcion",
        "requisitos"
    ]

    partes = []

    for campo in campos:

        valor = oferta.get(campo, "")

        if valor:
            partes.append(str(valor))

    return " ".join(partes)


# ============================================================
# OBTENER DATOS DEL PERFIL
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
# OBTENER EXPERIENCIA DEL PERFIL
# ============================================================

def experiencia_perfil(perfil):

    experiencia = perfil.get(
        "experiencia",
        {}
    )

    meses = experiencia.get(
        "meses_aproximados",
        0
    )

    try:
        meses = float(meses)
    except (ValueError, TypeError):
        meses = 0

    return {
        "meses_aproximados": meses,
        "anos_aproximados": round(meses / 12, 2)
    }


# ============================================================
# OBTENER COMPETENCIAS DEL PERFIL
# ============================================================

def competencias_del_perfil(perfil):

    resultado = set()

    conocimientos = perfil.get(
        "conocimientos",
        {}
    )

    for categoria, valores in conocimientos.items():

        if isinstance(valores, list):

            for valor in valores:

                resultado.add(
                    normalizar(valor)
                )

    experiencia = perfil.get(
        "experiencia",
        {}
    )

    for campo in [
        "experiencia_practica_real",
        "experiencia_practica_academica"
    ]:

        valores = experiencia.get(
            campo,
            []
        )

        if isinstance(valores, list):

            for valor in valores:

                resultado.add(
                    normalizar(valor)
                )

    return resultado


# ============================================================
# BUSCAR SI UNA COMPETENCIA ESTÁ EN EL PERFIL
# ============================================================

def competencia_en_perfil(
    competencia,
    perfil
):

    comp = normalizar(
        competencia
    )

    conocimientos = perfil.get(
        "conocimientos",
        {}
    )

    for valores in conocimientos.values():

        if not isinstance(valores, list):
            continue

        for valor in valores:

            texto = normalizar(valor)

            if comp in texto or texto in comp:
                return True

    return False


# ============================================================
# BUSCAR COMPETENCIAS EN EL PERFIL
# ============================================================

def clasificar_competencias(
    competencias_oferta,
    perfil
):

    nivel_practico = perfil.get(
        "nivel_practico",
        {}
    )

    practicas = {
        normalizar(x)
        for x in nivel_practico.get(
            "alto",
            []
        )
    }

    practicas.update(
        normalizar(x)
        for x in nivel_practico.get(
            "medio",
            []
        )
    )

    academicas = {
        normalizar(x)
        for x in nivel_practico.get(
            "academico",
            []
        )
    }

    requieren_practica = {
        normalizar(x)
        for x in nivel_practico.get(
            "requiere_experiencia_terreno",
            []
        )
    }

    relacionadas = []
    brechas = []
    aprendizaje_rapido = []
    brechas_practicas = []

    for competencia in competencias_oferta:

        comp = normalizar(
            competencia
        )

        # ----------------------------------------------------
        # EXPERIENCIA PRÁCTICA
        # ----------------------------------------------------

        tiene_practica = False

        for elemento in practicas:

            if comp in elemento or elemento in comp:
                tiene_practica = True
                break

        if tiene_practica:
            relacionadas.append(
                competencia
            )
            continue

        # ----------------------------------------------------
        # EXPERIENCIA ACADÉMICA
        # ----------------------------------------------------

        tiene_academica = False

        for elemento in academicas:

            if comp in elemento or elemento in comp:
                tiene_academica = True
                break

        if tiene_academica:

            aprendizaje_rapido.append(
                competencia
            )

            continue

        # ----------------------------------------------------
        # COMPETENCIA QUE REQUIERE TERRENO
        # ----------------------------------------------------

        requiere_terreno = False

        for elemento in requieren_practica:

            if comp in elemento or elemento in comp:
                requiere_terreno = True
                break

        if requiere_terreno:

            brechas_practicas.append(
                competencia
            )

            continue

        # ----------------------------------------------------
        # CONOCIMIENTO RELACIONADO
        # ----------------------------------------------------

        if competencia_en_perfil(
            competencia,
            perfil
        ):

            relacionadas.append(
                competencia
            )

        else:

            brechas.append(
                competencia
            )

    return {
        "conocimientos_relacionados": relacionadas,
        "aprendizaje_rapido": aprendizaje_rapido,
        "brechas": brechas,
        "brechas_practicas": brechas_practicas
    }


# ============================================================
# DETECTAR UBICACIÓN
# ============================================================

def analizar_ubicacion(
    ubicacion,
    perfil
):

    zonas = perfil.get(
        "objetivo",
        {}
    ).get(
        "zona_prioritaria",
        []
    )

    ubicacion_texto = normalizar(
        ubicacion
    )

    coincidencia = None

    for zona in zonas:

        if normalizar(zona) in ubicacion_texto:

            coincidencia = zona
            break

    return {
        "ubicacion_oferta": ubicacion,
        "zona_prioritaria": coincidencia is not None,
        "zona_coincidente": coincidencia
    }


# ============================================================
# ANALIZAR CARGO
# ============================================================

def analizar_cargo(
    titulo,
    perfil
):

    cargos = perfil.get(
        "tipo_de_cargo_prioritario",
        []
    )

    titulo_normalizado = normalizar(
        titulo
    )

    coincidencias = []

    for cargo in cargos:

        cargo_normalizado = normalizar(
            cargo
        )

        palabras = [
            palabra
            for palabra in cargo_normalizado.split()
            if len(palabra) > 3
        ]

        coincidencias_palabras = sum(
            1
            for palabra in palabras
            if palabra in titulo_normalizado
        )

        if coincidencias_palabras >= 2:

            coincidencias.append(
                cargo
            )

    return coincidencias


# ============================================================
# ANALIZAR EXPERIENCIA
# ============================================================

def analizar_experiencia(
    anos_solicitados,
    perfil
):

    experiencia = experiencia_perfil(
        perfil
    )

    meses = experiencia[
        "meses_aproximados"
    ]

    if anos_solicitados is None:

        return {
            "brecha": 0,
            "mensaje": "La oferta no indica claramente una cantidad de años de experiencia."
        }

    experiencia_solicitada_meses = (
        anos_solicitados * 12
    )

    brecha_meses = max(
        0,
        experiencia_solicitada_meses - meses
    )

    if anos_solicitados == 0:

        mensaje = (
            "La oferta no exige experiencia profesional previa."
        )

    elif brecha_meses == 0:

        mensaje = (
            "La experiencia registrada en el perfil alcanza "
            "el mínimo indicado por la oferta."
        )

    else:

        mensaje = (
            f"La oferta solicita aproximadamente "
            f"{anos_solicitados:g} año(s) de experiencia; "
            f"el perfil registra aproximadamente "
            f"{meses:g} meses."
        )

    return {
        "brecha_meses": round(
            brecha_meses,
            1
        ),
        "mensaje": mensaje
    }


# ============================================================
# CALCULAR COMPATIBILIDAD
# ============================================================

def calcular_compatibilidad(
    oferta,
    perfil,
    competencias,
    clasificacion,
    ubicacion,
    cargos,
    experiencia
):

    puntaje = 0
    fortalezas = []

    brechas = list(
        clasificacion["brechas"]
    )

    aprendizaje_rapido = list(
        clasificacion["aprendizaje_rapido"]
    )

    brechas_practicas = list(
        clasificacion["brechas_practicas"]
    )

    # --------------------------------------------------------
    # FORMACIÓN
    # --------------------------------------------------------

    profesion = normalizar(
        perfil.get(
            "profesion",
            ""
        )
    )

    titulo = normalizar(
        oferta.get(
            "titulo",
            ""
        )
    )

    texto = normalizar(
        texto_oferta(oferta)
    )

    palabras_formacion = [
        "automatizacion",
        "control",
        "electricidad",
        "electrico",
        "mantenimiento",
        "electromecanico"
    ]

    if any(
        palabra in profesion
        and palabra in texto
        for palabra in palabras_formacion
    ):

        puntaje += 20

        fortalezas.append(
            "La formación técnica está relacionada con el área del cargo."
        )

    # --------------------------------------------------------
    # SEC
    # --------------------------------------------------------

    certificacion = perfil.get(
        "certificacion_electrica",
        {}
    )

    if isinstance(
        certificacion,
        dict
    ):

        if normalizar(
            certificacion.get(
                "tipo",
                ""
            )
        ) == "sec clase d":

            if normalizar(
                "electrico"
            ) in texto:

                puntaje += 10

                fortalezas.append(
                    "El perfil cuenta con preparación para SEC Clase D; "
                    "la certificación todavía está en trámite."
                )

    # --------------------------------------------------------
    # COMPETENCIAS
    # --------------------------------------------------------

    total_competencias = len(
        competencias
    )

    if total_competencias > 0:

        relacionadas = len(
            clasificacion[
                "conocimientos_relacionados"
            ]
        )

        academicas = len(
            aprendizaje_rapido
        )

        practicas = len(
            brechas_practicas
        )

        # Conocimientos que realmente coinciden
        puntaje += min(
            30,
            relacionadas * 6
        )

        # Conocimiento académico suma, pero menos
        puntaje += min(
            12,
            academicas * 3
        )

        # No premiamos como dominio aquello
        # que requiere experiencia práctica.
        puntaje -= min(
            12,
            practicas * 2
        )

        for competencia in clasificacion[
            "conocimientos_relacionados"
        ]:

            fortalezas.append(
                f"El perfil presenta conocimientos relacionados con {competencia}."
            )

    # --------------------------------------------------------
    # UBICACIÓN
    # --------------------------------------------------------

    if ubicacion[
        "zona_prioritaria"
    ]:

        puntaje += 10

        fortalezas.append(
            f"La ubicación ({ubicacion['ubicacion_oferta']}) "
            "está dentro de las zonas prioritarias."
        )

    # --------------------------------------------------------
    # CARGO
    # --------------------------------------------------------

    if cargos:

        puntaje += 15

        fortalezas.append(
            "El tipo de cargo coincide con uno o más cargos "
            "prioritarios del perfil."
        )

    # --------------------------------------------------------
    # EXPERIENCIA
    # --------------------------------------------------------

    anos_solicitados = oferta.get(
        "_anos_experiencia_solicitados"
    )

    if anos_solicitados is not None:

        if anos_solicitados == 0:

            puntaje += 10

            fortalezas.append(
                "La oferta no exige experiencia profesional previa."
            )

        else:

            if experiencia["brecha_meses"] <= 6:

                puntaje += 5

            elif experiencia["brecha_meses"] <= 12:

                puntaje += 2

            else:

                puntaje -= 5

            brechas.append(
                experiencia["mensaje"]
            )

    # --------------------------------------------------------
    # LIMITAR PUNTAJE
    # --------------------------------------------------------

    puntaje = max(
        0,
        min(
            100,
            round(puntaje)
        )
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
    # PRIORIDAD DE POSTULACIÓN
    # --------------------------------------------------------

    if puntaje >= 80:

        prioridad = "ALTA"

        recomendacion = (
            "POSTULAR"
        )

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
    # MENSAJES DE EXPERIENCIA
    # --------------------------------------------------------

    if (
        anos_solicitados is not None
        and anos_solicitados > 0
        and experiencia["brecha_meses"] <= 12
    ):

        aprendizaje_rapido.append(
            "La diferencia de experiencia no es demasiado grande; "
            "conviene postular igualmente si el resto de los "
            "requisitos encaja."
        )

    # --------------------------------------------------------
    # BRECHAS PRÁCTICAS
    # --------------------------------------------------------

    if brechas_practicas:

        brechas_practicas.insert(
            0,
            "La principal diferencia es la experiencia práctica "
            "acumulada en terreno."
        )

    return {
        "puntaje": puntaje,
        "probabilidad_ajuste": probabilidad,
        "prioridad_postulacion": prioridad,
        "recomendacion": recomendacion,
        "fortalezas": fortalezas,
        "conocimientos_relacionados":
            clasificacion[
                "conocimientos_relacionados"
            ],
        "brechas": eliminar_duplicados(
            brechas
        ),
        "aprendizaje_rapido":
            eliminar_duplicados(
                aprendizaje_rapido
            ),
        "brechas_practicas":
            eliminar_duplicados(
                brechas_practicas
            )
    }


# ============================================================
# ELIMINAR DUPLICADOS
# ============================================================

def eliminar_duplicados(lista):

    resultado = []

    for elemento in lista:

        if elemento not in resultado:

            resultado.append(
                elemento
            )

    return resultado


# ============================================================
# ANALIZAR UNA OFERTA
# ============================================================

def analizar_oferta(
    oferta,
    perfil
):

    texto = texto_oferta(
        oferta
    )

    competencias = detectar_competencias(
        texto
    )

    anos_solicitados = (
        detectar_experiencia_solicitada(
            texto
        )
    )

    oferta[
        "_anos_experiencia_solicitados"
    ] = anos_solicitados

    experiencia = analizar_experiencia(
        anos_solicitados,
        perfil
    )

    ubicacion = analizar_ubicacion(
        oferta.get(
            "ubicacion",
            ""
        ),
        perfil
    )

    cargos = analizar_cargo(
        oferta.get(
            "titulo",
            ""
        ),
        perfil
    )

    clasificacion = clasificar_competencias(
        competencias,
        perfil
    )

    compatibilidad = calcular_compatibilidad(
        oferta,
        perfil,
        competencias,
        clasificacion,
        ubicacion,
        cargos,
        experiencia
    )

    # --------------------------------------------------------
    # ELIMINAR CAMPO INTERNO
    # --------------------------------------------------------

    if "_anos_experiencia_solicitados" in oferta:

        del oferta[
            "_anos_experiencia_solicitados"
        ]

    return {
        "competencias_detectadas": competencias,

        "experiencia_detectada": (
            experiencia_detectada_legible(
                anos_solicitados
            )
        ),

        "anos_experiencia_solicitados":
            anos_solicitados,

        "experiencia_perfil":
            experiencia_perfil(
                perfil
            ),

        "ubicacion":
            ubicacion,

        "cargos_coincidentes":
            cargos,

        "compatibilidad":
            compatibilidad
    }


# ============================================================
# EXPERIENCIA LEGIBLE
# ============================================================

def experiencia_detectada_legible(
    anos
):

    if anos is None:
        return []

    if anos == 0:
        return [
            "sin experiencia"
        ]

    if anos == 1:
        return [
            "1 año"
        ]

    if anos == int(anos):
        return [
            f"{int(anos)} años"
        ]

    return [
        f"{anos} años"
    ]


# ============================================================
# ACTUALIZAR TENDENCIAS
# ============================================================

def actualizar_tendencias(
    historial
):

    contador_competencias = Counter()
    contador_experiencia = Counter()
    contador_ubicaciones = Counter()
    contador_cargos = Counter()

    ofertas = historial.get(
        "ofertas",
        []
    )

    for oferta in ofertas:

        analisis = oferta.get(
            "analisis",
            {}
        )

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

            elif experiencia == 1:

                clave = "1 año"

            elif experiencia == int(
                experiencia
            ):

                clave = f"{int(experiencia)} años"

            else:

                clave = f"{experiencia} años"

            contador_experiencia[
                clave
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

    historial.setdefault(
        "tendencias",
        {}
    )

    historial[
        "tendencias"
    ] = {

        "competencias":
            dict(
                contador_competencias.most_common()
            ),

        "experiencia_requerida":
            dict(
                contador_experiencia.most_common()
            ),

        "ubicaciones":
            dict(
                contador_ubicaciones.most_common()
            ),

        "cargos":
            dict(
                contador_cargos.most_common()
            )
    }


# ============================================================
# RESUMEN DEL MERCADO
# ============================================================

def crear_resumen_mercado(
    historial
):

    tendencias = historial.get(
        "tendencias",
        {}
    )

    return {

        "ofertas_analizadas":
            len(
                historial.get(
                    "ofertas",
                    []
                )
            ),

        "competencias_mas_solicitadas":
            tendencias.get(
                "competencias",
                {}
            ),

        "experiencia_mas_solicitada":
            tendencias.get(
                "experiencia_requerida",
                {}
            ),

        "ubicaciones_mas_repetidas":
            tendencias.get(
                "ubicaciones",
                {}
            ),

        "cargos_mas_repetidos":
            tendencias.get(
                "cargos",
                {}
            )
    }


# ============================================================
# PROCESAR HISTORIAL COMPLETO
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

            historial = json.load(
                archivo
            )

    except FileNotFoundError:

        print(
            "No se encontró historial.json"
        )

        return

    # --------------------------------------------------------
    # CARGAR PERFIL
    # --------------------------------------------------------

    perfil = cargar_perfil()

    if not perfil:

        print(
            "No se pudo cargar perfil.json"
        )

        return

    # --------------------------------------------------------
    # ANALIZAR OFERTAS
    # --------------------------------------------------------

    ofertas = historial.get(
        "ofertas",
        []
    )

    ofertas_analizadas = 0

    for oferta in ofertas:

        oferta["analisis"] = analizar_oferta(
            oferta,
            perfil
        )

        ofertas_analizadas += 1

    # --------------------------------------------------------
    # TENDENCIAS
    # --------------------------------------------------------

    actualizar_tendencias(
        historial
    )

    # --------------------------------------------------------
    # RESUMEN
    # --------------------------------------------------------

    historial[
        "resumen_mercado"
    ] = crear_resumen_mercado(
        historial
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

    # --------------------------------------------------------
    # MOSTRAR RESULTADO EN ACTIONS
    # --------------------------------------------------------

    print(
        "=========================================="
    )

    print(
        "       INVESTIGADOR LABORAL"
    )

    print(
        "=========================================="
    )

    print(
        f"Ofertas analizadas: {ofertas_analizadas}"
    )

    experiencia = experiencia_perfil(
        perfil
    )

    print(
        f"Experiencia del perfil: "
        f"{experiencia['meses_aproximados']} meses"
    )

    print(
        "\nCOMPETENCIAS MÁS SOLICITADAS:"
    )

    for competencia, cantidad in (
        historial[
            "tendencias"
        ][
            "competencias"
        ].items()
    ):

        print(
            f"- {competencia}: "
            f"{cantidad} ofertas"
        )

    print(
        "\nEXPERIENCIA SOLICITADA:"
    )

    for nivel, cantidad in (
        historial[
            "tendencias"
        ][
            "experiencia_requerida"
        ].items()
    ):

        print(
            f"- {nivel}: "
            f"{cantidad} ofertas"
        )

    print(
        "\nRESULTADO DE LAS OFERTAS:"
    )

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
            f"Compatibilidad: "
            f"{compatibilidad.get('puntaje', 0)}/100"
        )

        print(
            f"Probabilidad: "
            f"{compatibilidad.get('probabilidad_ajuste', 'N/D')}"
        )

        print(
            f"Prioridad: "
            f"{compatibilidad.get('prioridad_postulacion', 'N/D')}"
        )

        print(
            f"Recomendación: "
            f"{compatibilidad.get('recomendacion', 'N/D')}"
        )

    print(
        "\n=========================================="
    )

    print(
        "Análisis terminado correctamente."
    )

    print(
        "=========================================="
    )


# ============================================================
# EJECUTAR
# ============================================================

if __name__ == "__main__":

    analizar_historial()
