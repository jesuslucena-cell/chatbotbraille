from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

# Importar la función desde motor.py
from motor import consultar_bot

app = FastAPI(
    title="Chatbot EducaMadrid",
    description="API Backend para el bot de consulta educativa",
    version="1.0.0"
)

# Configurar CORS para permitir peticiones desde la interfaz web sin bloqueos
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Definir la estructura de la consulta recibida
class Consulta(BaseModel):
    pregunta: str

# Ruta de prueba de estado
@app.get("/")
def home():
    return {"status": "ok", "mensaje": "Servidor del Chatbot EducaMadrid funcionando correctamente."}

# Ruta principal del Chatbot
# NOTA: Se usa 'def' (síncrono) para ejecutar LangChain en un hilo secundario sin congelar FastAPI
@app.post("/preguntar")
def preguntar(data: Consulta):
    texto_respuesta = consultar_bot(data.pregunta)
    
    # Devuelve tanto 'respuesta' como 'answer' para garantizar compatibilidad con el JS del frontend
    return {
        "respuesta": texto_respuesta,
        "answer": texto_respuesta
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=10000, reload=True)
