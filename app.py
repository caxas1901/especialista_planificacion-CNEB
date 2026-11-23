import os
import streamlit as st
from google import genai

# Configuración visual de la aplicación
st.set_page_config(
    page_title="DocentIA CNEB - Planificador Curricular",
    page_icon="📘",
    layout="wide"
)

# Estilos visuales personalizados
st.markdown("""
    <style>
    .main-header { font-size: 28px; font-weight: 700; color: #1e3a8a; margin-bottom: 0px; }
    .sub-header { font-size: 15px; color: #475569; margin-bottom: 20px; }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] { background-color: #f1f5f9; border-radius: 6px; padding: 8px 16px; font-weight: 600; }
    .stTabs [aria-selected="true"] { background-color: #2563eb !important; color: white !important; }
    </style>
""", unsafe_allow_html=True)

# Encabezado principal
st.markdown('<div class="main-header">📘 DocentIA CNEB: Diseñador Curricular EBR</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Generación de sesiones y unidades alineadas al CNEB (R.M. N.° 281-2016) y R.V.M. N.° 094-2020-MINEDU</div>', unsafe_allow_html=True)

# Instrucciones confidenciales del sistema
SYSTEM_INSTRUCTIONS = """
ROL Y PROPÓSITO GENERAL:
Eres DocentIA CNEB, especialista de élite en Ingeniería Pedagógica, Didáctica Aplicada y Evaluación Formativa para EBR en Perú (Inicial, Primaria, Secundaria y Multigrado).

REGLAS DE ORO OBLIGATORIAS:
1. MATRIZ DE EVALUACIÓN:
   - Formular OBLIGATORIAMENTE al menos UN criterio de evaluación por CADA capacidad de la competencia seleccionada.
   - Estructura del criterio: Habilidad (acción observable) + Contenido conceptual + Condición de calidad y contexto.
   - Incluir siempre los criterios redactados en lenguaje amigable y cercano para el estudiante.
2. SECUENCIA DIDÁCTICA Y MEDIACIÓN COGNITIVA:
   - Inicio: Acogida, problematización / reto contextualizado, saberes previos y propósito compartido.
   - Desarrollo: Procesos didácticos del área, mediación dialógica mediante preguntas socráticas y atención diferenciada/multinivel.
   - Retroalimentación formativa en acción: Aplicar la Escalera de Wilson (Clarificar -> Valorar -> Expresar inquietudes -> Hacer sugerencias).
   - Cierre: Autoevaluación y reflexión metacognitiva.
"""

# Configuración del cliente API con clave protegida
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key and "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]

if not api_key:
    st.error("No se detectó la clave GEMINI_API_KEY en Secrets de Streamlit.")
    st.stop()

client = genai.Client(api_key=api_key)

# Panel lateral con selectores pedagógicos
with st.sidebar:
    st.header("⚙️ Parámetros Curriculares")
    
    nivel = st.selectbox(
        "Nivel Educativo:",
        ["Primaria (Polidocente)", "Primaria (Multigrado / Unidocente)", "Inicial (Ciclo II)", "Secundaria"]
    )
    
    if "Primaria" in nivel:
        grados = st.multiselect(
            "Grado(s) o Ciclos:",
            ["1° grado (Ciclo III)", "2° grado (Ciclo III)", "3° grado (Ciclo IV)", "4° grado (Ciclo IV)", "5° grado (Ciclo V)", "6° grado (Ciclo V)"],
            default=["3° grado (Ciclo IV)", "4° grado (Ciclo IV)"]
        )
    elif "Inicial" in nivel:
        grados = st.multiselect("Edad(s):", ["3 años", "4 años", "5 años"], default=["4 años", "5 años"])
    else:
        grados = st.multiselect("Grado de Secundaria:", ["1°", "2°", "3°", "4°", "5°"], default=["1°", "2°"])

    area = st.selectbox(
        "Área Curricular:",
        ["Ciencia y Tecnología", "Matemática", "Comunicación", "Personal Social", "Desarrollo Personal (DPCC)", "Arte y Cultura"]
    )
    
    duracion = st.select_slider("Duración estimada (minutos):", options=[45, 90, 135, 180], value=90)

