import os
import streamlit as st
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_text_splitters import RecursiveCharacterTextSplitter

current_dir = os.path.dirname(os.path.abspath(__file__))
dotenv_path = os.path.join(current_dir, '.env')
load_dotenv(dotenv_path=dotenv_path)

st.set_page_config(page_title="Agente de IA - BimBam Buy", page_icon="🤖")

st.title("🤖 Agente de IA para Soporte y Políticas (BimBam Buy)")
st.write("Consulta los manuales internos de garantías, envíos, pagos, afiliados y devoluciones.")

PDF_DIR = os.path.join(current_dir, "data")

@st.cache_resource
def initialize_vector_store():
    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if not api_key:
        return None
        
    if not os.path.exists(PDF_DIR):
        os.makedirs(PDF_DIR)
        
    loader = PyPDFDirectoryLoader(PDF_DIR)
    docs = loader.load()
    
    if not docs:
        return None

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(docs)

    # Usar embeddings locales con HuggingFace para evitar errores de API
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vectorstore = FAISS.from_documents(splits, embeddings)
    return vectorstore.as_retriever(search_kwargs={"k": 3})

retriever = initialize_vector_store()

api_key_check = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")

if not api_key_check:
    st.error("⚠️ No se encontró la GEMINI_API_KEY en el archivo .env.")
elif retriever is None:
    st.warning(f"⚠️ No se pudieron leer los PDFs en la carpeta 'data'.")
else:
    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.2, google_api_key=api_key_check)
    




    query = st.text_input("¿Qué deseas consultar sobre las políticas de BimBam Buy?")

    if query:
        with st.spinner("Analizando la documentación interna..."):
            relevant_docs = retriever.invoke(query)
            context = "\n\n".join([doc.page_content for doc in relevant_docs])
            
            prompt = f"""Responde a la siguiente pregunta basándote únicamente en el contexto provisto:
            
            Contexto:
            {context}
            
            Pregunta: {query}"""
            
            response = llm.invoke(prompt)
            st.markdown("### Respuesta:")
            st.write(response.content)