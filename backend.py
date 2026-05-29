# Importa Gemini para generar respuestas
from google import genai

# Importa tipos de Gemini para enviar imágenes al modelo
from google.genai import types

# Importa SentenceTransformer para crear embeddings locales
from sentence_transformers import SentenceTransformer

# Importa load_dotenv para cargar variables del archivo .env
from dotenv import load_dotenv

# Importa ChromaDB para consultar la base vectorial del PDF
import chromadb

# Importa expresiones regulares para detectar páginas
import re

# Importa os para leer variables de entorno y verificar archivos
import os
# Importa Streamlit
import streamlit as st

# Fuerza a cargar el .env ubicado en la misma carpeta del backend.py
load_dotenv(dotenv_path=".env", override=True)

api_key = st.secrets.get("GEMINI_API_KEY", os.getenv("GEMINI_API_KEY"))
gemini_model = st.secrets.get("GEMINI_MODEL", os.getenv("GEMINI_MODEL"))

# Muestra la ruta actual desde donde se ejecuta el proyecto
print(f"CARPETA ACTUAL: {os.getcwd()}")

# Muestra si el archivo .env existe en esa carpeta
print(f"EXISTE .env: {os.path.exists('.env')}")

# Obtiene la API Key de Gemini desde el archivo .env
gemini_api_key = os.getenv("GEMINI_API_KEY")

# Obtiene el modelo de Gemini desde el archivo .env
gemini_model = os.getenv("GEMINI_MODEL", "gemini-2.0-flash-lite")

# Muestra en consola qué modelo está usando realmente
print(f"MODELO GEMINI CARGADO: {gemini_model}")

# Crea el cliente principal de Gemini
client = genai.Client(api_key=gemini_api_key)

# Carga el mismo modelo local usado en vectorizar_pdf.py
modelo_embeddings = SentenceTransformer("all-MiniLM-L6-v2")

# Carga la base vectorial local creada con vectorizar_pdf.py
chroma_client = chromadb.PersistentClient(path="base_vectorial_calculo")

# Carga la colección donde están los fragmentos del PDF
coleccion = chroma_client.get_or_create_collection(name="calculo_pdf")


# Función para convertir texto en embedding local
def crear_embedding(texto):

    # Convierte el texto en vector numérico
    embedding = modelo_embeddings.encode(texto)

    # Devuelve el vector como lista
    return embedding.tolist()


# Función para detectar página numérica o especial
def detectar_pagina(pregunta):

    # Convierte la pregunta a mayúsculas para detectar AP, FM, RES, etc.
    texto = pregunta.upper()

    # Busca páginas especiales como AP-2, FM-4, RES-3, IND-1, C-1
    especial = re.search(
        r"\b(AP-\d+|FM-\d+|RES-\d+|IND-\d+|ÍND-\d+|C-\d+)\b",
        texto
    )

    # Si encuentra una página especial, la devuelve
    if especial:
        return especial.group(1).replace("ÍND", "IND")

    # Busca página numérica como "página 102" o "pagina 102"
    normal = re.search(r"p[aá]gina(?:\s+de)?\s+(\d+)", pregunta.lower())

    # Si encuentra página numérica, la devuelve como texto
    if normal:
        return normal.group(1)

    # Si no encuentra página, devuelve None
    return None
def es_referencia_libro(texto):

    texto = texto.lower()

    patrones = [
        r"p[aá]gina\s+\d+",
        r"problema\s+\d+",
        r"ejercicio\s+\d+",
        r"n[uú]mero\s+\d+",
        r"\b\d+\b"
    ]

    for patron in patrones:
        if re.search(patron, texto):
            return True

    return False

