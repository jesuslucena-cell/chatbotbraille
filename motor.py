import os
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import CharacterTextSplitter

# --- CONFIGURACIÓN ---
# Pega aquí tu API KEY de Groq entre las comillas
GROQ_API_KEY = "TU_API_KEY_DE_GROQ_AQUÍ"
MODELO_IA = "llama3-8b-8192"

# --- CREAR BASE DE CONOCIMIENTO ---
print("Cargando base de conocimiento...")
texto_administrativo_prueba = """
CALENDARIO ACADÉMICO 2024:
- Inicio de clases: 10 de septiembre.
- Exámenes primer trimestre: del 15 al 20 de diciembre.
- Plazo matrícula segundo trimestre: hasta el 10 de enero.
- Tutorías: Martes de 10:00 a 12:00.
"""

text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
docs = text_splitter.create_documents([texto_administrativo_prueba])

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
vectorstore = FAISS.from_documents(docs, embeddings)
retriever = vectorstore.as_retriever()

llm = ChatGroq(temperature=0, groq_api_key=GROQ_API_KEY, model_name=MODELO_IA)
print("¡Motor del chatbot listo!")

# --- FUNCIÓN DE CONSULTA ---
def preguntar_al_chatbot(pregunta_usuario):
    # 1. Buscar los fragmentos más relevantes en la base de conocimiento
    docs_relacionados = retriever.invoke(pregunta_usuario)
    contexto = "\n\n".join([doc.page_content for doc in docs_relacionados])
    
    # 2. Enviar la pregunta y el contexto directamente a Groq
    prompt = f"""Eres un asistente administrativo. Responde de forma clara usando únicamente la siguiente información:

{contexto}

Pregunta del alumno: {pregunta_usuario}"""

    respuesta = llm.invoke(prompt)
    return respuesta.content