from fastapi import FastAPI
from pydantic import BaseModel
from motor import consultar_bot

app = FastAPI(
    title="Chatbot Administrativo",
    description="API RAG para consultas administrativas de EducaMadrid"
)

class Consulta(BaseModel):
    pregunta: str

@app.get("/")
def home():
    return {"status": "API activa. Ve a /docs para la interfaz interactiva."}

@app.post("/preguntar")
def preguntar(consulta: Consulta):
    respuesta = consultar_bot(consulta.pregunta)
    return {"respuesta": respuesta}