# Función para buscar información dentro del PDF vectorizado
def buscar_en_pdf(pregunta):

    # Detecta si el usuario pidió una página específica
    pagina_etiqueta = detectar_pagina(pregunta)

    # Si pidió una página específica
    if pagina_etiqueta:

        # Busca por etiqueta exacta de página
        resultados = coleccion.get(
            where={"pagina_etiqueta": pagina_etiqueta},
            include=["documents", "metadatas"]
        )

        # Obtiene fragmentos encontrados
        fragmentos = resultados["documents"]

        # Si no encontró por etiqueta, intenta buscar como página numérica
        if not fragmentos and pagina_etiqueta.isdigit():

            # Convierte la etiqueta a número
            pagina_libro = int(pagina_etiqueta)

            # Busca por página numérica
            resultados = coleccion.get(
                where={"pagina_libro": pagina_libro},
                include=["documents", "metadatas"]
            )

            # Obtiene fragmentos encontrados
            fragmentos = resultados["documents"]

        # Si no encontró nada
        if not fragmentos:
            return f"No encontré contenido guardado para la página {pagina_etiqueta}."

        # Une todos los fragmentos de esa página
        return "\n\n".join(fragmentos)

    # Si no pidió página específica, busca semánticamente
    embedding_pregunta = crear_embedding(pregunta)

    # Consulta la base vectorial
    resultados = coleccion.query(
        query_embeddings=[embedding_pregunta],
        n_results=6
    )

    # Obtiene los fragmentos
    fragmentos = resultados["documents"][0]

    # Une los fragmentos
    return "\n\n".join(fragmentos)


# Función para manejar errores de Gemini
def manejar_error_gemini(error):

    # Convierte el error a texto
    error_texto = str(error)

    # Si se agotó la cuota gratuita
    if "RESOURCE_EXHAUSTED" in error_texto or "429" in error_texto:
        return (
            "Se agotó temporalmente la cuota gratuita de Gemini.\n\n"
            "Intenta nuevamente más tarde o cambia el modelo en el archivo `.env`."
        )

    # Si Gemini está saturado
    if "503" in error_texto or "UNAVAILABLE" in error_texto:
        return (
            "Gemini está saturado temporalmente.\n\n"
            "Intenta nuevamente en unos segundos."
        )

    # Otro error
    return f"Ocurrió un error al generar la respuesta: {error}"

# Detecta si la pregunta pertenece a cálculo matemático
def es_tema_calculo(texto):

    # Convierte el texto a minúsculas
    texto = texto.lower()

    # Palabras relacionadas con cálculo
    palabras_calculo = [
        "calculo",
        "cálculo",
        "derivada",
        "integral",
        "limite",
        "límite",
        "funcion",
        "función",
        "ecuacion",
        "ecuación",
        "grafica",
        "gráfica",
        "resolver",
        "matematica",
        "matemática",
        "fraccion",
        "fracción",
        "raiz",
        "raíz",
        "logaritmo",
        "trigonometria",
        "sabes",
        "haces",
        "hacer",
        "ayudas",
        "ayudar",
        "puedes",
        "funciones",
        "explicas",
        "resolver",
    ]

    # Verifica si alguna palabra está presente
    return any(palabra in texto for palabra in palabras_calculo)

# Detecta operaciones matemáticas básicas
def contiene_operacion_basica(texto):

    # Operadores matemáticos
    operadores = ["+", "-", "*", "/", "^", "(", ")"]

    # Verifica si hay números
    tiene_numero = any(caracter.isdigit() for caracter in texto)

    # Verifica si hay operadores
    tiene_operador = any(operador in texto for operador in operadores)

    # Devuelve True si parece operación matemática
    return tiene_numero and tiene_operador