# Formulario principal de entrada
col1, col2 = st.columns([2, 1])

with col1:
    titulo_tema = st.text_input(
        "Título o tema eje de la sesión:",
        placeholder="Ej: Indagamos sobre los ecosistemas de nuestra comunidad y su conservación"
    )
    reto_contexto = st.text_area(
        "Situación significativa o reto del contexto:",
        placeholder="Describe brevemente la situación problemática, vivencia local o necesidad de aprendizaje...",
        height=100
    )

with col2:
    competencia = st.text_input(
        "Competencia principal (opcional):",
        placeholder="Ej: Explica el mundo físico basándose en conocimientos..."
    )
    enfoque_transversal = st.selectbox(
        "Enfoque Transversal priorizado:",
        ["Ambiental", "Intercultural", "Orientación al bien común", "Inclusivo o de atención a la diversidad", "Búsqueda de la excelencia", "De derechos"]
    )

# Disparador de generación
if st.button("🚀 Generar Planificación Didáctica", type="primary", use_container_width=True):
    if not titulo_tema.strip():
        st.warning("Por favor ingresa al menos el título o tema eje para estructurar la planificación.")
    else:
        prompt_estructurado = f"""
        POR FAVOR DISEÑA LA SESIÓN DE APRENDIZAJE CON LOS SIGUIENTES PARÁMETROS:
        - Nivel/Modalidad: {nivel}
        - Grados/Edades: {', '.join(grados)}
        - Área: {area}
        - Duración: {duracion} minutos
        - Enfoque transversal: {enfoque_transversal}
        - Título/Tema: {titulo_tema}
        - Situación o contexto: {reto_contexto}
        - Competencia específica solicitada: {competencia if competencia.strip() else 'Seleccionar la más idónea del CNEB'}
        
        REQUISITO DE SALIDA:
        Devuelve el documento completo organizado con las siguientes secciones en Markdown:
        1. DATOS INFORMATIVOS Y PROPÓSITOS DE APRENDIZAJE
        2. MATRIZ DE EVALUACIÓN FORMATIVA (Tabla con Competencia, Capacidades, Criterios de Evaluación y Criterios en lenguaje cercano)
        3. SECUENCIA DIDÁCTICA DETALLADA (Inicio, Desarrollo con procesos didácticos y alternancia si es multigrado, y Cierre con metacognición)
        4. PROTOCOLO DE RETROALIMENTACIÓN (Escalera de Wilson modelada)
        5. ANEXO: INSTRUMENTO FORMATIVO / FICHA DE TRABAJO
        """
        
        with st.spinner("Construyendo planificación técnica de alta granularidad..."):
            # Rotación en cascada de modelos activos en tu cuenta
            modelos_disponibles = ["gemini-3.8-flash", "gemini-flash-latest", "gemini-3.5-flash-lite"]
            respuesta_generada = None
            ultimo_error = ""

            for mod in modelos_disponibles:
                try:
                    response = client.models.generate_content(
                        model=mod,
                        contents=prompt_estructurado,
                        config=genai.types.GenerateContentConfig(
                            system_instruction=SYSTEM_INSTRUCTIONS,
                            temperature=0.3
                        )
                    )
                    if response and response.text:
                        respuesta_generada = response.text
                        break
                except Exception as e:
                    ultimo_error = str(e)
                    continue

            if respuesta_generada:
                st.success("¡Planificación curricular generada exitosamente!")
                st.markdown("---")
                st.markdown(respuesta_generada)
                
                st.download_button(
                    label="📥 Descargar planificación (.txt)",
                    data=respuesta_generada,
                    file_name=f"Sesion_{area.replace(' ', '_')}.txt",
                    mime="text/plain"
                )
            else:
                st.error(f"Los servidores están experimentando alta demanda momentánea. Intenta presionar nuevamente. Detalle: {ultimo_error}")
