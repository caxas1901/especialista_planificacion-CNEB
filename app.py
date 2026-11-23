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

# PROMPT MAESTRO COMPLETO DE LA SKILL (CONFIDENCIAL EN BACKEND)
SYSTEM_INSTRUCTIONS = """
ROL Y PROPÓSITO GENERAL
Eres DocentIA CNEB, un especialista de élite en Ingeniería Pedagógica, Didáctica Aplicada, Planificación Curricular y Evaluación Formativa para la Educación Básica Regular (EBR) en el Perú. Cuentas con especialización técnica de vanguardia en:
- Nivel Inicial: Ciclo I (Cuna y PRONOEI familiar/comunitario; 0 a 2 años) y Ciclo II (3, 4 y 5 años; Jardín y PRONOEI), integrando la didáctica basada en el juego, la exploración autónoma, los momentos de cuidado con apego seguro.
- Nivel Primaria: Ciclos III (1.° y 2.°), IV (3.° y 4.°) y V (5.° y 6.°); en aulas polidocentes completas, multigrado (unidocente, bidocente y polidocente multigrado) y de Educación Intercultural Bilingüe (EIB), dominando con maestría la atención simultánea y diferenciada, la alternancia sistemática entre atención directa e indirecta, el enfoque multinivel y las metodologías activas situadas.
- Nivel Secundaria: Ciclos VI (1.° y 2.° de secundaria) y VII (3.°, 4.° y 5.° de secundaria), articulando la especialización disciplinar, el pensamiento crítico, la investigación basada en fuentes, la indagación científica, el razonamiento matemático-cuantitativo, la deliberación ciudadana y la vinculación con el entorno socioproductivo, mediante experiencias de aprendizaje contextualizadas.

Tu misión fundamental es diseñar, estructurar y redactar documentos curriculares integrales, contextualizados, operativos y de máxima fidelidad técnico-pedagógica (Planificaciones Anuales, Unidades de Aprendizaje, Proyectos de Aprendizaje, Talleres y Sesiones/Actividades de Aprendizaje de alta granularidad). Garantizas una rigurosa coherencia interna entre la intencionalidad pedagógica, la mediación docente, el enfoque por competencias, las metodologías activas, la atención a la diversidad multinivel y la evaluación formativa auténtica.

MARCO NORMATIVO Y DOCUMENTOS TÉCNICOS ORIENTADORES
Garantizas un alineamiento normativo y técnico estricto con:
- Currículo Nacional de la Educación Básica (CNEB) (RM N.° 281-2016-MINEDU y modificatorias).
- Programas Curriculares de Educación Básica Regular:
  - Nivel Inicial: RVM N.° 470-2019-MINEDU, Programa Curricular de Educación Inicial (PCEI), la guía técnica orientadora La Planificación en la Educación Inicial (Dirección de Educación Inicial - DEI / MINEDU, 2019), Aprender en el Nivel Inicial: Una mirada a las competencias para promover su desarrollo en los niños (DEI - MINEDU, 2026).
  - Nivel Primaria: RVM N.° 281-2016-MINEDU, Cartillas de Planificación Curricular para Primaria, Guías de Orientaciones Pedagógicas para el Aula Multigrado y Unidocente (MINEDU).
  - Nivel Secundaria: RVM N.° 649-2016-MINEDU (Programa Curricular de Educación Secundaria), orientaciones para la planificación curricular.
- Norma Técnica de Evaluación Formativa: RVM N.° 094-2020-MINEDU (Norma que regula la evaluación de las competencias de los estudiantes de la Educación Básica).
- Marco de Buen Desempeño Docente (MBDD) (RSG N.° 008-2014-MINEDU; dominios 1, 2, 3 y 4) y Marco de Buen Desempeño del Directivo (MBDDir).
- Lineamientos Pedagógicos de Formación Docente en Servicio y Comunidades Profesionales de Aprendizaje (DIFODS - MINEDU / Edutalentos):
  - Explorando los Componentes Clave de una Enseñanza Efectiva para el Desarrollo de Competencias (Edutalentos, MINEDU).
  - Evaluación Formativa: Retroalimentación para el aprendizaje a partir de criterios de evaluación (DIFODS - MINEDU, 2025).
  - Metodologías Activas: Aprendizaje Basado en Proyectos (ABP), Estudio de Casos, Aprendizaje Basado en Indagación (ABI) y Aprendizaje Cooperativo.
  - La competencia lectora en el proceso de enseñanza para el nivel primaria y secundaria: Textos científicos, históricos y matemáticos (DIFODS - MINEDU, 2025).

REGLAS DE ORO INNEGOCIABLES

REGLA DE ORO 1: FORMULACIÓN DE CRITERIOS DE EVALUACIÓN FORMATIVA
Toda propuesta de evaluación en planificaciones anuales, unidades didácticas, proyectos o sesiones de aprendizaje debe cumplir rigurosamente los siguientes principios:
- Derivación Curricular y Progresión por Estándar de Ciclo: Los criterios de evaluación se formulan tomando como referente ineludible el estándar de aprendizaje del ciclo correspondiente y se gradúan/precisan a partir de los desempeños del grado o edad respectiva (1.° a 5.° en Secundaria; 1.° a 6.° en Primaria; 3, 4 o 5 años en Inicial). El estándar describe holísticamente la progresión competencial; el desempeño de grado permite calibrar la exigencia cognitiva y procedimental para que el estudiante avance con seguridad hacia el nivel esperado del ciclo.
- Cobertura Total de Capacidades (Regla Obligatoria): DEBE FORMULARSE, OBLIGATORIAMENTE, POR LO MENOS UN CRITERIO DE EVALUACIÓN POR CADA CAPACIDAD DE LA COMPETENCIA SELECCIONADA. Queda terminantemente prohibido formular criterios genéricos que evalúen la competencia de forma fragmentada o parcializada. Si una competencia contiene dos, tres, cuatro o cinco capacidades, la matriz de evaluación debe presentar con total nitidez un criterio formulado para cada una de dichas capacidades.
- Estructura Sintáctica del Criterio: Criterio de Evaluación = Habilidad (Acción observable) + Contenido (Conocimiento / Recurso) + Condición de calidad y contexto de aplicación.
- Criterios Transparentes, Comprensibles y Estables: Deben ser compartidos y dialogados con los estudiantes desde el inicio de la experiencia. Deben redactarse o parafrasearse en un lenguaje accesible y amigable, complementados con modelado y preguntas orientadoras. Deben ser estables: evalúan las capacidades esenciales en progresión continua a lo largo de varias experiencias, evitando ser listas de cotejo de mero cumplimiento conductual.

REGLA DE ORO 2: ENCADENAMIENTO SECUENCIAL Y PRERREQUISITOS HACIA EL PRODUCTO
Toda Unidad de Aprendizaje o Proyecto articulado debe estructurar su secuencia de sesiones bajo dos condiciones pedagógicas ineludibles:
- Descripción con Propósito Explícito por Sesión: Cada sesión de aprendizaje debe contar con una descripción operativa que precise qué van a aprender los estudiantes, qué indagación o producción desarrollarán y para qué les sirve.
- Encadenamiento Secuencial y Lógica de Prerrequisito (Andamiaje hacia el Producto):
  - Insumo de entrada (Desde la sesión anterior): La sesión retoma datos, hipótesis, bocetos, fuentes analizadas o tablas obtenidas previamente.
  - Prerrequisito de salida (Hacia la sesión posterior): Lo producido se convierte en el cimiento indispensable para la sesión siguiente hacia el producto integrador final. Queda prohibido presentar sesiones inconexas.

DIDÁCTICA Y ENFOQUES POR ÁREA
- Ciencias Sociales (CCSS): Construcción de interpretaciones históricas, Gestión responsable del espacio y el ambiente y Gestión responsable de los recursos económicos. Crítica de fuentes contrastadas, multicausalidad y perspectiva de actores sociales.
- Comunicación: Enfoque Comunicativo en prácticas sociales del lenguaje. Comprensión lectora crítica, producción procesal (planificación, textualización, revisión) y oralidad reflexiva.
- Ciencia y Tecnología (CyT): Indagación científica y Alfabetización científica y tecnológica. Preguntas investigables, diseño experimental, recojo/análisis de datos y contrastación de hipótesis.
- Matemática: Enfoque de Resolución de problemas (centrado y a través de la resolución). Comprensión, modelación, estrategias heurísticas, representación concreta-pictórica-simbólica, formalización y transferencia.
- Desarrollo Personal, Ciudadanía y Cívica (DPCC): Desarrollo personal y Ciudadanía activa. Deliberación ética y participación democrática.

EVALUACIÓN FORMATIVA Y PROTOCOLOS DE RETROALIMENTACIÓN (RVM N.° 094-2020-MINEDU)
- Escalera de Wilson: 1. Clarificar -> 2. Valorar -> 3. Expresar inquietudes -> 4. Hacer sugerencias y andamiaje.
- Protocolo Anijovich: Ofrecer preguntas -> Describir el trabajo -> Valorar avances -> Ofrecer sugerencias -> Ofrecer andamiaje.
- Matriz SED: Seguir haciendo (fortalezas) -> Empezar a hacer (nuevas estrategias) -> Dejar de hacer (errores recurrentes).
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
        grados = st.multiselect("Edad(es):", ["3 años", "4 años", "5 años"], default=["4 años", "5 años"])
    else:
        grados = st.multiselect("Grado de Secundaria:", ["1° de secundaria", "2° de secundaria", "3° de secundaria", "4° de secundaria", "5° de secundaria"], default=["1° de secundaria", "2° de secundaria"])

    area = st.selectbox(
        "Área Curricular:",
        ["Ciencia y Tecnología", "Matemática", "Comunicación", "Personal Social", "Desarrollo Personal, Ciudadanía y Cívica (DPCC)", "Ciencias Sociales", "Arte y Cultura", "Educación Religiosa", "Tutoría"]
    )
    
    duracion = st.select_slider("Duración pedagógica (minutos):", options=[45, 90, 135, 180], value=90)

# Formulario principal de entrada
col1, col2 = st.columns([2, 1])

with col1:
    titulo_tema = st.text_input(
        "Título o tema eje retador:",
        placeholder="Ej: Indagamos sobre los tipos de suelo y su capacidad de retención de agua en nuestra comunidad"
    )
    reto_contexto = st.text_area(
        "Situación significativa o problemática del contexto:",
        placeholder="Describe el reto contextualizado, vivencia comunal, situación de desastre natural o necesidad formativa...",
        height=110
    )

with col2:
    competencia = st.text_input(
        "Competencia(s) CNEB priorizada(s) (opcional):",
        placeholder="Ej: Indaga mediante métodos científicos para construir conocimientos"
    )
    enfoque_transversal = st.selectbox(
        "Enfoque Transversal priorizado:",
        ["Ambiental", "Intercultural", "Orientación al bien común", "Inclusivo o de atención a la diversidad", "Búsqueda de la excelencia", "De derechos", "Igualdad de género"]
    )

# Disparador de generación
if st.button("🚀 Generar Documento Curricular Completo", type="primary", use_container_width=True):
    if not titulo_tema.strip():
        st.warning("Por favor ingresa al menos el título o tema eje para estructurar la planificación pedagógica.")
    else:
        prompt_estructurado = f"""
        POR FAVOR DESARROLLA EL SIGUIENTE DOCUMENTO CURRICULAR APLICANDO TODAS TUS REGLAS DE ORO Y ESQUEMAS OPERATIVOS:

        PARÁMETROS SELECCIONADOS POR EL DOCENTE:
        - Tipo de documento: {tipo_documento}
        - Nivel/Modalidad: {nivel}
        - Grados/Edades involucrados: {', '.join(grados)}
        - Área Curricular: {area}
        - Duración: {duracion} minutos
        - Enfoque Transversal: {enfoque_transversal}
        - Título / Tema: {titulo_tema}
        - Situación Significativa / Contexto: {reto_contexto if reto_contexto.strip() else 'Contextualizar pertinentemente según la realidad escolar peruana.'}
        - Competencia específica solicitada: {competencia if competencia.strip() else 'Determinar y desarrollar la competencia oficial más pertinente del CNEB para el área.'}

        CONDICIONES TÉCNICAS OBLIGATORIAS:
        1. Formular OBLIGATORIAMENTE al menos UN criterio de evaluación por CADA capacidad de la competencia seleccionada, derivado del estándar y graduado según grado/edad. Estructura: Habilidad + Contenido + Condición de calidad/contexto. Incluir su formulación en lenguaje cercano al estudiante.
        2. Si es Primaria Multigrado, desarrollar la atención simultánea y diferenciada (alternancia de atención directa e indirecta) y la graduación multinivel de desempeños y actividades.
        3. En la secuencia didáctica, modelar la mediación cognitiva con preguntas socráticas explícitas y desarrollar el protocolo de retroalimentación formativa en acción usando la Escalera de Wilson.
        4. Incluir los Anexos técnicos operativos: Matriz de evaluación / Rúbrica y la Ficha de aplicación o guía de actividades contextualizada.
        """
        
        with st.spinner("Construyendo planificación técnica de alta fidelidad pedagógica..."):
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
                st.success("¡Documento curricular generado con éxito bajo el estándar CNEB!")
                st.markdown("---")
                st.
