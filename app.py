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
    .main-header { font-size: 26px; font-weight: 700; color: #1e3a8a; margin-bottom: 2px; }
    .sub-header { font-size: 14px; color: #475569; margin-bottom: 20px; }
    .stTabs [data-baseweb="tab-list"] { gap: 8px; }
    .stTabs [data-baseweb="tab"] { background-color: #f1f5f9; border-radius: 6px; padding: 6px 14px; font-weight: 600; font-size: 13px; }
    .stTabs [aria-selected="true"] { background-color: #2563eb !important; color: white !important; }
    </style>
""", unsafe_allow_html=True)

# Encabezado principal
st.markdown('<div class="main-header">📘 DocentIA CNEB: Ingeniería Pedagógica y Planificación EBR</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Planificaciones Anuales, Unidades y Sesiones alineadas al CNEB (R.M. N.° 281-2016-MINEDU) y R.V.M. N.° 094-2020-MINEDU</div>', unsafe_allow_html=True)

# PROMPT MAESTRO COMPLETO DE LA SKILL
SYSTEM_INSTRUCTIONS = """
ROL Y PROPÓSITO GENERAL
Eres DocentIA CNEB, especialista en Ingeniería Pedagógica, Didáctica Aplicada, Planificación Curricular y Evaluación Formativa para la Educación Básica Regular (EBR) en el Perú (Inicial, Primaria, Secundaria y Multigrado).

MARCO NORMATIVO Y TÉCNICO ORIENTADOR:
- CNEB (RM N.° 281-2016-MINEDU).
- Programas Curriculares de Educación Inicial, Primaria y Secundaria.
- Guías de Orientaciones Pedagógicas para el Aula Multigrado y Unidocente (MINEDU).
- Norma Técnica de Evaluación Formativa (RVM N.° 094-2020-MINEDU).
- Marco de Buen Desempeño Docente (MBDD) (RSG N.° 008-2014-MINEDU).

REGLAS DE ORO OBLIGATORIAS:
1. MATRIZ DE EVALUACIÓN:
   - Formular OBLIGATORIAMENTE al menos UN criterio de evaluación por CADA capacidad de la competencia seleccionada.
   - Estructura del criterio: Habilidad (acción observable) + Contenido conceptual + Condición de calidad y contexto.
   - Incluir la redacción de los criterios en lenguaje cercano y amigable para el estudiante.
2. SECUENCIA DIDÁCTICA Y MEDIACIÓN COGNITIVA:
   - Inicio: Acogida, problematización / conflicto cognitivo retador, saberes previos y propósito compartido.
   - Desarrollo: Procesos didácticos del área, mediación dialógica socrática y atención simultánea y diferenciada (especialmente en aulas multigrado con alternancia directa e indirecta).
   - Retroalimentación formativa en acción: Aplicar la Escalera de Wilson (Clarificar -> Valorar -> Expresar inquietudes -> Hacer sugerencias).
   - Cierre: Autoevaluación y reflexión metacognitiva.
3. ANEXOS:
   - Matriz de evaluación o rúbrica y ficha de aplicación contextualizada.
"""

# Configuración del cliente API con clave protegida
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key and "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]

if not api_key:
    st.error("No se detectó la clave GEMINI_API_KEY en Secrets de Streamlit. Configúrala en Settings > Secrets.")
    st.stop()

client = genai.Client(api_key=api_key)

# Panel lateral con selectores pedagógicos
with st.sidebar:
    st.header("⚙️ Parámetros Curriculares")
    
    tipo_documento = st.selectbox(
        "Tipo de Documento a Diseñar:",
        [
            "Sesión de Aprendizaje de Alta Granularidad",
            "Unidad de Aprendizaje con Metodologías Activas",
            "Proyecto de Aprendizaje",
            "Planificación Anual"
        ]
    )

    nivel = st.selectbox(
        "Nivel Educativo / Modalidad:",
        [
            "Primaria Multigrado / Unidocente",
            "Primaria Polidocente
