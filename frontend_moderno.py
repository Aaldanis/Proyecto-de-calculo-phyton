# Importa Streamlit para construir la interfaz web del asistente
import streamlit as st

# Importa re para corregir números con puntos de miles
import re

# Importa funciones para detectar y crear gráficas matemáticas
from graficador import extraer_funcion_para_graficar, crear_grafica

# Importa la herramienta para convertir voz a texto
from streamlit_mic_recorder import mic_recorder

# Importa la función del backend que conecta con Gemini
from backend import responder_con_gemini


# Configuración general de la página
st.set_page_config(
    page_title="Asistente Virtual de Cálculo 1",
    page_icon="∫",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =====================================================
# FUNCIÓN PARA COLOCAR VIDEO DE FONDO OPTIMIZADO
# =====================================================

def fondo_video():
    # URL directa del video subido en GitHub
    # Se usa raw.githubusercontent para que Streamlit pueda cargarlo correctamente
    video_url = "https://raw.githubusercontent.com/Aaldanis/Proyecto-de-calculo-phyton/cambios-prueba/fondo.mp4.mp4"

    # Inserta el video como fondo
    # autoplay: inicia solo
    # muted: necesario para que autoplay funcione
    # loop: repite el video
    # playsinline: evita que el celular lo abra en pantalla completa
    # preload="auto": intenta precargarlo para que no quede negro
    st.markdown(
        f"""
        <video autoplay muted loop playsinline preload="auto" id="video-fondo">
            <source src="{video_url}" type="video/mp4">
        </video>
        """,
        unsafe_allow_html=True
    )


# Ejecuta el video de fondo
fondo_video()


# =====================================================
# ESTILOS CSS DE LA INTERFAZ
# =====================================================

st.html("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700;800&family=Inter:wght@400;500;700;800&display=swap');

#video-fondo {
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    object-fit: cover;
    object-position: center center;
    z-index: 0;
    opacity: 0.45;
    pointer-events: none;
     /* Ayuda a que el video no se pause o parpadee en móviles */
    -webkit-transform: translateZ(0);
    transform: translateZ(0);
}

@media (max-width: 768px) {
    #video-fondo {
        object-position: 75% center;
    }
}

.stApp {
    background: transparent !important;
    color: white;
}

[data-testid="stAppViewContainer"] {
    background: transparent !important;
    position: relative;
    z-index: 1;
}

[data-testid="stAppViewContainer"] > .main {
    background: transparent !important;
}

section[data-testid="stSidebar"] {
    z-index: 2;
    background: rgba(3, 7, 18, 0.94);
    border-right: 1px solid rgba(56, 189, 248, 0.35);
}

section[data-testid="stSidebar"] * {
    color: white;
}

.block-container {
    width: min(92vw, 1150px);
    max-width: none;
    padding-top: 3rem;
    padding-bottom: 3rem;
    margin: auto;
}

.sidebar-title {
    font-family: 'Orbitron', sans-serif;
    font-size: 24px;
    font-weight: 800;
    margin-bottom: 30px;
}

.nav-item {
    padding: 14px 16px;
    margin: 10px 0;
    border-radius: 14px;
    background: rgba(15, 23, 42, 0.65);
    border: 1px solid rgba(168, 85, 247, 0.35);
    box-shadow: 0 0 18px rgba(168, 85, 247, 0.12);
    font-weight: 700;
}

.main-hero,
.glass-panel {
    background: rgba(5, 11, 30, 0.35);
    border: 1px solid rgba(56, 189, 248, 0.60);
    border-radius: 26px;
    padding: 36px;
    box-shadow: 0 0 40px rgba(56, 189, 248, 0.22);
    backdrop-filter: blur(14px);
    margin-bottom: 28px;
}

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

.hero-title {
    font-family: 'Inter', sans-serif;
    font-size: 46px;
    line-height: 1.05;
    font-weight: 900;
    color: white;
    margin-bottom: 18px;
}

