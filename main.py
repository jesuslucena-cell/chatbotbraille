import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import uvicorn

from motor import consultar_bot

app = FastAPI(
    title="Chatbot EducaMadrid",
    description="API Backend para el bot de consulta educativa",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Consulta(BaseModel):
    pregunta: str

# Montar carpeta de archivos estáticos si existe
if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

# Servir el HTML del chat al entrar a la URL raíz
@app.get("/")
def home():
    if os.path.exists("static/index.html"):
        return FileResponse("static/index.html")
    elif os.path.exists("index.html"):
        return FileResponse("index.html")
    return {"status": "ok", "mensaje": "Servidor activo. Coloca tu index.html para ver la interfaz."}

@app.post("/preguntar")
def preguntar(data: Consulta):
    texto_respuesta = consultar_bot(data.pregunta)
    return {
        "respuesta": texto_respuesta,
        "answer": texto_respuesta
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=10000, reload=True)
