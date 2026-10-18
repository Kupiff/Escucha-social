import os
import streamlit as st
from crewai import Agent, Crew, Process, Task, LLM
from langchain_community.tools import DuckDuckGoSearchRun

st.set_page_config(page_title="Escucha Social AI", page_icon="📡", layout="wide")

st.title("📡 Sistema de Agentes de IA - Escucha Social")
st.markdown("Analiza marcas, tendencias u opiniones en tiempo real utilizando agentes autónomos con **CrewAI** y **Google Gemini**.")

col1, col2 = st.columns([1, 1])

with col1:
    gemini_api_key = st.text_input(
        "Llave de API de Google Gemini", 
        type="password", 
        help="Introduce tu clave personal de Google AI Studio"
    )
    tema_busqueda = st.text_area(
        "Tema, Marca o Producto a Analizar", 
        placeholder="Ejemplo: Tesla Cybercab, Inteligencia Artificial en Educación..."
    )
    btn_analizar = st.button("🚀 Iniciar Escucha Social", type="primary")

with col2:
    st.subheader("Reporte Final de Análisis")
    output_container = st.empty()
    output_container.info("El informe generado por el equipo de agentes aparecerá aquí...")

if btn_analizar:
    if not gemini_api_key.strip():
        st.error("⚠️ Por favor, introduce tu API Key de Google Gemini.")
    elif not tema_busqueda.strip():
        st.error("⚠️ Por favor, introduce un tema o marca para analizar.")
    else:
        os.environ["GEMINI_API_KEY"] = gemini_api_key.strip()
        
        with st.spinner("🤖 Los agentes están investigando y analizando la web..."):
            try:
                search_tool = DuckDuckGoSearchRun()
                llm = LLM(
                    model="gemini/gemini-1.5-flash",
                    api_key=gemini_api_key.strip()
                )

                investigador = Agent(
                    role="Investigador de Escucha Social",
                    goal=f"Buscar opiniones, conversaciones y tendencias recientes sobre: {tema_busqueda}",
                    backstory="Analista experto en datos web y redes sociales.",
                    tools=[search_tool],
                    llm=llm,
                    verbose=True
                )

                analista = Agent(
                    role="Analista Estratégico de Marcas",
                    goal="Sintetizar la información recolectada y generar un informe completo",
                    backstory="Especialista en inteligencia de mercado y reputación online.",
                    llm=llm,
                    verbose=True
                )

                tarea_investigacion = Task(
                    description=f"Realiza una búsqueda profunda sobre '{tema_busqueda}'. Recopila opiniones y noticias recientes.",
                    expected_output="Resumen detallado con los hallazgos principales.",
                    agent=investigador
                )

                tarea_analisis = Task(
                    description=f"Analiza los resultados obtenidos sobre '{tema_busqueda}'. Clasifica el sentimiento general e identifica tendencias.",
                    expected_output="Informe estructurado en Markdown con Resumen, Sentimiento, Tendencias y Recomendaciones.",
                    agent=analista
                )

                equipo = Crew(
                    agents=[investigador, analista],
                    tasks=[tarea_investigacion, tarea_analisis],
                    process=Process.sequential
                )

                resultado = equipo.kickoff()
                output_container.markdown(str(resultado))
                st.success("¡Análisis completado!")
                
            except Exception as e:
                st.error(f"❌ Ocurrió un error: {str(e)}")
