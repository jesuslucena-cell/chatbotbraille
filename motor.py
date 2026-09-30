import os
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# 1. Cargar embeddings ligeros para CPU
embeddings = HuggingFaceEmbeddings(
    model_name="all-MiniLM-L6-v2",
    model_kwargs={'device': 'cpu'}
)

# 2. Cargar índice FAISS
INDEX_PATH = "faiss_index"

if os.path.exists(INDEX_PATH):
    vectorstore = FAISS.load_local(
        INDEX_PATH, 
        embeddings, 
        allow_dangerous_deserialization=True
    )
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
else:
    retriever = None

# 3. Configurar modelo LLM con Groq
llm = ChatGroq(
    temperature=0,
    model_name="llama3-8b-8192",
    groq_api_key=os.getenv("GROQ_API_KEY")
)

# 4. Plantilla de prompt
template = """Responde a la pregunta basada únicamente en el siguiente contexto administrativo:

Contexto:
{context}

Pregunta: {question}

Respuesta clara y directa:"""

prompt = ChatPromptTemplate.from_template(template)

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

def consultar_bot(pregunta: str) -> str:
    if not retriever:
        return "El sistema aún no tiene cargada la base de datos de documentos."
    
    chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    
    return chain.invoke(pregunta)
