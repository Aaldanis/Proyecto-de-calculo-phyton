# Importa Streamlit para construir la interfaz web del asistente
import streamlit as st

# Importa la función que detecta funciones matemáticas dentro de la respuesta
# y la función que genera la gráfica usando Python
from graficador import extraer_funcion_para_graficar, crear_grafica

# Importa la herramienta que permite convertir voz a texto dentro de Streamlit
from streamlit_mic_recorder import speech_to_text

# Importa la función del backend que conecta con Gemini para generar respuestas
from backend import responder_con_gemini


# Configuración general de la página de Streamlit
st.set_page_config(
    page_title="Asistente Virtual de Cálculo 1",  # Título que aparece en la pestaña del navegador
    page_icon="∫",                               # Ícono de la aplicación
    layout="wide",                               # Usa el ancho completo de la pantalla
    initial_sidebar_state="expanded"             # Muestra la barra lateral abierta al iniciar
)


# CSS personalizado para darle estilo moderno tipo cyberpunk a la interfaz
st.markdown("""
<style>

/* Importa fuentes modernas desde Google Fonts */
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700;800&family=Inter:wght@400;500;700;800&display=swap');

/* Estilo general de toda la aplicación */
.stApp {
    background:
        linear-gradient(rgba(2, 6, 23, 0.50), rgba(2, 6, 23, 0.70)),
        url("https://i.imgur.com/8Km9tLL.jpeg");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
    color: white;
}

/* Contenedor principal donde va el contenido */
.block-container {
    max-width: 980px;
    padding-top: 3rem;
    padding-bottom: 3rem;
}

/* Estilo de la barra lateral */
section[data-testid="stSidebar"] {
    background: rgba(3, 7, 18, 0.94);
    border-right: 1px solid rgba(56, 189, 248, 0.35);
}

/* Hace que el texto de la barra lateral sea blanco */
section[data-testid="stSidebar"] * {
    color: white;
}

/* Título del menú lateral */
.sidebar-title {
    font-family: 'Orbitron', sans-serif;
    font-size: 24px;
    font-weight: 800;
    margin-bottom: 30px;
}

/* Elementos visuales del menú lateral */
.nav-item {
    padding: 14px 16px;
    margin: 10px 0;
    border-radius: 14px;
    background: rgba(15, 23, 42, 0.65);
    border: 1px solid rgba(168, 85, 247, 0.35);
    box-shadow: 0 0 18px rgba(168, 85, 247, 0.12);
    font-weight: 700;
}

/* Tarjeta principal del encabezado */
.main-hero {
    background: rgba(5, 11, 30, 0.82);
    border: 1px solid rgba(56, 189, 248, 0.60);
    border-radius: 26px;
    padding: 36px;
    box-shadow:
        0 0 40px rgba(56, 189, 248, 0.22),
        inset 0 0 30px rgba(147, 51, 234, 0.08);
    backdrop-filter: blur(14px);
    margin-bottom: 28px;
}

/* Etiqueta pequeña superior del encabezado */
.hero-badge {
    display: inline-block;
    padding: 9px 18px;
    border-radius: 999px;
    background: rgba(8, 145, 178, 0.22);
    border: 1px solid rgba(34, 211, 238, 0.65);
    color: #67e8f9;
    font-weight: 800;
    font-size: 13px;
    box-shadow: 0 0 18px rgba(34, 211, 238, 0.30);
    margin-bottom: 24px;
}

/* Título principal */
.hero-title {
    font-family: 'Inter', sans-serif;
    font-size: 46px;
    line-height: 1.05;
    font-weight: 900;
    color: #ffffff;
    margin-bottom: 18px;
}

/* Efecto degradado para la palabra Cálculo 1 */
.hero-gradient {
    background: linear-gradient(90deg, #38bdf8, #a855f7);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

/* Subtítulo del encabezado */
.hero-subtitle {
    color: #dbeafe;
    font-size: 17px;
    line-height: 1.7;
    margin-bottom: 30px;
}

/* Fila donde se colocan las tarjetas pequeñas */
.feature-row {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 14px;
}

/* Tarjetas pequeñas de características */
.feature-card {
    background: rgba(8, 13, 32, 0.88);
    border: 1px solid rgba(168, 85, 247, 0.55);
    border-radius: 18px;
    padding: 22px;
    min-height: 125px;
    box-shadow: 0 0 22px rgba(168, 85, 247, 0.16);
}

/* Título de cada tarjeta pequeña */
.feature-card strong {
    display: block;
    color: white;
    font-size: 17px;
    margin-bottom: 12px;
}

/* Texto de cada tarjeta pequeña */
.feature-card span {
    color: #cbd5e1;
    font-size: 14px;
}

/* Paneles de vidrio para historial, entrada y áreas */
.glass-panel {
    background: rgba(5, 11, 30, 0.82);
    border: 1px solid rgba(96, 165, 250, 0.45);
    border-radius: 24px;
    padding: 28px;
    margin-bottom: 28px;
    box-shadow: 0 0 32px rgba(59, 130, 246, 0.18);
    backdrop-filter: blur(14px);
}

/* Título de cada sección */
.section-title {
    font-weight: 900;
    font-size: 20px;
    margin-bottom: 18px;
    color: #ffffff;
}

/* Caja que aparece cuando todavía no hay conversación */
.empty-chat {
    background: rgba(2, 6, 23, 0.75);
    border: 1px solid rgba(148, 163, 184, 0.20);
    border-radius: 18px;
    padding: 22px;
    text-align: center;
    color: #cbd5e1;
}

/* Caja de cada conversación */
.chat-box {
    background: rgba(2, 6, 23, 0.72);
    border: 1px solid rgba(56, 189, 248, 0.25);
    border-radius: 18px;
    padding: 20px;
    margin-bottom: 18px;
}

/* Etiquetas Usuario y Asistente */
.msg-label {
    font-weight: 900;
    color: #67e8f9;
    margin: 10px 0 8px 0;
}

/* Burbuja donde aparece la pregunta del usuario */
.user-bubble {
    background: linear-gradient(90deg, rgba(37,99,235,0.55), rgba(147,51,234,0.55));
    padding: 14px 16px;
    border-radius: 14px;
    color: white;
    margin-bottom: 12px;
}

/* Estilo de la caja de texto */
textarea {
    background: rgba(2, 6, 23, 0.88) !important;
    color: white !important;
    border: 1px solid rgba(56, 189, 248, 0.75) !important;
    border-radius: 16px !important;
}

/* Estilo general de los botones */
.stButton button {
    background: linear-gradient(90deg, #2563eb, #9333ea);
    color: white;
    border: none;
    border-radius: 15px;
    font-weight: 900;
    box-shadow: 0 0 20px rgba(147, 51, 234, 0.38);
}

/* Efecto al pasar el mouse sobre botones */
.stButton button:hover {
    transform: scale(1.03);
    box-shadow: 0 0 28px rgba(56, 189, 248, 0.55);
}

/* Diseño responsivo para pantallas pequeñas */
@media (max-width: 900px) {
    .feature-row {
        grid-template-columns: 1fr;
    }

    .hero-title {
        font-size: 34px;
    }
}

</style>
""", unsafe_allow_html=True)


