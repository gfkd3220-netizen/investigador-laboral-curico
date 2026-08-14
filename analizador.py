import json
import re
from collections import Counter


# ============================================================
# CONFIGURACIÓN
# ============================================================

ARCHIVO_HISTORIAL = "historial.json"
ARCHIVO_PERFIL = "perfil.json"


# ============================================================
# COMPETENCIAS Y PALABRAS CLAVE
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
        "tableros electricos",
        "tablero de control"
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
        "controlador programable"
    ],

    "PLC Siemens": [
        "siemens",
        "tia portal",
        "s7-1200",
        "s7-1500",
        "s7 1200",
        "s7 1500"
    ],

    "PLC Delta": [
        "delta plc",
        "plc delta"
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

    "arranque de motores": [
        "arranque directo",
        "estrella triángulo",
        "estrella triangulo",
        "arranque de motor"
    ],

    "seguridad eléctrica": [
        "seguridad eléctrica",
        "seguridad electrica",
        "procedimientos eléctricos",
        "procedimientos electricos"
    ],

    "baja tensión": [
        "baja tensión",
        "baja tension",
        "bt",
        "instalaciones de baja tensión",
        "instalaciones de baja tension"
    ],

    "canalizaciones": [
        "canalización",
        "canalizaciones",
        "canaleta",
        "canaletas",
        "bandeja",
        "bandejas",
        "bandejas portacables"
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

    "3 años": [
        "3 años de experiencia",
        "3 años experiencia",
        "experiencia de 3 años",
        "experiencia 3 años",
        "experiencia mínima de 3 años",
        "experiencia minima de 3 años"
    ],

    "4 años": [
        "4 años de experiencia",
        "4 años experiencia",
        "experiencia de 4 años",
        "experiencia 4 años"
    ],

    "5 años o más": [
        "5 años de experiencia",
        "5 años experiencia",
        "experiencia de 5 años",
        "experiencia 5 años",
        "más de 5 años",
        "mas de 5 años"
    ]
}


# ============================================================
# NORMALIZACIÓN
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
        r"(\d+)\s*años?\s*(?:de)?\s*experiencia",
        r"(\d+)\s*anos?\s*(?:de)?\s*experiencia"
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

    return None


# ============================================================
# DETECTAR UBICACIÓN
# ============================================================

def detectar_ubicacion(oferta, perfil):

    ubicacion = str(oferta.get("ubicacion", "")).strip()

    zonas = perfil.get("objetivo", {}).get(
        "zona_prioritaria",
        []
    )

    ubicacion_normalizada = normalizar(ubicacion)

    coincidente = None

    for zona in zonas:

        if normalizar(zona) in ubicacion_normalizada:
            coincidente = zona
            break

    return {
        "ubicacion_oferta": ubicacion,
        "zona_prioritaria": coincidente is not None,
        "zona_coincidente": coincidente
    }


# ============================================================
# DETECTAR TIPO DE CARGO
# ============================================================

def detectar_cargo(oferta, perfil):

    texto = normalizar(
        str(oferta.get("titulo", "")) + " " +
        str(oferta.get("descripcion", ""))
    )

    cargos = perfil.get(
        "tipo_de_cargo_prioritario",
        []
    )

    encontrados = []

    for cargo in cargos:

        palabras = normalizar(cargo).split()

        if any(palabra in texto for palabra in palabras):
            encontrados.append(cargo)

    return encontrados


# ============================================================
# CONSTRUIR TEXTO COMPLETO DE OFERTA
# ============================================================

def obtener_texto_oferta(oferta):

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

    return texto


# ============================================================
# OBTENER CONOCIMIENTOS DEL PERFIL
# ============================================================

def obtener_conocimientos_perfil(perfil):

    conocimientos = []

    fortalezas = perfil.get("fortalezas", [])

    conocimientos.extend(fortalezas)

    automatizacion = perfil.get(
        "automatizacion_y_control",
        {}
    )

    conocimientos.append("PLC")
    conocimientos.append("variadores de frecuencia")
    conocimientos.append("HMI")
    conocimientos.append("control de motores")

    conocimientos.extend(
        automatizacion.get("control_de_motores", {}).get(
            "conocimientos",
            []
        )
    )

    electricos = perfil.get(
        "conocimientos_electricos",
        {}
    )

    conocimientos.extend(
        electricos.get("conocimientos", [])
    )

    return conocimientos


# ============================================================
# ANALIZAR COMPATIBILIDAD
# ============================================================

def analizar_compatibilidad(
    competencias,
    experiencia_requerida,
    anos_requeridos,
    ubicacion,
    cargos,
    oferta,
    perfil
):

    puntos = 0
    puntos_maximos = 100

    fortalezas = []
    brechas = []
    aprendizaje_rapido = []
    brechas_practicas = []

    # --------------------------------------------------------
    # FORMACIÓN
    # --------------------------------------------------------

    titulo = normalizar(
        perfil.get("profesion", "")
    )

    texto_oferta = normalizar(
        obtener_texto_oferta(oferta)
    )

    if "automatizacion" in titulo:

        if any(
            palabra in texto_oferta
            for palabra in [
                "automatizacion",
                "automatización",
                "control",
                "plc",
                "instrumentacion",
                "instrumentación",
                "mantenimiento"
            ]
        ):

            puntos += 20

            fortalezas.append(
                "La formación técnica está directamente relacionada con el cargo."
            )

        else:

            puntos += 10

            fortalezas.append(
                "Cuenta con formación técnica relacionada."
            )

    # --------------------------------------------------------
    # COMPETENCIAS
    # --------------------------------------------------------

    competencias_perfil = [
        normalizar(x)
        for x in obtener_conocimientos_perfil(perfil)
    ]

    for competencia in competencias:

        competencia_normalizada = normalizar(
            competencia
        )

        coincide = False

        for conocimiento in competencias_perfil:

            if (
                competencia_normalizada in conocimiento
                or conocimiento in competencia_normalizada
            ):
                coincide = True
                break

        if coincide:

            puntos += 4

            fortalezas.append(
                f"Cuenta con conocimientos relacionados con {competencia}."
            )

        else:

            brechas.append(
                f"{competencia}"
            )

    # --------------------------------------------------------
    # EXPERIENCIA
    # --------------------------------------------------------

    meses = perfil.get(
        "experiencia",
        {}
    ).get(
        "meses_aproximados",
        0
    )

    if anos_requeridos is None:

        if experiencia_requerida:

            if "sin experiencia" in experiencia_requerida:

                puntos += 15

                fortalezas.append(
                    "La oferta acepta perfiles sin experiencia."
                )

            else:

                puntos += 8

        else:

            puntos += 8

    else:

        experiencia_usuario = meses / 12

        if experiencia_usuario >= anos_requeridos:

            puntos += 20

            fortalezas.append(
                "La experiencia indicada alcanza el mínimo solicitado."
            )

        elif anos_requeridos <= 1:

            puntos += 14

            brechas.append(
                f"La oferta solicita aproximadamente {anos_requeridos} año de experiencia."
            )

            aprendizaje_rapido.append(
                "La diferencia de experiencia puede compensarse parcialmente con formación técnica."
            )

        elif anos_requeridos == 2:

            puntos += 8

            brechas.append(
                "La oferta solicita 2 años de experiencia y el perfil todavía está iniciando su experiencia profesional."
            )

        else:

            puntos += 2

            brechas.append(
                f"La oferta solicita {anos_requeridos} años de experiencia."
            )

    # --------------------------------------------------------
    # UBICACIÓN
    # --------------------------------------------------------

    if ubicacion.get("zona_prioritaria"):

        puntos += 10

        fortalezas.append(
            f"La ubicación ({ubicacion.get('ubicacion_oferta')}) está dentro de las zonas prioritarias."
        )

    else:

        puntos += 3

        if ubicacion.get("ubicacion_oferta"):

            brechas.append(
                f"La ubicación ({ubicacion.get('ubicacion_oferta')}) no está entre las zonas prioritarias."
            )

    # --------------------------------------------------------
    # CARGO
    # --------------------------------------------------------

    if cargos:

        puntos += 10

        fortalezas.append(
            "El tipo de cargo coincide con uno de los cargos prioritarios."
        )

    # --------------------------------------------------------
    # DETECTAR CONOCIMIENTOS QUE REQUIEREN PRÁCTICA
    # --------------------------------------------------------

    competencias_practicas = [
        "diagnóstico de fallas",
        "instrumentación",
        "PLC Siemens",
        "PLC",
        "SCADA",
        "mantenimiento correctivo",
        "puesta en marcha",
        "programación"
    ]

    for competencia in competencias:

        if competencia in competencias_practicas:

            if competencia in [
                "PLC Siemens",
                "SCADA",
                "instrumentación"
            ]:

                brechas_practicas.append(
                    f"{competencia}: requiere experiencia práctica para alcanzar autonomía."
                )

            elif competencia == "diagnóstico de fallas":

                brechas_practicas.append(
                    "Diagnóstico de fallas: es una competencia que normalmente requiere experiencia práctica en terreno."
                )

            elif competencia == "mantenimiento correctivo":

                brechas_practicas.append(
                    "Mantenimiento correctivo: conviene desarrollar experiencia práctica con equipos reales."
                )

    # --------------------------------------------------------
    # APRENDIZAJE AUTODIDACTA
    # --------------------------------------------------------

    competencias_aprendibles = [
        "PLC",
        "PLC Siemens",
        "variadores de frecuencia",
        "HMI",
        "lectura de planos",
        "automatización",
        "mantenimiento preventivo",
        "seguridad eléctrica"
    ]

    for competencia in competencias:

        if competencia in competencias_aprendibles:

            aprendizaje_rapido.append(
                f"{competencia}: puede reforzarse mediante estudio, simulación y práctica guiada."
            )

    # --------------------------------------------------------
    # LIMITAR PUNTAJE
    # --------------------------------------------------------

    puntos = max(
        0,
        min(
            puntos,
            puntos_maximos
        )
    )

    # --------------------------------------------------------
    # PROBABILIDAD
    # --------------------------------------------------------

    if puntos >= 75:

        nivel = "ALTA"

    elif puntos >= 50:

        nivel = "MEDIA"

    elif puntos >= 30:

        nivel = "MEDIA-BAJA"

    else:

        nivel = "BAJA"

    return {
        "puntaje": puntos,
        "probabilidad_ajuste": nivel,
        "fortalezas": list(dict.fromkeys(fortalezas)),
        "brechas": list(dict.fromkeys(brechas)),
        "aprendizaje_rapido": list(dict.fromkeys(aprendizaje_rapido)),
        "brechas_practicas": list(dict.fromkeys(brechas_practicas))
    }


# ============================================================
# ANALIZAR UNA OFERTA
# ============================================================

def analizar_oferta(oferta, perfil):

    texto = obtener_texto_oferta(oferta)

    competencias = detectar_competencias(texto)

    experiencia = detectar_experiencia(texto)

    anos_requeridos = extraer_anos_experiencia(texto)

    ubicacion = detectar_ubicacion(
        oferta,
        perfil
    )

    cargos = detectar_cargo(
        oferta,
        perfil
    )

    compatibilidad = analizar_compatibilidad(
        competencias,
        experiencia,
        anos_requeridos,
        ubicacion,
        cargos,
        oferta,
        perfil
    )

    return {

        "competencias_detectadas": competencias,

        "experiencia_detectada": experiencia,

        "anos_experiencia_solicitados": anos_requeridos,

        "ubicacion": ubicacion,

        "cargos_coincidentes": cargos,

        "compatibilidad": compatibilidad
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

    if not perfil:

        print("No se pudo cargar el perfil.")
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
    # INFORME EN ACTIONS
    # --------------------------------------------------------

    print("==========================================")
    print("       INVESTIGADOR LABORAL")
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

    print("\nANÁLISIS DE COMPATIBILIDAD:")

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
            f"Empresa: {oferta.get('empresa', 'Sin empresa')}"
        )

        print(
            f"Compatibilidad: "
            f"{compatibilidad.get('probabilidad_ajuste', 'N/D')}"
        )

        print(
            f"Puntaje: "
            f"{compatibilidad.get('puntaje', 0)}/100"
        )

        print("Fortalezas:")

        for item in compatibilidad.get(
            "fortalezas",
            []
        ):

            print(
                f"  + {item}"
            )

        print("Brechas:")

        for item in compatibilidad.get(
            "brechas",
            []
        ):

            print(
                f"  - {item}"
            )

        print("Aspectos que puedes reforzar:")

        for item in compatibilidad.get(
            "aprendizaje_rapido",
            []
        ):

            print(
                f"  * {item}"
            )

        print("Brechas que requieren práctica:")

        for item in compatibilidad.get(
            "brechas_practicas",
            []
        ):

            print(
                f"  ! {item}"
            )

    print("\n==========================================")
    print("Análisis terminado correctamente.")
    print("==========================================")


# ============================================================
# EJECUTAR
# ============================================================

if __name__ == "__main__":

    analizar_historial()
