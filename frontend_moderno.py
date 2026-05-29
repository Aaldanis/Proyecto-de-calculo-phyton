# Importa Streamlit para crear la interfaz del asistente
import streamlit as st

# Importa los estilos modernos desde el archivo estilos_moderno.py
from estilos_moderno import cargar_estilos

# Importa funciones para detectar y crear gráficas matemáticas
from graficador import extraer_funcion_para_graficar, crear_grafica

# Importa la función para convertir voz a texto
from streamlit_mic_recorder import speech_to_text

# Importa la función que conecta con Gemini
from backend import responder_con_gemini


# Configuración general de la página
# Debe ir antes de mostrar cualquier elemento en pantalla
st.set_page_config(
    page_title="Asistente de Cálculo 1",
    page_icon="∫",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# Carga los estilos CSS personalizados
cargar_estilos()


# Crea la variable para guardar la pregunta actual
if "pregunta" not in st.session_state:
    st.session_state.pregunta = ""


# Crea la variable para guardar el historial de conversación
if "historial" not in st.session_state:
    st.session_state.historial = []


# Encabezado principal de la aplicación
st.markdown(
"""
<div class="main-hero">
<div class="hero-badge"> Proyecto universitario · IA + Cálculo + Voz</div>

<h1 class="hero-title">
Asistente Virtual de <span class="hero-gradient">Cálculo 1</span>
</h1>

<p class="hero-subtitle">
Sistema desarrollado en Python + Streamlit<br>
Proyecto universitario de Inteligencia Artificial aplicada al Cálculo.
</p>

<div class="feature-row">
<div class="feature-card">
<strong>🎤 Entrada por voz</strong>
<span>Permite hacer preguntas habladas.</span>
</div>

<div class="feature-card">
<strong>∫ Enfoque matemático</strong>
<span>Diseñado para temas de Cálculo 1.</span>
</div>

<div class="feature-card">
<strong>📈 Gráficas</strong>
<span>Puede mostrar funciones generadas por Python.</span>
</div>
</div>
</div>
""",
unsafe_allow_html=True
)


# =====================================================
# HISTORIAL DEL CHAT
# =====================================================

# Abre un panel visual para mostrar el historial
st.markdown('<div class="glass-panel">', unsafe_allow_html=True)

# Título del historial
st.markdown('<div class="section-title">Historial del asistente</div>', unsafe_allow_html=True)


# Si todavía no hay mensajes en el historial
if len(st.session_state.historial) == 0:

    # Muestra un mensaje inicial amigable
    st.markdown(
    """
    <div class="empty-chat">
    <h3>Tu conversación aparecerá aquí</h3>
    <p>Haz una pregunta escrita o por voz para iniciar la demostración del asistente.</p>
    </div>
    """,
    unsafe_allow_html=True
    )

else:

    # Recorre el historial en orden inverso
    # Así la respuesta más reciente aparece primero
    for mensaje in st.session_state.historial:

        # Abre una caja para cada conversación
        st.markdown('<div class="chat-box">', unsafe_allow_html=True)

        # Muestra la etiqueta del usuario
        st.markdown('<div class="msg-label">Usuario</div>', unsafe_allow_html=True)

        # Muestra la pregunta del usuario
        st.markdown(
            f'<div class="user-bubble">{mensaje["pregunta"]}</div>',
            unsafe_allow_html=True
        )

        # Muestra la etiqueta del asistente
        st.markdown('<div class="msg-label">Asistente</div>', unsafe_allow_html=True)

        # Muestra la respuesta del asistente
        st.markdown(
            f'<div class="bot-bubble">{mensaje["respuesta"]}</div>',
            unsafe_allow_html=True
        )

        # Obtiene la función detectada para graficar, si existe
        funcion_grafica = mensaje.get("funcion_grafica")

        # Si existe una función para graficar
        if funcion_grafica:

            # Crea la gráfica usando graficador.py
            figura = crear_grafica(funcion_grafica)

            # Si la gráfica se creó correctamente
            if figura:

                # Muestra la gráfica en Streamlit
                st.pyplot(figura)

            else:

                # Si hubo error al graficar, muestra advertencia
                st.warning("No puedo realizar la gráfica.")

        # Cierra la caja del mensaje
        st.markdown('</div>', unsafe_allow_html=True)


# Cierra el panel del historial
st.markdown('</div>', unsafe_allow_html=True)


# =====================================================
# PANEL DE ENTRADA DEL USUARIO
# =====================================================

# Abre el panel donde el usuario escribe o habla
st.markdown('<div class="glass-panel">', unsafe_allow_html=True)

# Título del panel de consulta
st.markdown('<div class="section-title">Realiza una consulta</div>', unsafe_allow_html=True)


# Crea dos columnas:
# una grande para escribir y otra pequeña para botones
col_texto, col_acciones = st.columns([4, 1.15], vertical_alignment="bottom")


# Columna izquierda: caja de texto
with col_texto:

    # Área de texto para escribir la pregunta
    st.session_state.pregunta = st.text_area(
        "Escribe tu pregunta:",
        value=st.session_state.pregunta,
        placeholder="Ejemplo: Explícame cómo derivar x^2 + 3x o grafica y = x**2 - 4",
        height=120
    )


# Columna derecha: botones y micrófono
with col_acciones:

    # Botón de micrófono para convertir voz a texto
    texto_voz = speech_to_text(
        language="es",
        start_prompt="🎤 Hablar",
        stop_prompt="⏹️ Detener",
        just_once=True,
        key="voz"
    )

    # Botón para enviar la consulta
    preguntar = st.button(
        "Enviar consulta",
        use_container_width=True
    )

    # Botón para limpiar el historial
    borrar_historial = st.button(
        "Limpiar chat",
        use_container_width=True
    )


# Cierra el panel de entrada
st.markdown('</div>', unsafe_allow_html=True)


# =====================================================
# ACCIONES DE LOS BOTONES
# =====================================================

# Si el usuario habló por micrófono
if texto_voz:

    # Coloca el texto reconocido en la caja de texto
    st.session_state.pregunta = texto_voz

    # Recarga la interfaz para mostrar el texto reconocido
    st.rerun()


# Si el usuario presiona limpiar chat
if borrar_historial:

    # Limpia el historial completo
    st.session_state.historial = []

    # Limpia también la pregunta actual
    st.session_state.pregunta = ""

    # Recarga la interfaz
    st.rerun()


# Si el usuario presiona enviar consulta
if preguntar:

    # Limpia espacios al inicio y al final de la pregunta
    pregunta_limpia = st.session_state.pregunta.strip()

    # Valida que el usuario haya escrito algo
    if pregunta_limpia == "":

        # Muestra advertencia si la pregunta está vacía
        st.warning("Escribe una pregunta primero o usa el botón de voz.")

    else:

        try:

            # Muestra un mensaje mientras el asistente responde
            with st.spinner("El asistente está razonando la respuesta..."):

                # Envía la pregunta al backend con Gemini
                respuesta_final = responder_con_gemini(pregunta_limpia)

                # Detecta si la respuesta contiene una función para graficar
                funcion_grafica = extraer_funcion_para_graficar(respuesta_final)

            # Guarda la conversación en el historial
            st.session_state.historial.append({
                "pregunta": pregunta_limpia,
                "respuesta": respuesta_final,
                "funcion_grafica": funcion_grafica
            })

            # Limpia la caja de texto después de responder
            st.session_state.pregunta = ""

            # Recarga la interfaz para mostrar la respuesta nueva
            st.rerun()

        except Exception as error:

            # Muestra cualquier error que ocurra en pantalla
            st.error(f"Ocurrió un error: {error}")
