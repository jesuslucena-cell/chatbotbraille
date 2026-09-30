import os
from langchain_community.embeddings import FastEmbedEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_openai import ChatOpenAI
from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate

# Obtener clave API de OpenRouter desde Render
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")

# 1. Embeddings ligeros
embeddings = FastEmbedEmbeddings(
    model_name="BAAI/bge-small-en-v1.5"
)

# 2. Cargar FAISS
vectorstore = FAISS.load_local(
    "faiss_index", 
    embeddings, 
    allow_dangerous_deserialization=True
)

retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

# 3. LLM Gratuito activo en OpenRouter (NVIDIA Nemotron 3.5 Lightning)
llm = ChatOpenAI(
    model="nvidia/nemotron-3.5-lightning:free",
    openai_api_key=OPENROUTER_API_KEY,
    openai_api_base="https://openrouter.ai/api/v1",
    temperature=0.2
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
