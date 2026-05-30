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

# Importa Streamlit para leer secrets en Streamlit Cloud
import streamlit as st

# Carga variables del archivo .env local
load_dotenv(dotenv_path=".env", override=True)

# Lee API Key y modelo desde Streamlit Secrets o desde .env
gemini_api_key = st.secrets.get("GEMINI_API_KEY", os.getenv("GEMINI_API_KEY"))
gemini_model = st.secrets.get("GEMINI_MODEL", os.getenv("GEMINI_MODEL", "gemini-2.0-flash-lite"))

# Crea el cliente principal de Gemini
client = genai.Client(api_key=gemini_api_key)

# Carga el modelo local de embeddings
modelo_embeddings = SentenceTransformer("all-MiniLM-L6-v2")

# Carga la base vectorial local
chroma_client = chromadb.PersistentClient(path="base_vectorial_calculo")

# Carga la colección donde están los fragmentos del PDF
coleccion = chroma_client.get_or_create_collection(name="calculo_pdf")


# Convierte texto en embedding local
def crear_embedding(texto):
    embedding = modelo_embeddings.encode(texto)
    return embedding.tolist()


# Detecta si el usuario pidió una página específica del libro
def detectar_pagina(pregunta):
    texto = pregunta.upper()

    especial = re.search(
        r"\b(AP-\d+|FM-\d+|RES-\d+|IND-\d+|ÍND-\d+|C-\d+)\b",
        texto
    )

    if especial:
        return especial.group(1).replace("ÍND", "IND")

    normal = re.search(r"p[aá]gina(?:\s+de)?\s+(\d+)", pregunta.lower())

    if normal:
        return normal.group(1)

    return None


# Detecta si el usuario hace referencia a ejercicio, problema o página del libro
def es_referencia_libro(texto):
    texto = texto.lower()

    patrones = [
        r"p[aá]gina\s+\d+",
        r"problema\s+\d+",
        r"ejercicio\s+\d+",
        r"n[uú]mero\s+\d+"
    ]

    for patron in patrones:
        if re.search(patron, texto):
            return True

    return False


# Busca información en el PDF vectorizado
def buscar_en_pdf(pregunta):
    pagina_etiqueta = detectar_pagina(pregunta)

    if pagina_etiqueta:
        resultados = coleccion.get(
            where={"pagina_etiqueta": pagina_etiqueta},
            include=["documents", "metadatas"]
        )

        fragmentos = resultados["documents"]

        if not fragmentos and pagina_etiqueta.isdigit():
            pagina_libro = int(pagina_etiqueta)

            resultados = coleccion.get(
                where={"pagina_libro": pagina_libro},
                include=["documents", "metadatas"]
            )

            fragmentos = resultados["documents"]

        if not fragmentos:
            return f"No encontré contenido guardado para la página {pagina_etiqueta}."

        return "\n\n".join(fragmentos)

    embedding_pregunta = crear_embedding(pregunta)

    resultados = coleccion.query(
        query_embeddings=[embedding_pregunta],
        n_results=6
    )

    fragmentos = resultados["documents"][0]

    return "\n\n".join(fragmentos)


# Maneja errores de Gemini
def manejar_error_gemini(error):
    error_texto = str(error)

    if "RESOURCE_EXHAUSTED" in error_texto or "429" in error_texto:
        return (
            "Se agotó temporalmente la cuota gratuita de Gemini.\n\n"
            "Intenta nuevamente más tarde o cambia el modelo en Streamlit Secrets."
        )

    if "503" in error_texto or "UNAVAILABLE" in error_texto:
        return (
            "Nos encontramos saturados temporalmente.\n\n"
            "Intenta nuevamente en unos segundos."
        )

    return f"Ocurrió un error al generar la respuesta: {error}"


