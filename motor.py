import os
from langchain_community.embeddings import FastEmbedEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_openai import ChatOpenAI
from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate

OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")

# Mismo modelo que en crear_indice.py
embeddings = FastEmbedEmbeddings(
    model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
)

vectorstore = FAISS.load_local(
    "faiss_index",
    embeddings,
    allow_dangerous_deserialization=True,
)

retriever = vectorstore.as_retriever(
    search_type="mmr", search_kwargs={"k": 8, "fetch_k": 30}
)

llm = ChatOpenAI(
    model="nvidia/nemotron-3.5-lightning:free",
    openai_api_key=OPENROUTER_API_KEY,
    openai_api_base="https://openrouter.ai/api/v1",
    temperature=0.2,
    timeout=60,
    max_retries=1,
)

system_prompt = (
    "Eres el asistente virtual administrativo del IES Luis Braille "
    "(ciclo de Administración y Finanzas, modalidad virtual). "
    "Responde en español, con tono cercano y claro, como lo haría una persona de secretaría. "
    "Usa únicamente el contexto. Si piden listas (módulos, ECTS, horas, fechas), "
    "da la lista completa. Interpreta erratas en los nombres "
    "(p. ej. 'Gestión Financeira' es 'Gestión financiera'). "
    "No menciones que existe un 'contexto'. Si la información no aparece, dilo con "
    "amabilidad y sugiere consultar con el tutor o con secretaría.\n\n"
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
        print("ERROR consultar_bot:", repr(e), flush=True)
        return "Ahora mismo no puedo responder. Inténtalo de nuevo en un minuto."
