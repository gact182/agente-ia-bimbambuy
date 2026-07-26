# 🤖 Agente de IA para Soporte y Políticas (BimBam Buy)

Aplicación web interactiva desarrollada con **Streamlit**, **LangChain** y **Google Gemini** para actuar como un asistente de soporte interno capaz de consultar y responder dudas basadas en los manuales en PDF de la empresa BimBam Buy (garantías, envíos, pagos, afiliados y devoluciones).

---

## 🛠️ Arquitectura y Tecnologías
El proyecto utiliza un flujo de recuperación de información aumentada (**RAG** - *Retrieval-Augmented Generation*):
* **Interfaz de Usuario:** Streamlit
* **Orquestador de LLM / Cadenas:** LangChain
* **Carga de Documentos:** PyPDFDirectoryLoader (procesa los manuales internos en PDF de la carpeta `data/`)
* **Segmentación de Texto:** RecursiveCharacterTextSplitter (divide el texto en fragmentos óptimos de 1000 caracteres)
* **Base de Datos Vectorial:** FAISS (almacena y busca los fragmentos de texto relevantes localmente)
* **Modelos de IA:** Google GenAI (Gemini) para la generación de respuestas contextuales.

---

## 💬 Ejemplos de Preguntas y Respuestas

* **Pregunta:** ¿Cuál es la política de devoluciones?
* **Respuesta generada por el agente:** Según el manual interno de BimBam Buy, cuentas con hasta 30 días calendario a partir de la fecha de entrega para solicitar una devolución, siempre y cuando el producto se encuentre en su empaque original y sin uso.
  
---

## 📂 Estructura del Proyecto
```text
agente-ia-bimbambuy/
│
├── .env                  # Variables de entorno (API Key de Google - No se sube a GitHub)
├── .gitignore            # Archivos excluidos del control de versiones
├── app.py                # Código principal de la aplicación Streamlit
├── requirements.txt      # Dependencias del proyecto Python
└── data/                 # Carpeta contenedora de los manuales en PDF
    ├── Guía de Tiempos ...pdf
    ├── Manual de Garant...pdf
    ├── Política de Reemb...pdf
    ├── Preguntas_Frecu...pdf
    └── Programa de Afili...pdf

---

