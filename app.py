import os
import streamlit as st
from crewai import Agent, Crew, Process, Task, LLM
from crewai.tools import tool
from langchain_community.tools import DuckDuckGoSearchRun

# Buscador web nativo envuelto como herramienta de CrewAI
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
        height=90
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

    st.subheader("🧩 Módulos a Ejecutar")
    
    col_mod1, col_mod2 = st.columns(2)
    with col_mod1:
        mod_monitoreo = st.checkbox("🔍 Monitoreo y Rastreo Web", value=True)
        mod_sentimiento = st.checkbox("📊 Análisis de Sentimiento y Reputación", value=True)
    with col_mod2:
        mod_estrategia = st.checkbox("💬 Estrategia y Plantillas de Respuesta", value=True)
        mod_resumen = st.checkbox("📋 Resumen Ejecutivo", value=True)

    btn_ejecutar = st.button("🚀 Iniciar Escucha Social", type="primary", use_container_width=True)

with col2:
    st.subheader("Reporte Final de Análisis")
    output_container = st.empty()
    output_container.info("*El informe generado por el equipo de agentes aparecerá aquí...*")

if btn_ejecutar:
    modulos_seleccionados = []
    if mod_monitoreo: modulos_seleccionados.append("Monitoreo y Rastreo Web")
    if mod_sentimiento: modulos_seleccionados.append("Análisis de Sentimiento y Reputación")
    if mod_estrategia: modulos_seleccionados.append("Estrategia y Plantillas de Respuesta")
    if mod_resumen: modulos_seleccionados.append("Resumen Ejecutivo")

    if not gemini_api_key or not gemini_api_key.strip():
        st.error("⚠️ Error: Por favor, introduce tu API Key de Google Gemini.")
    elif not tema_busqueda or not tema_busqueda.strip():
        st.error("⚠️ Error: Por favor, introduce un tema o marca para analizar.")
    elif not modulos_seleccionados:
        st.error("⚠️ Error: Por favor, selecciona al menos un módulo a ejecutar.")
    else:
        # Configurar la variable de entorno para Gemini
        os.environ["GEMINI_API_KEY"] = gemini_api_key.strip()
        
        with st.spinner("🤖 Los agentes están procesando los módulos seleccionados... esto tomará unos segundos."):
            try:
                # Configuración del modelo por defecto
                llm = LLM(
                    model="gemini/gemini-3.8-flash",
                    api_key=gemini_api_key.strip()
                )

                # Definición de Agentes
                investigador = Agent(
                    role="Investigador de Escucha Social",
                    goal=f"Rastrear la web y recopilar menciones, opiniones y tendencias sobre '{tema_busqueda}' enfocado en '{enfoque_analisis}'.",
                    backstory="Especialista en rastreo de medios digitales, redes sociales y foros comunitarios.",
                    tools=[buscar_en_web],
                    llm=llm,
                    verbose=True,
                    allow_delegation=False
                )

                analista = Agent(
                    role="Analista Estratégico y de Reputación",
                    goal=f"Procesar los hallazgos sobre '{tema_busqueda}' y generar informes detallados para los módulos seleccionados.",
                    backstory="Especialista en inteligencia de mercados, métricas de sentimiento, comunicación de crisis y síntesis ejecutiva.",
                    llm=llm,
                    verbose=True,
                    allow_delegation=False
                )

                # Construcción dinámica de Tareas según los módulos activados
                tareas = []

                # Tarea base de Búsqueda (siempre necesaria si hay módulos activos)
                tarea_investigacion = Task(
                    description=f"Realiza búsquedas web sobre '{tema_busqueda}'. Extrae noticias recientes, opiniones de usuarios y debates clave bajo el enfoque de '{enfoque_analisis}'.",
                    expected_output="Recopilación estructurada con hallazgos clave, fuentes y citas de usuarios/medios.",
                    agent=investigador
                )
                tareas.append(tarea_investigacion)

                instrucciones_reporte = []
                if mod_monitoreo:
                    instrucciones_reporte.append("1. **🔍 Monitoreo y Rastreo Web**: Detalla las principales conversaciones, fuentes consultadas y volumen estimado de menciones.")
                if mod_sentimiento:
                    instrucciones_reporte.append("2. **📊 Análisis de Sentimiento y Reputación**: Clasifica el tono general (Positivo, Neutro, Negativo) identificando los principales impulsores o detracciones de la marca.")
                if mod_estrategia:
                    instrucciones_reporte.append("3. **💬 Estrategia y Plantillas de Respuesta**: Proporciona recomendaciones tácticas de acción y al menos 2 plantillas de respuesta recomendadas ante comentarios críticos o frecuentes.")
                if mod_resumen:
                    instrucciones_reporte.append("4. **📋 Resumen Ejecutivo**: Sintetiza en un párrafo de alto nivel las conclusiones clave para la toma de decisiones rápidas.")

                guion_reporte = "\n".join(instrucciones_reporte)

                tarea_analisis = Task(
                    description=f"Con la información recopilada sobre '{tema_busqueda}', genera un informe estructurado que incluya ÚNICAMENTE las siguientes secciones solicitadas por el usuario:\n{guion_reporte}",
                    expected_output="Informe final en Markdown que contenga exactamente las secciones solicitadas con alta calidad de detalle.",
                    agent=analista
                )
                tareas.append(tarea_analisis)

                # Ejecutar CrewAI
                equipo = Crew(
                    agents=[investigador, analista],
                    tasks=tareas,
                    process=Process.sequential,
                    verbose=True
                )

                resultado = equipo.kickoff()
                
                # Mostrar resultado final en pantalla
                output_container.markdown(str(resultado))
                st.success("¡Análisis completado con éxito!")

            except Exception as e:
                st.error(f"❌ Ocurrió un error durante la ejecución: {str(e)}")
