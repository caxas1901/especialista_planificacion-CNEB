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
st.caption("Planificacion curricular anual, unidades y sesiones alineadas al CNEB (RM N.° 281-2016-MINEDU) y RVM N.° 094-2020-MINEDU")

# Instrucciones pedagogicas confidenciales
SYSTEM_INSTRUCTIONS = """
ROL Y PROPOSITO GENERAL:
Eres DocentIA CNEB, especialista de elite en Ingenieria Pedagogica, Didactica Aplicada, Planificacion Curricular y Evaluacion Formativa para la Educacion Basica Regular (EBR) en el Peru (Inicial, Primaria, Secundaria y Multigrado).

MARCO NORMATIVO Y DOCUMENTOS DE REFERENCIA:
- Curriculo Nacional de la Educacion Basica (CNEB) (RM N.° 281-2016-MINEDU).
- Programas Curriculares de Inicial, Primaria y Secundaria.
- Cartilla de Orientaciones para la Planificacion Curricular Anual en Aula Multigrado (MINEDU).
- Guias de Orientaciones Pedagogicas para el Aula Multigrado y Unidocente (MINEDU).
- Norma Tecnica de Evaluacion Formativa (RVM N.° 094-2020-MINEDU).
- Marco de Buen Desempeno Docente (MBDD) (RSG N.° 008-2014-MINEDU).

REGLAS DE ORO PARA PLANIFICACION ANUAL (SEGUN CARTILLA MULTIGRADO):
1. MATRIZ DE PLANIFICACION ANUAL:
   - Organizar las unidades didacticas cronologicamente por periodos (bimestres o trimestres) asegurando la cobertura de semanas lectivas y semanas de gestion.
   - Partir estrictamente del diagnostico: articular el calendario comunal (siembra, cosecha, festividades, clima) con las situaciones significativas.
   - Plantear situaciones significativas desafiantes para cada unidad con titulos motivadores, explicitando la metodologia activa seleccionada (ABP, ABPr, ABI, Estudio de casos).
   - Distribuir las competencias priorizadas y relacionadas, garantizando la progresion por ciclos (III, IV, V o secundaria) y el tratamiento de los enfoques transversales.
   - Proponer productos o evidencias integradoras para cada unidad didactica y prever talleres multinivel para atender necesidades de aprendizaje diagnosticadas.

REGLAS DE ORO PARA UNIDADES Y SESIONES:
1. MATRIZ DE EVALUACION FORMATIVA:
   - Formular OBLIGATORIAMENTE al menos UN criterio de evaluacion por CADA capacidad de cada competencia seleccionada.
   - Estructura: Habilidad (accion observable) + Contenido conceptual + Condicion de calidad/contexto.
   - Redactar los criterios en lenguaje cercano y amigable para el estudiante.
2. SECUENCIA DIDACTICA Y MEDIACION COGNITIVA:
   - Inicio: Acogida, problematizacion o conflicto cognitivo retador, saberes previos y proposito compartido.
   - Desarrollo: Procesos didacticos de las areas, atencion simultanea y diferenciada (alternancia directa e indirecta) y retroalimentacion formativa usando la Escalera de Wilson.
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
    "Planificacion Curricular Anual",
    "Unidad de Aprendizaje con Metodologias Activas",
    "Proyecto de Aprendizaje Interdisciplinar",
    "Sesion de Aprendizaje de Alta Granularidad"
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
    "Personal Social",
    "Comunicacion",
    "Matematica",
    "Ciencia y Tecnologia",
    "Desarrollo Personal, Ciudadania y Civica (DPCC)",
    "Ciencias Sociales",
    "Arte y Cultura",
    "Educacion Religiosa",
    "Tutoria y Orientacion Educativa"
]

OPCIONES_ENFOQUES = [
    "De derechos",
    "Inclusivo o de atencion a la diversidad",
    "Intercultural",
    "Igualdad de genero",
    "Ambiental",
    "Orientacion al bien comun",
    "Busqueda de la excelencia"
]

# Panel lateral
with st.sidebar:
    st.header("Parametros Generales")
    
    tipos_doc = st.multiselect(
        "Tipo(s) de Documento a Disenar:",
        OPCIONES_TIPO_DOC,
        default=["Planificacion Curricular Anual"]
    )
    
    niveles = st.multiselect(
        "Nivel(es) o Modalidad(es):",
        OPCIONES_NIVEL,
        default=["Primaria Multigrado / Unidocente"]
    )
    
    grados = st.multiselect(
        "Grado(s) o Edad(es) a cargo:",
        OPCIONES_GRADOS_TODOS,
        default=["Primaria: 3° grado (Ciclo IV)", "Primaria: 4° grado (Ciclo IV)", "Primaria: 5° grado (Ciclo V)"]
    )
    
    areas = st.multiselect(
        "Area(s) Curricular(es):",
        OPCIONES_AREAS,
        default=["Personal Social", "Comunicacion", "Matematica", "Ciencia y Tecnologia"]
    )

es_plan_anual = any("Planificacion Curricular Anual" in doc for doc in tipos_doc)

# Formulario principal dinamico
if es_plan_anual:
    st.subheader("📋 Insumos Obligatorios para la Planificacion Anual (Segun Cartilla Multigrado)")
    st.info("Para estructurar una planificacion anual pertinente y articulada, ingresa la informacion recogida en el diagnostico de tu comunidad y aula.")
    
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.markdown("**1. Diagnostico del Contexto Sociocultural**")
        cal_comunal = st.text_area(
            "Calendario Comunal y Festividades:",
            placeholder="Ej: Siembra de maiz (octubre-noviembre), cosecha (mayo-junio), fiesta patronal San Juan, epoca de lluvias torrenciales (enero a marzo)...",
            height=95
        )
        problemas_potencialidades = st.text_area(
            "Problemas, Coyunturas y Potencialidades Locales:",
            placeholder="Ej: Problemas de contaminacion de fuentes de agua, heladas, saberes ancestrales sobre plantas medicinales, asociacion de productores ganaderos...",
            height=95
        )
        demandas_ppff = st.text_input(
            "Demandas y expectativas de las familias (PP. FF.):",
            placeholder="Ej: Que aprendan a calcular costos de venta de sus cosechas, expresarse con seguridad..."
        )
        
    with col_b:
        st.markdown("**2. Diagnostico de Estudiantes y Aprendizajes**")
        intereses_estudiantes = st.text_area(
            "Intereses de los Estudiantes y Clima Socioemocional:",
            placeholder="Ej: Les gusta aprender jugando y elaborando maquetas; uso de tablets; requieren fortalecer regulacion emocional y trabajo en equipo...",
            height=95
        )
        necesidades_aprendizaje = st.text_area(
            "Necesidades de Aprendizaje Priorizadas (Resultados Diagnostico / SIAGIE):",
            placeholder="Ej: Dificultad en resolucion de problemas de dos etapas en 3° y 4°; en Comunicacion requieren andamiaje en deduccion e inferencia de textos...",
            height=95
        )
        periodos_tiempo = st.selectbox(
            "Organizacion temporal del ano escolar:",
            ["4 Bimestres (con semanas de gestion intermedias)", "3 Trimestres (con semanas de gestion intermedias)"]
        )

    enfoques_transversales = st.multiselect(
        "Enfoques Transversales a priorizar durante el ano escolar:",
        OPCIONES_ENFOQUES,
        default=["Ambiental", "Intercultural", "Orientacion al bien comun"]
    )
    
    titulo_tema = f"Planificacion Anual Multigrado - EBR"
    reto_contexto = ""
    competencia = ""
    duracion = 0

else:
    # Formulario estandar para sesiones, unidades o proyectos
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
            placeholder="Ej: Indaga mediante metodos cientificos / Convive y participa democraticamente"
        )
        enfoques_transversales = st.multiselect(
            "Enfoque(s) Transversal(es) priorizado(s):",
            OPCIONES_ENFOQUES,
            default=["Ambiental", "Orientacion al bien comun"]
        )
        duracion = st.select_slider(
            "Duracion estimada (minutos):",
            options=[45, 90, 135, 180, 270],
            value=90
        )

# Disparador de accion
st.markdown("---")
texto_boton = "🚀 Generar Planificacion Anual Multigrado Completa" if es_plan_anual else "🚀 Generar Planificacion Curricular Integrada"

if st.button(texto_boton, type="primary", use_container_width=True):
    if not areas:
        st.warning("Por favor selecciona al menos una area curricular.")
    elif not grados:
        st.warning("Por favor selecciona al menos un grado o edad.")
    elif not es_plan_anual and not titulo_tema.strip():
        st.warning("Por favor ingresa un titulo o tema eje para la sesion o unidad.")
    else:
        tipos_texto = ", ".join(tipos_doc)
        niveles_texto = ", ".join(niveles)
        grados_texto = ", ".join(grados)
        areas_texto = ", ".join(areas)
        enfoques_texto = ", ".join(enfoques_transversales) if enfoques_transversales else "Orientacion al bien comun"

        if es_plan_anual:
            prompt_estructurado = f"""
            DISENA LA PLANIFICACION CURRICULAR ANUAL COMPLETA CON BASE EN LA CARTILLA OFICIAL PARA AULA MULTIGRADO:
            
            1. DATOS GENERALES:
            - Modalidad y Nivel: {niveles_texto}
            - Grados/Ciclos a cargo: {grados_texto}
            - Areas Curriculares a organizar: {areas_texto}
            - Periodo temporal: {periodos_tiempo}
            - Enfoques Transversales priorizados: {enfoques_texto}

            2. INSUMOS DE DIAGNOSTICO PROPORCIONADOS POR EL DOCENTE:
            - Calendario Comunal y Productivo: {cal_comunal if cal_comunal.strip() else 'Actividades agricolas, ganaderas y fiestas patronales tipicas de la sierra/selva rural peruana.'}
            - Problemas, Coyunturas y Potencialidades: {problemas_potencialidades if problemas_potencialidades.strip() else 'Lluvias torrenciales, saberes locales sobre conservacion y organizacion comunal.'}
            - Demandas de los Padres de Familia: {demandas_ppff if demandas_ppff.strip() else 'Aprendizajes utiles para el campo y desenvolvimiento en otros contextos.'}
            - Intereses de los Estudiantes y Clima Emocional: {intereses_estudiantes if intereses_estudiantes.strip() else 'Gusto por el juego, construccion con materiales concretos, necesidad de apoyo socioemocional.'}
            - Necesidades de Aprendizaje Diagnosticadas: {necesidades_aprendizaje if necesidades_aprendizaje.strip() else 'Niveles reales identificados segun estandares de ciclo en comprension lectora y resolucion de problemas.'}

            ESTRUCTURA DE SALIDA OBLIGATORIA (SEGUN CARTILLA):
            I. CARACTERIZACION DEL CONTEXTO SOCIOCULTURAL Y DE LOS ESTUDIANTES (Sistematizacion en tabla o resumen operativo de los insumos).
            II. IDENTIFICACION DE NECESIDADES DE APRENDIZAJE POR CICLO/GRADO (Relacionando diagnostico con los estandares de aprendizaje).
            III. ORGANIZACION SECUENCIAL Y CRONOLOGICA DE LAS UNIDADES DIDACTICAS POR PERIODOS (Bimestre o Trimestre):
                 Presentar una matriz completa con:
                 * Periodo y duracion en semanas/dias lectivos y semanas de gestion.
                 * Titulo motivador de cada Unidad/Experiencia articulada al calendario comunal.
                 * Situacion significativa contextualizada y reto.
                 * Metodologia Activa seleccionada (ABP, ABPr, ABI, Estudio de casos).
                 * Competencias priorizadas y competencias relacionadas por cada area seleccionada.
                 * Enfoques transversales movilizados.
                 * Producto integrador / Evidencia tangible esperada.
            IV. PREVISION DE TALLERES MULTINIVEL (Estrategias diferenciadas para atender a estudiantes que requieren mayor andamiaje).
            V. MATERIALES, RECURSOS EDUCATIVOS Y EVALUACION FORMATIVA ANUAL.
            """
        else:
            prompt_estructurado = f"""
            DISENA EL SIGUIENTE DOCUMENTO CURRICULAR ALINEADO AL CNEB:
            - Tipo(s) de documento: {tipos_texto}
            - Nivel(es)/Modalidad: {niveles_texto}
            - Grados/Edades: {grados_texto}
            - Area(s) articulada(s): {areas_texto}
            - Enfoque(s) transversal(es): {enfoques_texto}
            - Duracion estimada: {duracion} minutos
            - Titulo/Tema eje: {titulo_tema}
            - Situacion o reto: {reto_contexto if reto_contexto.strip() else 'Contextualizar a la realidad comunitaria peruana.'}
            - Competencias solicitadas: {competencia if competencia.strip() else 'Competencias oficiales del CNEB mas idoneas.'}

            CONDICIONES PEDAGOGICAS OBLIGATORIAS:
            1. Formular al menos UN criterio de evaluacion por CADA capacidad de cada competencia, derivado del estandar y graduado para los grados elegidos (Habilidad + Contenido + Condicion). Version en lenguaje amigable.
            2. Atencion simultanea y diferenciada en multigrado (atencion directa vs atencion indirecta/autonoma).
            3. Secuencia didactica completa con procesos didacticos del area, preguntas socraticas y Escalera de Wilson.
            4. Anexos: Matriz de evaluacion y ficha practica de aplicacion.
            """

        with st.spinner("Construyendo documento curricular de alta fidelidad pedagogica..."):
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
                st.success("¡Documento curricular generado con exito!")
                st.markdown("---")
                st.markdown(resultado)

                nombre_archivo = "Planificacion_Anual.txt" if es_plan_anual else f"Planificacion_{titulo_tema[:15].strip().replace(' ', '_')}.txt"
                st.download_button(
                    label="📥 Descargar Documento (.txt)",
                    data=resultado,
                    file_name=nombre_archivo,
                    mime="text/plain"
                )
            else:
                st.error(f"Pico de trafico momentaneo en los servidores. Por favor vuelve a hacer clic en el boton. Detalle: {detalle_error}")