# Barra lateral izquierda de la aplicación
with st.sidebar:

    # Título visual del menú lateral
    st.markdown('<div class="sidebar-title">🧠 Aldanis AI</div>', unsafe_allow_html=True)

    # Opciones decorativas del menú lateral
    st.markdown('<div class="nav-item">🏠 Inicio</div>', unsafe_allow_html=True)
    st.markdown('<div class="nav-item">🎙 Entrada por voz</div>', unsafe_allow_html=True)
    st.markdown('<div class="nav-item">∑ Enfoque matemático</div>', unsafe_allow_html=True)
    st.markdown('<div class="nav-item">📊 Gráficas</div>', unsafe_allow_html=True)
    st.markdown('<div class="nav-item">🕘 Historial</div>', unsafe_allow_html=True)


# Crea la variable de sesión para guardar la pregunta actual
if "pregunta" not in st.session_state:
    st.session_state.pregunta = ""


# Crea la variable de sesión para guardar el historial de conversación
if "historial" not in st.session_state:
    st.session_state.historial = []


# Encabezado principal de la aplicación
st.markdown("""
<div class="main-hero">

    <div class="hero-badge">Proyecto universitario · IA + Cálculo + Voz</div>

    <h1 class="hero-title">
        Asistente Virtual de <span class="hero-gradient">Cálculo 1</span>
    </h1>

    <p class="hero-subtitle">
        Sistema desarrollado en Python + Streamlit.<br>
        Proyecto universitario de Inteligencia Artificial aplicada al Cálculo.
    </p>

    <div class="feature-row">

        <div class="feature-card">
            <strong>🎤 Entrada por voz</strong>
            <span>Permite hacer preguntas habladas.</span>
        </div>

        <div class="feature-card">
            <strong>∑ Enfoque matemático</strong>
            <span>Diseñado para temas de Cálculo 1.</span>
        </div>

        <div class="feature-card">
            <strong>📈 Gráficas</strong>
            <span>Puede mostrar funciones generadas por Python.</span>
        </div>

    </div>

</div>
""", unsafe_allow_html=True)


