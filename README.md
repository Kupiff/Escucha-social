# 📡 Agente de Escucha Social con IA (Social Listening AI)

> Sistema de agentes autónomos desarrollado con **CrewAI**, **Google Gemini** y **Streamlit** para analizar marcas, productos o tendencias en tiempo real y optimizar la estrategia de distribución en redes sociales (LinkedIn, X, Reddit).

🌐 **Aplicación en vivo:** [Probar en Streamlit Cloud](https://escucha-social.streamlit.app/)  
👨‍💻 **Creado por:** [rkweb.es](https://rkweb.es)

---

## 🚀 Características Principales

- **🔑 Interfaz Dinámica para API Keys:** Los usuarios introducen su propia clave de API de Google Gemini de forma segura desde la interfaz.
- **🎯 Enfoque de Análisis Personalizable:** Permite seleccionar la perspectiva del estudio (Reputación de marca, Marketing, Experiencia de usuario, Innovación o Gestión de crisis).
- **🧩 Módulos Modulares Seleccionables:** Activa o desactiva según tus necesidades:
  - 🔍 Monitoreo y Rastreo Web
  - 📊 Análisis de Sentimiento y Reputación
  - 💬 Estrategia y Plantillas de Respuesta
  - 📋 Resumen Ejecutivo
- **🤖 Multi-Agente con CrewAI:** Dos agentes especializados trabajan en equipo de forma secuencial (Investigador web y Analista estratégico).

---

## 🛠️ Tecnologías Utilizadas

- **Python 3.10+**
- **Streamlit** (Interfaz de usuario web)
- **CrewAI & CrewAI Tools** (Orquestación de agentes autónomos)
- **Google GenAI / Google Gemini** (Modelos LLM avanzados)
- **LangChain Community & DuckDuckGo** (Herramientas de búsqueda y rastreo en tiempo real)

---

## ⚙️ Instalación y Ejecución Local

Si deseas clonar y ejecutar este proyecto en tu entorno local:

1. **Clona el repositorio:**

   git clone https://github.com/kupiff/escucha-social.git
   cd escucha-social

3. Crea un entorno virtual e instálalo:

    python -m venv venv
    source venv/bin/activate  # En Windows: venv\Scripts\activate
    pip install -r requirements.txt
   
4. Ejecuta la aplicación de Streamlit:

    streamlit run app.py


Dependencias (requirements.txt)

Asegúrate de que tu archivo requirements.txt contenga lo siguiente para evitar errores de despliegue en la nube:

streamlit
crewai
crewai-tools
google-genai
langchain-community
duckduckgo-search

Automatización Keep-Alive (GitHub Actions)

Para evitar que Streamlit Cloud ponga a dormir la aplicación por inactividad, este repositorio incluye un flujo de trabajo en .github/workflows/keep-alive.yml que realiza pings periódicos automáticos.
Conecta conmigo

    Web personal: https://rkweb.es
    LinkedIn: https://www.linkedin.com/in/francisco-cupini-75637983/
