# Importa Streamlit para crear la interfaz del asistente
import streamlit as st

# Importa los estilos modernos desde estilos_moderno.py
from estilos_moderno import cargar_estilos

# Importa funciones para detectar y crear gráficas matemáticas
from graficador import extraer_funcion_para_graficar, crear_grafica

# Importa la función para convertir voz a texto
from streamlit_mic_recorder import speech_to_text

# Importa la función que conecta con Gemini
from backend import responder_con_gemini


# Configuración general de la página
st.set_page_config(
    page_title="Asistente de Cálculo 1",
    page_icon="∫",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# Carga los estilos CSS personalizados
cargar_estilos()


# Variable para guardar la pregunta actual
if "pregunta" not in st.session_state:
    st.session_state.pregunta = ""


# Variable para guardar el historial
if "historial" not in st.session_state:
    st.session_state.historial = []


# Encabezado principal
st.markdown(
"""
<div class="main-hero">
<div class="hero-badge">Proyecto universitario · IA + Cálculo + Voz</div>

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

st.markdown('<div class="glass-panel">', unsafe_allow_html=True)

st.markdown('<div class="section-title">Historial del asistente</div>', unsafe_allow_html=True)


if len(st.session_state.historial) == 0:

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

    # Muestra mensajes en orden normal:
    # lo viejo arriba y lo nuevo abajo
    for mensaje in st.session_state.historial:

        # Caja general de conversación
        st.markdown('<div class="chat-box">', unsafe_allow_html=True)

        # Usuario
        st.markdown('<div class="msg-label">Usuario</div>', unsafe_allow_html=True)

        st.markdown(
            f'<div class="user-bubble">{mensaje["pregunta"]}</div>',
            unsafe_allow_html=True
        )

        # Asistente
        st.markdown('<div class="msg-label">Asistente</div>', unsafe_allow_html=True)

        # IMPORTANTE:
        # Aquí NO metemos la respuesta dentro de un div HTML.
        # Así Streamlit puede renderizar Markdown y LaTeX correctamente.
        st.markdown(mensaje["respuesta"])

        # Gráfica si existe
        funcion_grafica = mensaje.get("funcion_grafica")

        if funcion_grafica:
            figura = crear_grafica(funcion_grafica)

            if figura:
                st.pyplot(figura)
            else:
                st.warning("No puedo realizar la gráfica.")

        # Cierra caja de conversación
        st.markdown('</div>', unsafe_allow_html=True)


st.markdown('</div>', unsafe_allow_html=True)


# =====================================================
# PANEL DE ENTRADA DEL USUARIO
# =====================================================

st.markdown('<div class="glass-panel">', unsafe_allow_html=True)

st.markdown('<div class="section-title">Realiza una consulta</div>', unsafe_allow_html=True)


col_texto, col_acciones = st.columns([4, 1.15], vertical_alignment="bottom")


with col_texto:
    st.text_area(
        "Escribe tu pregunta:",
        key="pregunta",
        placeholder="Ejemplo: Explícame cómo derivar x^2 + 3x o grafica y = x**2 - 4",
        height=120
    )


with col_acciones:

    texto_voz = speech_to_text(
        language="es",
        start_prompt="🎤 Hablar",
        stop_prompt="⏹️ Detener",
        just_once=True,
        key="voz"
    )

    preguntar = st.button(
        "Enviar consulta",
        use_container_width=True
    )

    borrar_historial = st.button(
        "Limpiar chat",
        use_container_width=True
    )


st.markdown('</div>', unsafe_allow_html=True)


# =====================================================
# ACCIONES
# =====================================================

if texto_voz:
    st.session_state.pregunta = texto_voz
    st.rerun()


if borrar_historial:
    st.session_state.historial = []
    st.session_state.pregunta = ""
    st.rerun()


if preguntar:

    pregunta_limpia = st.session_state.pregunta.strip()

    if pregunta_limpia == "":
        st.warning("Escribe una pregunta primero o usa el botón de voz.")

    else:

        try:

            with st.spinner("El asistente está razonando la respuesta..."):

                respuesta_final = responder_con_gemini(pregunta_limpia)

                funcion_grafica = extraer_funcion_para_graficar(respuesta_final)

            st.session_state.historial.append({
                "pregunta": pregunta_limpia,
                "respuesta": respuesta_final,
                "funcion_grafica": funcion_grafica
            })

            st.session_state.pregunta = ""

            st.rerun()

        except Exception as error:

            st.error(f"Ocurrió un error: {error}")