# Función principal que responde usando Gemini y el PDF
def responder_con_gemini(pregunta):
      # Si no es cálculo ni operación matemática, se rechaza
    if (
        not es_tema_calculo(pregunta)
        and not contiene_operacion_basica(pregunta)
        and not es_referencia_libro(pregunta)
    ):
        return "Lo siento, solo puedo ayudarte con temas de Cálculo Matemático."

    # Detecta página numérica o especial
    pagina_etiqueta = detectar_pagina(pregunta)

    # Busca contexto textual en ChromaDB
    contexto_pdf = buscar_en_pdf(pregunta)

    # Si el usuario pidió una página específica
    if pagina_etiqueta:

        # Ruta de imagen según etiqueta
        ruta_imagen = f"paginas_calculo/pagina_{pagina_etiqueta}.png"

        # Verifica si existe la imagen
        if not os.path.exists(ruta_imagen):
            return f"No encontré la imagen de la página {pagina_etiqueta}."

        # Abre la imagen de la página
        with open(ruta_imagen, "rb") as archivo:
            imagen_bytes = archivo.read()

        # Prompt para Gemini con imagen
        prompt = f"""
Eres un tutor universitario especializado en Cálculo 1.
ÁREAS QUE DOMINAS:
- Límites y continuidad (definición épsilon-delta, límites laterales, indeterminaciones)
- Derivadas (definición, reglas de derivación, derivadas implícitas, aplicaciones)
- Integrales (indefinidas, definidas, técnicas: sustitución, partes, fracciones parciales)
- Series y sucesiones (convergencia, series de Taylor y Maclaurin, radio de convergencia)
- Cálculo multivariable (derivadas parciales, gradiente, divergencia, integrales múltiples)
- Ecuaciones diferenciales ordinarias (separables, lineales, orden superior)
- Vectores y geometría diferencial

REGLA PRINCIPAL:
Siempre debes responder la pregunta del usuario.
El PDF es material de apoyo, no tu única fuente obligatoria.
REGLAS ABSOLUTAS — NO NEGOCIABLES
1. Cuando resuelvas un problema, muestra TODOS los pasos detalladamente.
2. Responde siempre en español.
3. Sé amable pero firme con el filtro de temas.
4. Si hay material de referencia disponible, úsalo para fundamentar tus respuestas en este caso es el pdf utilizado.
5.Si el PDF no contiene suficiente información, usa conocimiento general de Cálculo 1 para completar la explicación correctamente.
6.Procura siempre dar las formulas necesarias usa el pdf como referencia para buscar formulas para mostrarlas al usuario.

PROHIBIDO:
- No digas que "el PDF no contiene la definición".
- No digas que "tu única fuente es el PDF".
- No rechaces preguntas básicas de Cálculo 1.
- No respondas únicamente analizando el contexto recuperado.

OBJETIVO:
Explicar teoría, resolver ejercicios y ayudar al estudiante universitario.

Reglas:
1. Usa el PDF como apoyo cuando sea útil.
2. Si la pregunta es conceptual, responde con:
   - definición,
   - explicación sencilla,
   - fórmula si existe,
   - ejemplo corto.
3. Si la pregunta es un ejercicio:
   - resuelve paso a paso,
   - muestra procedimiento,
   - muestra respuesta final.
4. Usa lenguaje claro y académico.
5. Usa LaTeX compatible con Streamlit.
6. Usa $ ... $ para fórmulas pequeñas.
7. Usa $$ ... $$ para fórmulas grandes.
8. Cuando analices ejercicios desde imagen, revisa cuidadosamente radicales, raíces cuadradas, raíces cúbicas, exponentes fraccionarios y denominadores. No conviertas una raíz en una potencia entera. Si aparece √ o ∛, debes conservarlo en LaTeX.
9. Antes de resolver, reescribe exactamente el ejercicio original en LaTeX respetando raíces, exponentes, fracciones y variables.
10. En preguntas conceptuales de Cálculo 1, siempre incluye al menos una fórmula matemática importante en LaTeX.

Formato visual obligatorio:
- Usa títulos Markdown como:
## Definición
## Explicación
## Ejemplo
## Procedimiento
## Respuesta final

- Separa cada paso con líneas en blanco.
- No escribas párrafos gigantes.
- Las fórmulas importantes deben ir en bloques $$ ... $$.

Reglas para gráficas:
- Solo genera gráfica si el usuario pide explícitamente:
graficar, gráfica, dibujar, representar o visualizar.

- Si el usuario pide una gráfica y existe una función válida, escribe al final:
GRAFICAR_PYTHON: expresión

Ejemplo:
GRAFICAR_PYTHON: x**2 - 4

- Usa ** para potencias.
- No uses LaTeX dentro de GRAFICAR_PYTHON.
- No uses y= ni f(x)=.

- Si el usuario NO pide gráfica, NO escribas nada relacionado con gráficas.

Contexto textual extraído:
{contexto_pdf}

Pregunta del usuario:
{pregunta}

Respuesta:
"""

        # Intenta enviar texto + imagen a Gemini
        try:

            # Genera respuesta usando Gemini
            respuesta = client.models.generate_content(
                model=gemini_model,
                contents=[
                    prompt,
                    types.Part.from_bytes(
                        data=imagen_bytes,
                        mime_type="image/png"
                    )
                ]
            )

            # Devuelve respuesta
            return respuesta.text

        # Captura errores de Gemini
        except Exception as error:

            # Devuelve mensaje amigable
            return manejar_error_gemini(error)

    # Prompt normal cuando no se pidió página específica
    prompt = f"""
Eres un tutor universitario especializado en Cálculo 1.
ÁREAS QUE DOMINAS:
- Límites y continuidad (definición épsilon-delta, límites laterales, indeterminaciones)
- Derivadas (definición, reglas de derivación, derivadas implícitas, aplicaciones)
- Integrales (indefinidas, definidas, técnicas: sustitución, partes, fracciones parciales)
- Series y sucesiones (convergencia, series de Taylor y Maclaurin, radio de convergencia)
- Cálculo multivariable (derivadas parciales, gradiente, divergencia, integrales múltiples)
- Ecuaciones diferenciales ordinarias (separables, lineales, orden superior)
- Vectores y geometría diferencial

REGLA PRINCIPAL:
Siempre debes responder la pregunta del usuario.
El PDF es material de apoyo, no tu única fuente obligatoria.
REGLAS ABSOLUTAS — NO NEGOCIABLES:
1. Cuando resuelvas un problema, muestra TODOS los pasos detalladamente.
2. Responde siempre en español.
3. Sé amable pero firme con el filtro de temas.
4. Si hay material de referencia disponible, úsalo para fundamentar tus respuestas en este caso es el pdf utilizado.
5. Si el PDF no contiene suficiente información, usa conocimiento general de Cálculo 1 para completar la explicación correctamente.
6. Procura siempre dar las formulas necesarias usa el pdf como referencia para buscar formulas para mostrarlas al usuario.

Formato visual obligatorio:
- Usa títulos con Markdown, por ejemplo: ## Ejercicio, ## Procedimiento, ## Respuesta final.
- Separa cada paso con una línea en blanco.
- Usa listas numeradas para el procedimiento.
- No escribas párrafos largos.
- No repitas la misma fórmula muchas veces.
- Las fórmulas importantes deben ir solas en bloques $$ ... $$.
- La respuesta final debe ir al final y en negrita.

Reglas para gráficas:
- Si el usuario pide graficar y la función es graficable, escribe al final una línea exacta así:
GRAFICAR_PYTHON: expresión
- La expresión debe ser una función explícita de x.
- No uses LaTeX en GRAFICAR_PYTHON.
- No uses y= ni f(x)=.
- Usa ** para potencias.
- Usa * para multiplicaciones.
- Puedes usar sin(x), cos(x), tan(x), exp(x), log(x), sqrt(x), abs(x).
- Si el usuario NO pide una gráfica, no escribas nada relacionado con gráficas.
- Si el usuario pide gráfica pero no hay función clara, explica brevemente que necesita una función explícita de x.

Contexto extraído del PDF:
{contexto_pdf}

Pregunta del usuario:
{pregunta}

Respuesta:
"""

    # Intenta generar respuesta usando Gemini
    try:

        # Envía prompt a Gemini
        respuesta = client.models.generate_content(
            model=gemini_model,
            contents=prompt
        )

        # Devuelve texto generado
        return respuesta.text

    # Captura errores de Gemini
    except Exception as error:

        # Devuelve mensaje amigable
        return manejar_error_gemini(error)
