import os
import streamlit as st
from google import genai

st.set_page_config(page_title="Asistente Pedagógico CNEB", page_icon="📚", layout="centered")

st.title("📚 Asistente Curricular CNEB")
st.caption("Planificación curricular y evaluación formativa alineada a la EBR")

# Instrucciones confidenciales protegidas en el servidor
SYSTEM_INSTRUCTIONS = """
ROL Y PROPÓSITO:
Eres DocentIA CNEB, especialista en Planificación Curricular y Evaluación Formativa para EBR en Perú.
Diseñas sesiones y unidades de aprendizaje alineadas al CNEB (RM N.° 281-2016-MINEDU) y RVM N.° 094-2020-MINEDU.

REGLAS DE ORO:
1. Formular al menos UN criterio de evaluación por CADA capacidad de la competencia seleccionada.
2. Estructura del criterio: Habilidad (acción observable) + Contenido + Condición de calidad/contexto.
3. Secuencia didáctica completa: Inicio (problematización, saberes previos), Desarrollo (procesos didácticos del área, mediación y retroalimentación con Escalera de Wilson) y Cierre (metacognición).
"""

# Obtener la API Key desde los secretos configurados en Streamlit
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

consulta = st.text_area(
    "Ingresa el requerimiento pedagógico:",
    placeholder="Ej: Diseña una sesión de aprendizaje para 5° grado de primaria en el área de Ciencia y Tecnología...",
    height=120
)

if st.button("Generar Planificación", type="primary"):
    if not consulta.strip():
        st.warning("Por favor, ingresa los datos de la sesión.")
    else:
        with st.spinner("Elaborando planificación curricular..."):
            try:
                response = client.models.generate_content(
                    # Reemplázala por:
model="gemini-3.8-flash",
                    contents=consulta,
                    config=genai.types.GenerateContentConfig(
                        system_instruction=SYSTEM_INSTRUCTIONS,
                        temperature=0.3
                    )
                )
                st.markdown("---")
                st.markdown(response.text)
            except Exception as e:
                st.error(f"Error al conectar con el servicio: {e}")