# Panel visual para mostrar el historial del asistente
st.markdown('<div class="glass-panel">', unsafe_allow_html=True)

# Título del historial
st.markdown('<div class="section-title">🕘 Historial del asistente</div>', unsafe_allow_html=True)


# Si no hay mensajes en el historial, muestra un mensaje inicial
if len(st.session_state.historial) == 0:

    st.markdown("""
    <div class="empty-chat">
        <h3>Aún no hay preguntas realizadas.</h3>
        <p>Haz una pregunta escrita o por voz para iniciar la demostración del asistente.</p>
    </div>
    """, unsafe_allow_html=True)

# Si ya hay mensajes, los muestra uno por uno
else:

    # Recorre todos los mensajes guardados en el historial
    for mensaje in st.session_state.historial:

        # Abre una caja visual para cada conversación
        st.markdown('<div class="chat-box">', unsafe_allow_html=True)

        # Muestra la etiqueta del usuario
        st.markdown('<div class="msg-label">Usuario</div>', unsafe_allow_html=True)

        # Muestra la pregunta hecha por el usuario
        st.markdown(
            f'<div class="user-bubble">{mensaje["pregunta"]}</div>',
            unsafe_allow_html=True
        )

        # Muestra la etiqueta del asistente
        st.markdown('<div class="msg-label">Asistente</div>', unsafe_allow_html=True)

        # Muestra la respuesta del asistente con soporte Markdown y LaTeX
        st.markdown(mensaje["respuesta"])

        # Obtiene una posible función matemática para graficar
        funcion_grafica = mensaje.get("funcion_grafica")

        # Si existe una función detectable, intenta crear la gráfica
        if funcion_grafica:

            # Genera la figura usando la función del archivo graficador.py
            figura = crear_grafica(funcion_grafica)

            # Si la figura se creó correctamente, la muestra
            if figura:
                st.pyplot(figura)

            # Si no pudo crear la gráfica, muestra advertencia
            else:
                st.warning("No puedo realizar la gráfica.")

        # Cierra la caja visual de la conversación
        st.markdown('</div>', unsafe_allow_html=True)


# Cierra el panel del historial
st.markdown('</div>', unsafe_allow_html=True)


# Panel donde el usuario escribe o dicta su consulta
st.markdown('<div class="glass-panel">', unsafe_allow_html=True)

# Título del panel de consulta
st.markdown('<div class="section-title">💬 Realiza una consulta</div>', unsafe_allow_html=True)


# Crea dos columnas: una grande para texto y otra para botones
col_texto, col_acciones = st.columns([4, 1.15], vertical_alignment="bottom")


