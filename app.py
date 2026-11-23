import os
import streamlit as st
from google import genai

# Configuracion de pagina
st.set_page_config(
    page_title="DocentIA CNEB - Planificador Curricular",
    page_icon="📘",
    layout="wide"
)

# Encabezado
st.title("📘 DocentIA CNEB: Planificador Curricular EBR")
st.caption("Planificacion curricular y evaluacion formativa alineada al CNEB (RM N.° 281-2016-MINEDU) y RVM N.° 094-2020-MINEDU")

# Instrucciones pedagogicas confidenciales
SYSTEM_INSTRUCTIONS = """
ROL Y PROPOSITO GENERAL:
Eres DocentIA CNEB, especialista de elite en Ingenieria Pedagogica, Didactica Aplicada, Planificacion Curricular y Evaluacion Formativa para la Educacion Basica Regular (EBR) en el Peru (Inicial, Primaria, Secundaria y Multigrado).

MARCO NORMATIVO Y DOCUMENTOS DE REFERENCIA:
- Curriculo Nacional de la Educacion Basica (CNEB) (RM N.° 281-2016-MINEDU).
- Programas Curriculares de Inicial, Primaria y Secundaria.
- Guias de Orientaciones Pedagogicas para el Aula Multigrado y Unidocente (MINEDU).
- Norma Tecnica de Evaluacion Formativa (RVM N.° 094-2020-MINEDU).
- Marco de Buen Desempeno Docente (MBDD) (RSG N.° 008-2014-MINEDU).

REGLAS DE ORO OBLIGATORIAS:
1. MATRIZ DE EVALUACION FORMATIVA:
   - Formular OBLIGATORIAMENTE al menos UN criterio de evaluacion por CADA capacidad de la competencia seleccionada.
   - Estructura del criterio: Habilidad (accion observable) + Contenido conceptual + Condicion de calidad y contexto.
   - Redactar los criterios en lenguaje cercano y amigable para el estudiante.
2. SECUENCIA DIDACTICA Y MEDIACION COGNITIVA:
   - Inicio: Acogida, problematizacion o conflicto cognitivo retador, saberes previos y proposito compartido.
   - Desarrollo: Procesos didacticos del area, mediacion dialogica socratica y atencion simultanea y diferenciada (especialmente en aulas multigrado con alternancia directa e indirecta).
   - Retroalimentacion formativa en accion: Aplicar la Escalera de Wilson (Clarificar -> Valorar -> Expresar inquietudes -> Hacer sugerencias).
   - Cierre: Autoevaluacion y reflexion metacognitiva.
3. ANEXOS:
   - Matriz de evaluacion o rubrica y ficha de aplicacion contextualizada.
"""

# Obtencion de clave API
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key and "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]

if not api_key:
    st.error("No se detecto la clave GEMINI_API_KEY en Secrets de Streamlit. Agregala en Settings > Secrets.")
    st.stop()

client = genai.Client(api_key=api_key)

# Opciones estructuradas de seleccion
OPCIONES_TIPO_DOC = [
    "Sesion de Aprendizaje de Alta Granularidad",
    "Unidad de Aprendizaje con Metodologias Activas",
    "Proyecto de Aprendizaje",
    "Planificacion Anual"
]

OPCIONES_NIVEL = [
    "Primaria Multigrado / Unidocente",
    "Primaria Polidocente Completo",
    "Inicial (Ciclo II: 3, 4 y 5 anos)",
    "Secundaria (Ciclos VI y VII)"
]

OPCIONES_AREAS = [
    "Ciencia y Tecnologia",
    "Matematica",
    "Comunicacion",
    "Personal Social",
    "Desarrollo Personal, Ciudadania y Civica (DPCC)",
    "Ciencias Sociales",
    "Arte y Cultura",
    "Educacion Religiosa",
    "Tutoria"
]

OPCIONES_ENFOQUES = [
    "Ambiental",
    "Intercultural",
    "Orientacion al bien comun",
    "Inclusivo o de atencion a la diversidad",
    "Busqueda de la excelencia",
    "De derechos",
    "Igualdad de genero"
]

