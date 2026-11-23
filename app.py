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
st.caption("Planificacion curricular articulada y evaluacion formativa alineada al CNEB (RM N.° 281-2016-MINEDU) y RVM N.° 094-2020-MINEDU")

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
   - Formular OBLIGATORIAMENTE al menos UN criterio de evaluacion por CADA capacidad de la competencia seleccionada (o de cada area si es integrada).
   - Estructura del criterio: Habilidad (accion observable) + Contenido conceptual + Condicion de calidad y contexto.
   - Redactar los criterios en lenguaje cercano y amigable para el estudiante.
2. SECUENCIA DIDACTICA Y MEDIACION COGNITIVA:
   - Inicio: Acogida, problematizacion o conflicto cognitivo retador, saberes previos y proposito compartido.
   - Desarrollo: Procesos didacticos de las areas seleccionadas, mediacion dialogica socratica y atencion simultanea y diferenciada (especialmente en aulas multigrado con alternancia directa e indirecta).
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

# Opciones estructuradas
OPCIONES_TIPO_DOC = [
    "Sesion de Aprendizaje de Alta Granularidad",
    "Unidad de Aprendizaje con Metodologias Activas",
    "Proyecto de Aprendizaje Interdisciplinar",
    "Planificacion Anual"
]

OPCIONES_NIVEL = [
    "Primaria Multigrado / Unidocente",
    "Primaria Polidocente Completo",
    "Inicial (Ciclo II: 3, 4 y 5 anos)",
    "Secundaria (Ciclos VI y VII)"
]

OPCIONES_GRADOS_TODOS = [
    "Inicial: 3 anos", "Inicial: 4 anos", "Inicial: 5 anos",
    "Primaria: 1° grado (Ciclo III)", "Primaria: 2° grado (Ciclo III)",
    "Primaria: 3° grado (Ciclo IV)", "Primaria: 4° grado (Ciclo IV)",
    "Primaria: 5° grado (Ciclo V)", "Primaria: 6° grado (Ciclo V)",
    "Secundaria: 1° grado (Ciclo VI)", "Secundaria: 2° grado (Ciclo VI)",
    "Secundaria: 3° grado (Ciclo VII)", "Secundaria: 4° grado (Ciclo VII)", "Secundaria: 5° grado (Ciclo VII)"
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
    "Tutoria y Orientacion Educativa"
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

# Panel lateral con seleccion multiple completa
with st.sidebar:
    st.header("Parametros Curriculares")
    
    tipos_doc = st.multiselect(
        "Tipo(s) de Documento a Disenar:",
        OPCIONES_TIPO_DOC,
        default=["Sesion de Aprendizaje de Alta Granularidad"]
    )
    
    niveles = st.multiselect(
        "Nivel(es) o Modalidad(es):",
        OPCIONES_NIVEL,
        default=["Primaria Multigrado / Unidocente"]
    )
    
    grados = st.multiselect(
        "Grado(s) o Edad(es) involucrados:",
        OPCIONES_GRADOS_TODOS,
        default=["Primaria: 3° grado (Ciclo IV)", "Primaria: 4° grado (Ciclo IV)", "Primaria: 5° grado (Ciclo V)"]
    )
    
    areas = st.multiselect(
        "Area(s) Curricular(es) a articular:",
        OPCIONES_AREAS,
        default=["Ciencia y Tecnologia", "Matematica"]
    )
    
    duracion = st.select_slider(
        "Duracion pedagogica estimada (minutos):",
        options=[45, 90, 135, 180, 270, 360],
        value=90
    )

# Formulario principal
col1, col2 = st.columns([2, 1])

with col1:
    titulo_tema = st.text_input(
        "Titulo o tema eje articulador:",
        placeholder="Ej: Indagamos los recursos hidricos y calculamos su consumo responsable en nuestra comunidad"
    )
    reto_contexto = st.text_area(
        "Situacion significativa o reto del contexto:",
        placeholder="Describe el contexto comunal, problema local o situacion desafiante a resolver...",
        height=100
    )

with col2:
    competencia = st.text_input(
        "Competencia(s) CNEB especificas (opcional):",
        placeholder="Ej: Indaga mediante metodos cientificos / Resuelve problemas de cantidad"
    )
    enfoques_transversales = st.multiselect(
        "Enfoque(s) Transversal(es) priorizado(s):",
        OPCIONES_ENFOQUES,
        default=["Ambiental", "Orientacion al bien comun"]
    )

# Disparador de accion
if st.button("🚀 Generar Planificacion Curricular Integrada", type="primary", use_container_width=True):
    if not titulo_tema.strip():
        st.warning("Por favor ingresa un titulo o tema eje articulador.")
    elif not areas:
        st.warning("Por favor selecciona al menos una area curricular.")
    elif not grados:
        st.warning("Por favor selecciona al menos un grado o edad.")
    else:
        tipos_texto = ", ".join(tipos_doc) if tipos_doc else "Sesion de Aprendizaje"
        niveles_texto = ", ".join(niveles) if niveles else "EBR General"
        grados_texto = ", ".join(grados)
        areas_texto = ", ".join(areas)
        enfoques_texto = ", ".join(enfoques_transversales) if enfoques_transversales else "Orientacion al bien comun"

        prompt_estructurado = f"""
        DISENA EL SIGUIENTE DOCUMENTO CURRICULAR ALINEADO AL CNEB:
        - Tipo(s) de documento: {tipos_texto}
        - Nivel(es)/Modalidad: {niveles_texto}
        - Grados/Edades involucrados: {grados_texto}
        - Area(s) articulada(s): {areas_texto}
        - Enfoque(s) transversal(es): {enfoques_texto}
        - Duracion estimada: {duracion} minutos
        - Titulo/Tema eje: {titulo_tema}
        - Situacion o reto del contexto: {reto_contexto if reto_contexto.strip() else 'Contextualizar a la realidad escolar y comunitaria peruana.'}
        - Competencias indicadas por el usuario: {competencia if competencia.strip() else 'Seleccionar e integrar las competencias oficiales del CNEB mas idoneas para las areas elegidas.'}

        CONDICIONES PEDAGOGICAS OBLIGATORIAS:
        1. Formular OBLIGATORIAMENTE al menos UN criterio de evaluacion por CADA capacidad de cada competencia desarrollada, derivado del estandar y graduado para los grados/edades elegidos. Formato: Habilidad + Contenido + Condicion. Incluir version en lenguaje sencillo para los estudiantes.
        2. Articular de forma coherente las areas seleccionadas, mostrando con claridad como se complementan.
        3. En aulas multigrado, estructurar con precision la atencion simultanea y diferenciada (momentos de atencion directa del docente vs atencion indirecta/autonoma con fichas o lideres de equipo).
        4. En la secuencia didactica, incluir procesos didacticos de las areas, preguntas de mediacion socratica y retroalimentacion formativa usando la Escalera de Wilson.
        5. Incluir matrices de evaluacion formativa y ficha practica de aplicacion como anexos.
        """

        with st.spinner("Construyendo planificacion pedagogica integrada de alta granularidad..."):
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
                st.success("¡Planificacion curricular integrada generada con exito!")
                st.markdown("---")
                st.markdown(resultado)

                st.download_button(
                    label="📥 Descargar Documento Curricular (.txt)",
                    data=resultado,
                    file_name=f"Planificacion_{titulo_tema[:15].strip().replace(' ', '_')}.txt",
                    mime="text/plain"
                )
            else:
                st.error(f"Pico de trafico momentaneo en los servidores. Por favor vuelve a hacer clic en Generar. Detalle: {detalle_error}")