# Columna izquierda donde va la caja de texto
with col_texto:

    # Si existe texto pendiente reconocido por voz, lo coloca en la pregunta
    if "texto_voz_pendiente" in st.session_state:

        # Copia el texto de voz reconocido a la caja de texto
        st.session_state["pregunta"] = st.session_state["texto_voz_pendiente"]

        # Borra la variable temporal para evitar repetir el texto
        del st.session_state["texto_voz_pendiente"]

    # Caja de texto para que el usuario escriba su pregunta
    st.text_area(
        "Escribe tu pregunta:",
        key="pregunta",
        placeholder="Ejemplo: Explícame cómo derivar x^2 + 3x o grafica y = x**2 - 4",
        height=120
    )


# Columna derecha donde van los botones y el micrófono
with col_acciones:

    # Botón de voz que convierte audio hablado en texto
    texto_voz = speech_to_text(
        language="es",
        start_prompt="🎤 Hablar",
        stop_prompt="⏹️ Detener",
        just_once=True,
        key="voz"
    )

    # Botón para enviar la consulta al asistente
    preguntar = st.button(
        "Enviar consulta",
        use_container_width=True
    )

    # Botón para limpiar todo el historial del chat
    borrar_historial = st.button(
        "Limpiar chat",
        use_container_width=True
    )


# Cierra el panel de consulta
st.markdown('</div>', unsafe_allow_html=True)


# Panel informativo con las áreas que domina el asistente
st.markdown("""
<div class="glass-panel">

    <div class="section-title">⭐ Áreas de dominio</div>

    <div class="feature-row">

        <div class="feature-card">
            <strong>1. Límites y continuidad</strong>
            <span>Análisis de límites laterales, indeterminaciones y continuidad.</span>
        </div>

        <div class="feature-card">
            <strong>2. Derivadas</strong>
            <span>Reglas de derivación, razón de cambio y optimización.</span>
        </div>

        <div class="feature-card">
            <strong>3. Integrales</strong>
            <span>Integrales definidas, indefinidas y técnicas básicas.</span>
        </div>

    </div>

</div>
""", unsafe_allow_html=True)


# Si el usuario habló por micrófono, se guarda el texto reconocido
if texto_voz:

    # Guarda el texto convertido desde voz en una variable temporal
    st.session_state["texto_voz_pendiente"] = texto_voz

    # Recarga la app para colocar el texto en el área de escritura
    st.rerun()


# Si el usuario presiona el botón de limpiar historial
if borrar_historial:

    # Limpia todos los mensajes guardados
    st.session_state.historial = []

    # Elimina la pregunta actual si existe
    if "pregunta" in st.session_state:
        del st.session_state["pregunta"]

    # Recarga la aplicación para mostrar el historial vacío
    st.rerun()


# Si el usuario presiona el botón de enviar consulta
if preguntar:

    # Limpia espacios innecesarios de la pregunta
    pregunta_limpia = st.session_state.pregunta.strip()

    # Valida que el usuario no envíe una pregunta vacía
    if pregunta_limpia == "":

        # Muestra advertencia si no escribió ni dictó nada
        st.warning("Escribe una pregunta primero o usa el botón de voz.")

    # Si la pregunta sí tiene contenido, se procesa
    else:

        try:

            # Muestra una animación mientras Gemini genera la respuesta
            with st.spinner("El asistente está razonando la respuesta..."):

                # Envía la pregunta al backend para obtener la respuesta
                respuesta_final = responder_con_gemini(pregunta_limpia)

                # Busca si la respuesta contiene una función que pueda graficarse
                funcion_grafica = extraer_funcion_para_graficar(respuesta_final)

            # Guarda la pregunta, respuesta y posible gráfica en el historial
            st.session_state.historial.append({
                "pregunta": pregunta_limpia,
                "respuesta": respuesta_final,
                "funcion_grafica": funcion_grafica
            })

            # Limpia la caja de texto eliminando la variable de sesión
            if "pregunta" in st.session_state:
                del st.session_state["pregunta"]

            # Recarga la interfaz para mostrar la nueva respuesta
            st.rerun()

        # Captura cualquier error que ocurra durante la ejecución
        except Exception as error:

            # Muestra el error en pantalla sin romper toda la aplicación
            st.error(f"Ocurrió un error: {error}")