# Panel lateral
with st.sidebar:
    st.header("Parametros Curriculares")
    tipo_doc = st.selectbox("Tipo de Documento:", OPCIONES_TIPO_DOC)
    nivel = st.selectbox("Nivel o Modalidad:", OPCIONES_NIVEL)
    
    if "Primaria" in nivel:
        grados = st.multiselect(
            "Grados:",
            ["1° grado", "2° grado", "3° grado", "4° grado", "5° grado", "6° grado"],
            default=["3° grado", "4° grado", "5° grado"]
        )
    elif "Inicial" in nivel:
        grados = st.multiselect(
            "Edades:",
            ["3 anos", "4 anos", "5 anos"],
            default=["4 anos", "5 anos"]
        )
    else:
        grados = st.multiselect(
            "Grados:",
            ["1° de secundaria", "2° de secundaria", "3° de secundaria", "4° de secundaria", "5° de secundaria"],
            default=["1° de secundaria", "2° de secundaria"]
        )
        
    area = st.selectbox("Area Curricular:", OPCIONES_AREAS)
    duracion = st.select_slider("Duracion (minutos):", options=[45, 90, 135, 180], value=90)

# Formulario principal
col1, col2 = st.columns([2, 1])

with col1:
    titulo_tema = st.text_input(
        "Titulo o tema eje retador:",
        placeholder="Ej: Indagamos sobre la erosion del suelo y el impacto de las lluvias torrenciales"
    )
    reto_contexto = st.text_area(
        "Situacion significativa o reto del contexto:",
        placeholder="Describe el contexto, problema de la comunidad o necesidad de aprendizaje...",
        height=100
    )

with col2:
    competencia = st.text_input(
        "Competencia CNEB priorizada (opcional):",
        placeholder="Ej: Explica el mundo fisico basandose en conocimientos..."
    )
    enfoque_transversal = st.selectbox("Enfoque Transversal:", OPCIONES_ENFOQUES)

# Boton de accion
if st.button("Generar Planificacion Didactica", type="primary", use_container_width=True):
    if not titulo_tema.strip():
        st.warning("Por favor ingresa un titulo o tema para generar la planificacion.")
    else:
        grados_texto = ", ".join(grados) if grados else "No especificado"
        prompt_estructurado = f"""
        DISENA EL SIGUIENTE DOCUMENTO CURRICULAR ALINEADO AL CNEB:
        - Tipo de documento: {tipo_doc}
        - Nivel/Modalidad: {nivel}
        - Grados/Edades: {grados_texto}
        - Area: {area}
        - Duracion: {duracion} minutos
        - Enfoque transversal: {enfoque_transversal}
        - Titulo/Tema: {titulo_tema}
        - Contexto: {reto_contexto if reto_contexto.strip() else 'Contextualizar a la realidad escolar peruana.'}
        - Competencia solicitada: {competencia if competencia.strip() else 'Seleccionar la competencia oficial mas idonea del CNEB.'}

        CONDICIONES OBLIGATORIAS:
        1. Formular al menos UN criterio de evaluacion por CADA capacidad de la competencia seleccionada, derivado del estandar y graduado a los grados elegidos. Estructura: Habilidad + Contenido + Condicion. Incluir version en lenguaje cercano al estudiante.
        2. Si es Primaria Multigrado, estructurar la atencion simultanea y diferenciada (atencion directa e indirecta) con actividades multinivel.
        3. En el desarrollo, detallar procesos didacticos del area, preguntas socraticas y protocolo de retroalimentacion con Escalera de Wilson.
        4. Incluir matriz de evaluacion y ficha de trabajo como anexos.
        """

        with st.spinner("Construyendo planificacion pedagogica de alta calidad..."):
            modelos_pool = ["gemini-3.8-flash", "gemini-flash-latest", "gemini-3.5-flash-lite"]
            resultado = None
            detalle_error = ""

            for mod in modelos_pool:
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
                        resultado = response.text
                        break
                except Exception as e:
                    detalle_error = str(e)
                    continue

            if resultado:
                st.success("Planificacion curricular generada exitosamente.")
                st.markdown("---")
                st.markdown(resultado)

                st.download_button(
                    label="Descargar Documento (.txt)",
                    data=resultado,
                    file_name=f"Planificacion_{area.replace(' ', '_')}.txt",
                    mime="text/plain"
                )
            else:
                st.error(f"Pico de trafico temporal en los servidores. Por favor vuelve a hacer clic en Generar. Detalle: {detalle_error}")
