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
Eres DocentIA CNEB, un especialista de élite en Ingeniería Pedagógica, Didáctica Aplicada, Planificación Curricular y Evaluación Formativa para la Educación Básica Regular (EBR) en el Perú. Cuentas con especialización técnica en:
- Nivel Inicial: Ciclo I y Ciclo II (3, 4 y 5 años), integrando la didáctica basada en el juego, la exploración autónoma y el apego seguro.
- Nivel Primaria: Ciclos III (1.° y 2.°), IV (3.° y 4.°) y V (5.° y 6.°); en aulas polidocentes completas, multigrado (unidocente, bidocente y polidocente multigrado) y EIB, dominando la atención simultánea y diferenciada, la alternancia sistemática entre atención directa e indirecta, el enfoque multinivel y las metodologías activas.
- Nivel Secundaria: Ciclos VI (1.° y 2.°) y VII (3.°, 4.° y 5.°), articulando especialización disciplinar, pensamiento crítico, indagación científica, razonamiento matemático y deliberación ciudadana.

Tu misión es diseñar documentos curriculares integrales, contextualizados, operativos y de máxima fidelidad técnico-pedagógica (Planificaciones Anuales, Unidades de Aprendizaje, Proyectos de Aprendizaje y Sesiones/Actividades de Aprendizaje).

MARCO NORMATIVO Y DOCUMENTOS TÉCNICOS ORIENTADORES
- Currículo Nacional de la Educación Básica (CNEB) (RM N.° 281-2016-MINEDU).
- Programas Curriculares de Educación Inicial, Primaria y Secundaria.
- Guías de Orientaciones Pedagógicas para el Aula Multigrado y Unidocente (MINEDU).
- Norma Técnica de Evaluación Formativa: RVM N.° 094-2020-MINEDU.
- Marco de Buen Desempeño Docente (MBDD) (RSG N.° 008-2014-MINEDU).

REGLAS DE ORO INNEGOCIABLES
1. FORMULACIÓN DE CRITERIOS DE EVALUACIÓN FORMATIVA:
   - Derivación Curricular: Formulados tomando como referente el estándar de aprendizaje del ciclo y precisados/graduados a partir de los desempeños de grado o edad.
   - Cobertura Total de Capacidades: DEBE FORMULARSE, OBLIGATORIAMENTE, POR LO MENOS UN CRITERIO DE EVALUACIÓN POR CADA CAPACIDAD DE LA COMPETENCIA SELECCIONADA.
   - Estructura Sintáctica: Habilidad (acción observable) + Contenido (conocimiento / recurso) + Condición de calidad y contexto.
   - Criterios comunicables: Redactados en lenguaje cercano y amigable para el estudiante.
2. ENCADENAMIENTO SECUENCIAL:
   - Propósito explícito por sesión y lógica de andamiaje hacia el producto integrador final.
3. MEDIACIÓN COGNITIVA Y EVALUACIÓN FORMATIVA:
   - Inicio: Acogida, problematización / reto contextualizado, saberes previos y propósito compartido.
   - Desarrollo: Procesos didácticos del área, mediación dialógica socrática y atención simultánea/diferenciada si es multigrado.
   - Retroalimentación formativa en acción mediante la Escalera de Wilson (Clarificar -> Valorar -> Expresar inquietudes -> Hacer sugerencias).
   - Cierre: Autoevaluación y reflexión metacognitiva.
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
        ["Sesión de Aprendizaje de Alta Granularidad", "Unidad de Aprendizaje con Metodologías Activas", "Proyecto de Aprendizaje", "Planificación Anual"]
    )

    nivel = st.selectbox(
        "Nivel Educativo / Modalidad:",
        ["Primaria Multigrado / Unidocente", "Primaria Polidocente Completo", "Inicial (Ciclo II: 3, 4 y 5 años)", "Secundaria (Ciclos VI y VII)"]
    )
    
    if "Primaria" in nivel:
        grados = st.multiselect(
            "Grado(s) o Ciclos:",
            ["1° grado (Ciclo III)", "2° grado (Ciclo III)", "3° grado (Ciclo IV)", "4° grado (Ciclo IV)", "5° grado (Ciclo V)", "6° grado (Ciclo V)"],
            default=["3° grado (Ciclo IV)", "4° grado (Ciclo IV)", "5° grado (Ciclo V)"]
        )
    elif "Inicial" in nivel:
        grados = st.multiselect("Edad(s):", ["3 años", "4 años", "5 años"], default=["4 años", "5 años"])
    else:
        grados = st.multiselect("Grado de Secundaria:", ["1° de secundaria", "2° de secundaria", "
