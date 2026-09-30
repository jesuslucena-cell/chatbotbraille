import os
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_groq import ChatGroq
from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate

# Configurar API Key de Groq
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

# 1. Cargar Embeddings ligeros
embeddings = HuggingFaceEmbeddings(
    model_name="all-MiniLM-L6-v2",
    model_kwargs={'device': 'cpu'},
    encode_kwargs={'normalize_embeddings': True}
)

# 2. Cargar índice FAISS precalculado
vectorstore = FAISS.load_local(
    "faiss_index", 
    embeddings, 
    allow_dangerous_deserialization=True
)

retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

# 3. Configurar modelo LLM con Groq
llm = ChatGroq(
    temperature=0.2,
    model_name="llama-3.1-8b-instant",
    groq_api_key=GROQ_API_KEY
)

# 4. Prompt del sistema
system_prompt = (
    "Eres un asistente administrativo educativo amigable e informativo para EducaMadrid.\n"
    "Responde a la pregunta del usuario utilizando únicamente el contexto proporcionado a continuación.\n"
    "Si la respuesta no se encuentra en el contexto, di amablemente que no dispones de esa información.\n\n"
    "Contexto:\n{context}"
)

prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("human", "{input}"),
])

question_answer_chain = create_stuff_documents_chain(llm, prompt)
rag_chain = create_retrieval_chain(retriever, question_answer_chain)

def consultar_bot(pregunta: str) -> str:
    try:
        response = rag_chain.invoke({"input": pregunta})
        return response["answer"]
    except Exception as e:
        return f"Error al procesar la consulta: {str(e)}"