.hero-gradient {
    background: linear-gradient(90deg, #38bdf8, #a855f7);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero-subtitle {
    color: #dbeafe;
    font-size: 17px;
    line-height: 1.7;
    margin-bottom: 30px;
}

.feature-row {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 14px;
}

.feature-card {
    background: rgba(8, 13, 32, 0.45);
    border: 1px solid rgba(168, 85, 247, 0.55);
    border-radius: 18px;
    padding: 22px;
    min-height: 125px;
    box-shadow: 0 0 22px rgba(168, 85, 247, 0.16);
}

.feature-card strong {
    display: block;
    color: white;
    font-size: 17px;
    margin-bottom: 12px;
}

.feature-card span {
    color: #cbd5e1;
    font-size: 14px;
}

.section-title {
    font-weight: 900;
    font-size: 20px;
    margin-bottom: 18px;
    color: white;
}

.empty-chat {
    background: rgba(2, 6, 23, 0.45);
    border: 1px solid rgba(148, 163, 184, 0.20);
    border-radius: 18px;
    padding: 22px;
    text-align: center;
    color: #cbd5e1;
}

.chat-box {
    background: rgba(2, 6, 23, 0.35);
    border: 1px solid rgba(56, 189, 248, 0.25);
    border-radius: 18px;
    padding: 20px;
    margin-bottom: 18px;
}

.msg-label {
    font-weight: 900;
    color: #67e8f9;
    margin: 10px 0 8px 0;
}

.user-bubble {
    background: linear-gradient(90deg, rgba(37,99,235,0.45), rgba(147,51,234,0.45));
    padding: 14px 16px;
    border-radius: 14px;
    color: white;
    margin-bottom: 12px;
}

textarea {
    background: rgba(2, 6, 23, 0.88) !important;
    color: white !important;
    border: 1px solid rgba(56, 189, 248, 0.75) !important;
    border-radius: 16px !important;
}

.stButton button {
    background: linear-gradient(90deg, #2563eb, #9333ea);
    color: white;
    border: none;
    border-radius: 15px;
    font-weight: 900;
    box-shadow: 0 0 20px rgba(147, 51, 234, 0.38);
}

.stButton button:hover {
    transform: scale(1.03);
    box-shadow: 0 0 28px rgba(56, 189, 248, 0.55);
}

@media (max-width: 900px) {
    .feature-row {
        grid-template-columns: 1fr;
    }

    .hero-title {
        font-size: 34px;
    }
}
</style>
""")


# =====================================================
# BARRA LATERAL
# =====================================================

with st.sidebar:
    st.html('<div class="sidebar-title">Calculo</div>')
    st.html('<div class="nav-item">🏠 Inicio</div>')
    st.html('<div class="nav-item">🎙 Entrada por voz</div>')
    st.html('<div class="nav-item">∑ Enfoque matemático</div>')
    st.html('<div class="nav-item">📊 Gráficas</div>')
    st.html('<div class="nav-item">🕘 Historial</div>')


# =====================================================
# VARIABLES DE SESIÓN
# =====================================================

if "pregunta" not in st.session_state:
    st.session_state.pregunta = ""

if "historial" not in st.session_state:
    st.session_state.historial = []


# =====================================================
# ENCABEZADO PRINCIPAL
# =====================================================

st.html("""
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
""")


# =====================================================
# HISTORIAL DEL ASISTENTE
# =====================================================

st.html('<div class="glass-panel"><div class="section-title">🕘 Historial del asistente</div>')

if len(st.session_state.historial) == 0:
    st.html("""
    <div class="empty-chat">
        <h3>Aún no hay preguntas realizadas.</h3>
        <p>Haz una pregunta escrita o por voz para iniciar la demostración del asistente.</p>
    </div>
    """)
else:
    for mensaje in st.session_state.historial:
        st.html('<div class="chat-box">')
        st.html('<div class="msg-label">Usuario</div>')
        st.html(f'<div class="user-bubble">{mensaje["pregunta"]}</div>')
        st.html('<div class="msg-label">Asistente</div>')

        st.markdown(mensaje["respuesta"])

        funcion_grafica = mensaje.get("funcion_grafica")

        if funcion_grafica:
            figura = crear_grafica(funcion_grafica)

            if figura:
                st.pyplot(figura)
            else:
                st.warning("No puedo realizar la gráfica.")

        st.html('</div>')

st.html('</div>')


# =====================================================
# PANEL DE CONSULTA
# =====================================================

st.html('<div class="glass-panel"><div class="section-title">💬 Realiza una consulta</div>')

col_texto, col_acciones = st.columns([4, 1.15], vertical_alignment="bottom")

with col_texto:
    if "texto_voz_pendiente" in st.session_state:
        st.session_state["pregunta"] = st.session_state["texto_voz_pendiente"]
        del st.session_state["texto_voz_pendiente"]

    st.text_area(
        "Escribe tu pregunta:",
        key="pregunta",
        placeholder="Ejemplo: Explícame cómo derivar x^2 + 3x o grafica y = x**2 - 4",
        height=120
    )

with col_acciones:
        audio = mic_recorder(
            start_prompt="🎤 Hablar",
            stop_prompt="⏹️ Detener",
            just_once=True,
            key="voz"
)

st.write(audio)

    preguntar = st.button("Enviar consulta", use_container_width=True)
    borrar_historial = st.button("Limpiar chat", use_container_width=True)

st.html('</div>')


# =====================================================
# ÁREAS DE DOMINIO
# =====================================================

st.html("""
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
""")


# =====================================================
# FUNCIÓN PARA CORREGIR NÚMEROS DE VOZ
# =====================================================

def corregir_numeros_de_voz(texto):
    # Busca números como 1.000, 5.400, 25.000 o 1.250.000
    patron_miles = r"\b\d{1,3}(?:\.\d{3})+\b"

    # Función interna que elimina los puntos usados como separador de miles
    def quitar_puntos(coincidencia):
        numero = coincidencia.group(0)
        return numero.replace(".", "")

    # Reemplaza todos los números encontrados
    texto_corregido = re.sub(patron_miles, quitar_puntos, texto)

    return texto_corregido


# =====================================================
# ACCIONES DEL USUARIO
# =====================================================

if texto_voz:
    st.session_state["texto_voz_pendiente"] = texto_voz
    st.rerun()

if borrar_historial:
    st.session_state.historial = []

    if "pregunta" in st.session_state:
        del st.session_state["pregunta"]

    st.rerun()

if preguntar:
    pregunta_limpia = corregir_numeros_de_voz(
        st.session_state.pregunta.strip()
    )

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

            if "pregunta" in st.session_state:
                del st.session_state["pregunta"]

            st.rerun()

        except Exception as error:
            st.error(f"Ocurrió un error: {error}")
