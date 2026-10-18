import os
import streamlit as st
from crewai import Agent, Crew, Process, Task, LLM
from crewai.tools import tool
from langchain_community.tools import DuckDuckGoSearchRun

# Definimos la herramienta de búsqueda de forma nativa e inmune a errores
@tool("Buscador DuckDuckGo")
def buscar_en_web(query: str) -> str:
    """Busca en la web usando DuckDuckGo para obtener información actualizada, opiniones y noticias."""
    search = DuckDuckGoSearchRun()
    return search.run(query)

# Configuración de la página en Streamlit
st.set_page_config(
    page_title="Agente de Escucha Social AI",
    page_icon="📡",
    layout="wide"
)

st.title("📡 Sistema de Agentes de IA - Escucha Social")
st.markdown(
    """
    Analiza marcas, tendencias u opiniones en tiempo real utilizando agentes autónomos con **CrewAI** y **Google Gemini**.
    """
)

# Diseño en dos columnas
col1, col2 = st.columns([1, 1])

with col1:
    gemini_api_key = st.text_input(
        "Llave de API de Google Gemini (API Key)",
        type="password",
        placeholder="AIzaSy...",
        help="Introduce tu clave de API personal de Google AI Studio."
    )
    
    # Enlace de ayuda para obtener la API Key
    st.markdown(
        "🔑 **¿No tienes una API Key?** Consíguela de forma rápida y gratuita en "
        "[Google AI Studio](https://aistudio.google.com/app/apikey)."
    )
    
    st.divider()

    tema_busqueda = st.text_area(
        "Tema, Marca o Producto a Analizar",
        placeholder="Ejemplo: Tesla Cybercab, Lanzamiento iPhone 16, Inteligencia Artificial en Educación...",
        height=100
    )

    # Selector de Enfoque del Análisis
    enfoque_analisis = st.selectbox(
        "Enfoque del Análisis",
        options=[
            "General / Reputación de Marca",
            "Marketing y Estrategia Comercial",
            "Sentimiento de Clientes y Experiencia de Usuario",
            "Innovación Tecnológica y Producto",
            "Gestión de Crisis / Puntos Críticos"
        ],
        index=0,
        help="Selecciona la perspectiva principal desde la que los agentes analizarán la información."
    )
    
    btn_ejecutar = st.button("🚀 Iniciar Escucha Social", type="primary", use_container_width=True)

with col2:
    st.subheader("Reporte Final de Análisis")
    output_container = st.empty()
    output_container.info("*El informe generado por el equipo de agentes aparecerá aquí...*")

if btn_ejecutar:
    if not gemini_api_key or not gemini_api_key.strip():
        st.error("⚠️ Error: Por favor, introduce tu API Key de Google Gemini.")
    elif not tema_busqueda or not tema_busqueda.strip():
        st.error("⚠️ Error: Por favor, introduce un tema o marca para analizar.")
    else:
        # Configurar la variable de entorno para Gemini
        os.environ["GEMINI_API_KEY"] = gemini_api_key.strip()
        
        with st.spinner("🤖 Los agentes están investigando en la web y generando el análisis... esto tomará unos segundos."):
            try:
                # Configuración estándar del LLM compatible con CrewAI y Google GenAI
                llm = LLM(
                    model="gemini/gemini-2.0-flash",
                    api_key=gemini_api_key.strip()
                )

                # 1. Agente Investigador / Scraper
                investigador = Agent(
                    role="Investigador de Escucha Social",
                    goal=f"Buscar opiniones, conversaciones y tendencias recientes sobre '{tema_busqueda}', priorizando la perspectiva de '{enfoque_analisis}'.",
                    backstory="Eres un analista experto en datos web y redes sociales. Tu trabajo es encontrar información relevante y reciente sobre marcas, productos o temas específicos.",
                    tools=[buscar_en_web],
                    llm=llm,
                    verbose=True,
                    allow_delegation=False
                )

                # 2. Agente Analista de Sentimiento y Tendencias
                analista = Agent(
                    role="Analista Estratégico de Marcas",
                    goal=f"Sintetizar la información recolectada y generar un informe de escucha social enfocado en '{enfoque_analisis}'.",
                    backstory="Especialista en inteligencia de mercado y reputación online. Transformas datos dispersos de la web en insights accionables, análisis de sentimiento y recomendaciones estratégicas.",
                    llm=llm,
                    verbose=True,
                    allow_delegation=False
                )

                # Tarea 1: Búsqueda de información
                tarea_investigacion = Task(
                    description=f"Realiza una búsqueda profunda en la web sobre '{tema_busqueda}'. Recopila opiniones, menciones clave y noticias recientes, prestando especial atención a elementos relacionados con: {enfoque_analisis}.",
                    expected_output="Un resumen detallado con los hallazgos principales, datos clave y citas relevantes encontradas en la web.",
                    agent=investigador
                )

                # Tarea 2: Análisis y reporte
                tarea_analisis = Task(
                    description=f"Analiza los resultados obtenidos sobre '{tema_busqueda}' desde el enfoque de '{enfoque_analisis}'. Clasifica el sentimiento general (Positivo, Neutro, Negativo), identifica temas recurrentes y ofrece recomendaciones estratégicas directamente orientadas a este enfoque.",
                    expected_output=f"Un informe estructurado en formato Markdown con: 1. Resumen Ejecutivo (Perspectiva: {enfoque_analisis}), 2. Análisis de Sentimiento, 3. Temas Clave / Tendencias, 4. Recomendaciones Estratégicas Específicas.",
                    agent=analista
                )

                # Crear y ejecutar la Crew
                equipo = Crew(
                    agents=[investigador, analista],
                    tasks=[tarea_investigacion, tarea_analisis],
                    process=Process.sequential,
                    verbose=True
                )

                resultado = equipo.kickoff()
                
                # Mostrar el resultado final en la interfaz
                output_container.markdown(str(resultado))
                st.success("¡Análisis completado con éxito!")

            except Exception as e:
                st.error(f"❌ Ocurrió un error durante la ejecución: {str(e)}")