# Detecta si la pregunta pertenece a Cálculo o matemáticas relacionadas
def es_tema_calculo(texto):
    texto = texto.lower()

    palabras_calculo = [
        "calculo", "cálculo",
        "derivada", "derivar",
        "integral", "integrar",
        "limite", "límite",
        "funcion", "función",
        "ecuacion", "ecuación",
        "grafica", "gráfica", "graficar",
        "resolver",
        "matematica", "matemática",
        "fraccion", "fracción",
        "raiz", "raíz",
        "logaritmo",
        "trigonometria", "trigonometría",
        "seno", "coseno", "tangente",
        "continuidad", "sucesion", "sucesión",
        "serie", "pendiente",
        "maximo", "máximo", "minimo", "mínimo",
        "calculo", "cálculo", "calculo 1", "cálculo 1",
        "derivada", "derivar", "deriva", "derivame", "derívame",
        "diferenciacion", "diferenciación",
        "regla de la potencia", "regla del producto", "regla del cociente",
        "regla de la cadena", "derivada implicita", "derivada implícita",
        "derivada parcial",
        "integral", "integrar", "integra", "integrame", "intégrame",
        "integral definida", "integral indefinida",
        "antiderivada", "primitiva",
        "area bajo la curva", "área bajo la curva",
        "sumatoria", "suma de riemann", "riemann",
        "limite", "límite", "limites", "límites",
        "tiende a", "aproximacion", "aproximación",
        "continuidad", "discontinuidad",
        "asintota", "asíntota",
        "funcion", "función", "funciones",
        "dominio", "rango", "imagen",
        "evaluar funcion", "evaluar función",
        "composicion de funciones", "composición de funciones",
        "funcion inversa", "función inversa",
        "grafica", "gráfica", "graficar",
        "curva", "pendiente", "recta tangente",
        "recta normal", "interseccion", "intersección",
        "punto critico", "punto crítico",
        "maximo", "máximo", "minimo", "mínimo",
        "optimizacion", "optimización",
        "crecimiento", "decrecimiento",
        "concavidad", "inflexion", "inflexión",
        "polinomio", "potencia", "exponente",
        "cuadrado", "cubo", "raiz", "raíz",
        "radical", "fraccion", "fracción",
        "racionalizar",
        "seno", "coseno", "tangente",
        "secante", "cosecante", "cotangente",
        "trigonometria", "trigonometría",
        "identidad trigonometrica", "identidad trigonométrica",
        "logaritmo", "logaritmica", "logarítmica",
        "exponencial", "euler", "numero e", "número e",
        "ln", "log",
        "ecuacion", "ecuación",
        "resolver", "simplificar", "factorizar",
        "expandir", "despejar", "sustituir",
        "evaluar", "calcular",
        "x", "y", "f(x)", "dx", "dy",
        "d/dx", "dy/dx", "lim", "sin", "cos", "tan",
        "sqrt", "pi", "π"

        # Consultas sobre el asistente
        "sabes", "haces", "hacer",
        "ayudas", "ayudar",
        "puedes", "funciones",
        "explicas", "explicar"
    ]

    return any(palabra in texto for palabra in palabras_calculo)


# Detecta operaciones matemáticas básicas
def contiene_operacion_basica(texto):
    operadores = ["+", "-", "*", "/", "^", "(", ")"]

    tiene_numero = any(caracter.isdigit() for caracter in texto)
    tiene_operador = any(operador in texto for operador in operadores)

    return tiene_numero and tiene_operador


# Evalúa operaciones básicas de forma controlada
def resolver_operacion_basica(pregunta):
    expresion = pregunta.strip().replace("^", "**")

    if not re.fullmatch(r"[0-9\s\+\-\*\/\.\(\)\*]+", expresion):
        raise ValueError("Expresión no permitida.")

    resultado = eval(expresion, {"__builtins__": None}, {})

    return resultado


