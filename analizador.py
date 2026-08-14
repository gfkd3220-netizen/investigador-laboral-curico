import json
import re
from collections import Counter


# ============================================================
# CONFIGURACIÓN
# ============================================================

ARCHIVO_HISTORIAL = "historial.json"


# ============================================================
# COMPETENCIAS QUE VAMOS A DETECTAR
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
# EXPERIENCIA SOLICITADA
# ============================================================

PATRONES_EXPERIENCIA = {
    "sin experiencia": [
        "sin experiencia",
        "no requiere experiencia",
        "recién egresado",
        "recien egresado"
    ],

    "experiencia menor a 1 año": [
        "6 meses de experiencia",
        "6 meses experiencia",
        "menos de 1 año",
        "menos de un año"
    ],

    "1 año": [
        "1 año de experiencia",
        "1 año experiencia",
        "un año de experiencia"
    ],

    "2 años": [
        "2 años de experiencia",
        "2 años experiencia",
        "dos años de experiencia"
    ],

    "3 años o más": [
        "3 años de experiencia",
        "4 años de experiencia",
        "5 años de experiencia",
        "3 años experiencia",
        "4 años experiencia",
        "5 años experiencia",
        "más de 3 años",
        "mas de 3 años"
    ]
}


# ============================================================
# NORMALIZAR TEXTO
# ============================================================

def normalizar(texto):
    texto = texto.lower()

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
# ANALIZAR UNA OFERTA
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

    experiencia = detectar_experiencia(texto)

    return {
        "competencias_detectadas": competencias,
        "experiencia_detectada": experiencia
    }


# ============================================================
# ANALIZAR HISTORIAL COMPLETO
# ============================================================

def analizar_historial():

    try:

        with open(ARCHIVO_HISTORIAL, "r", encoding="utf-8") as archivo:
            historial = json.load(archivo)

    except FileNotFoundError:

        print("No se encontró historial.json")
        return

    ofertas = historial.get("ofertas", [])

    contador_competencias = Counter()
    contador_experiencia = Counter()

    ofertas_analizadas = 0

    for oferta in ofertas:

        resultado = analizar_oferta(oferta)

        oferta["analisis"] = resultado

        for competencia in resultado["competencias_detectadas"]:
            contador_competencias[competencia] += 1

        for experiencia in resultado["experiencia_detectada"]:
            contador_experiencia[experiencia] += 1

        ofertas_analizadas += 1

    historial["tendencias"]["competencias"] = dict(
        contador_competencias.most_common()
    )

    historial["tendencias"]["experiencia_requerida"] = dict(
        contador_experiencia.most_common()
    )

    historial["ultima_actualizacion"] = "actualizado automáticamente"

    with open(ARCHIVO_HISTORIAL, "w", encoding="utf-8") as archivo:

        json.dump(
            historial,
            archivo,
            ensure_ascii=False,
            indent=2
        )

    print("==========================================")
    print("ANÁLISIS LABORAL")
    print("==========================================")

    print(f"Ofertas analizadas: {ofertas_analizadas}")

    print("\nCOMPETENCIAS MÁS REPETIDAS:")

    for competencia, cantidad in contador_competencias.most_common():

        print(
            f"- {competencia}: {cantidad} ofertas"
        )

    print("\nEXPERIENCIA SOLICITADA:")

    for nivel, cantidad in contador_experiencia.most_common():

        print(
            f"- {nivel}: {cantidad} ofertas"
        )

    print("==========================================")


# ============================================================
# EJECUTAR
# ============================================================

if __name__ == "__main__":
    analizar_historial()