# Función principal que responde usando Gemini y el PDF
def responder_con_gemini(pregunta):

    # Si no es cálculo, operación matemática o referencia del libro, se rechaza
    if (
        not es_tema_calculo(pregunta)
        and not contiene_operacion_basica(pregunta)
        and not es_referencia_libro(pregunta)
    ):
        return "Lo siento, solo puedo ayudarte con temas de Cálculo Matemático."

    # Resuelve operaciones matemáticas básicas directamente
    if contiene_operacion_basica(pregunta):
        try:
            resultado = resolver_operacion_basica(pregunta)

            return f"""## Operación matemática

$$
{pregunta} = {resultado}
$$

## Respuesta final

**El resultado es {resultado}.**
"""

        except Exception:
            pass

    # Detecta página numérica o especial
    pagina_etiqueta = detectar_pagina(pregunta)

    # Busca contexto textual en ChromaDB
    contexto_pdf = buscar_en_pdf(pregunta)

    # Si el usuario pidió una página específica
    if pagina_etiqueta:
        ruta_imagen = f"paginas_calculo/pagina_{pagina_etiqueta}.png"

        if not os.path.exists(ruta_imagen):
            return f"No encontré la imagen de la página {pagina_etiqueta}."

        with open(ruta_imagen, "rb") as archivo:
            imagen_bytes = archivo.read()

        prompt = f"""
Eres un tutor universitario especializado en Cálculo 1.

ÁREAS QUE DOMINAS:
- Límites y continuidad.
- Derivadas.
- Integrales.
- Series y sucesiones.
- Aplicaciones de la derivada.
- Gráficas de funciones.
- Técnicas básicas de integración.

REGLA PRINCIPAL:
Siempre debes responder la pregunta del usuario.
El PDF es material de apoyo, no tu única fuente obligatoria.
Trabaja ÚNICAMENTE con la expresión que el usuario escriba.
NO inventes ejemplos.
NO uses otra fórmula diferente.
NO agregues teoría innecesaria.

REGLAS:
1. Responde siempre en español.
2. Cuando resuelvas un problema, muestra todos los pasos.
3. Usa el PDF como apoyo cuando sea útil.
4. Si el PDF no contiene suficiente información, usa conocimiento general de Cálculo 1.
5. No digas que el PDF no contiene la definición.
6. No digas que tu única fuente es el PDF.
7. No rechaces preguntas básicas de Cálculo 1.
8. Usa LaTeX compatible con Streamlit.
9. Usa $ ... $ para fórmulas pequeñas.
10. Usa $$ ... $$ para fórmulas grandes.
11. Cuando analices ejercicios desde imagen, respeta radicales, raíces cuadradas, raíces cúbicas, exponentes fraccionarios y denominadores.
12. Antes de resolver, reescribe exactamente el ejercicio original en LaTeX.

FORMATO:
- Usa títulos Markdown:
## Definición
## Explicación
## Ejemplo
## Procedimiento
## Respuesta final

REGLAS PARA GRÁFICAS:
- Solo genera gráfica si el usuario pide explícitamente graficar, gráfica, dibujar, representar o visualizar.
- Si el usuario pide gráfica y la función es válida, escribe al final:
GRAFICAR_PYTHON: expresión
- No uses LaTeX en GRAFICAR_PYTHON.
- No uses y= ni f(x)=.
- Usa ** para potencias.

Contexto textual extraído:
{contexto_pdf}

Pregunta del usuario:
{pregunta}

Respuesta:
"""

        try:
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

            return respuesta.text

        except Exception as error:
            return manejar_error_gemini(error)

    # Prompt normal
    prompt = f"""
Eres un tutor universitario especializado en Cálculo 1.

ÁREAS QUE DOMINAS:
- Límites y continuidad.
- Derivadas.
- Integrales.
- Series y sucesiones.
- Aplicaciones de la derivada.
- Gráficas de funciones.
- Técnicas básicas de integración.

REGLA PRINCIPAL:
Siempre debes responder la pregunta del usuario.
El PDF es material de apoyo, no tu única fuente obligatoria.
Trabaja ÚNICAMENTE con la expresión que el usuario escriba.
NO inventes ejemplos.
NO uses otra fórmula diferente.
NO agregues teoría innecesaria.

REGLAS:
1. Responde siempre en español.
2. Cuando resuelvas un problema, muestra todos los pasos.
3. Usa el PDF como apoyo cuando sea útil.
4. Si el PDF no contiene suficiente información, usa conocimiento general de Cálculo 1.
5. No digas que el PDF no contiene la definición.
6. No digas que tu única fuente es el PDF.
7. No rechaces preguntas básicas de Cálculo 1.
8. Usa LaTeX compatible con Streamlit.
9. Usa $ ... $ para fórmulas pequeñas.
10. Usa $$ ... $$ para fórmulas grandes.
11. Si la pregunta es conceptual, incluye definición, fórmula, explicación y ejemplo.
12. En preguntas conceptuales de Cálculo 1, incluye al menos una fórmula matemática importante.

FORMATO:
- Usa títulos Markdown:
## Definición
## Explicación
## Ejemplo
## Procedimiento
## Respuesta final

REGLAS PARA GRÁFICAS:
- Solo genera gráfica si el usuario pide explícitamente graficar, gráfica, dibujar, representar o visualizar.
- Si el usuario pide gráfica y la función es válida, escribe al final:
GRAFICAR_PYTHON: expresión
- No uses LaTeX en GRAFICAR_PYTHON.
- No uses y= ni f(x)=.
- Usa ** para potencias.
- Usa * para multiplicaciones.

Contexto extraído del PDF:
{contexto_pdf}

Pregunta del usuario:
{pregunta}

Respuesta:
"""

    try:
        respuesta = client.models.generate_content(
            model=gemini_model,
            contents=prompt
        )

        return respuesta.text

    except Exception as error:
        return manejar_error_gemini(error)
