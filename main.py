from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
import os
import uvicorn

from motor import consultar_bot

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Consulta(BaseModel):
    pregunta: str

@app.get("/")
def home():
    if os.path.exists("index.html"):
        return FileResponse("index.html")
    return {"status": "ok", "mensaje": "Coloca tu index.html en la raíz del proyecto."}

@app.post("/preguntar")
def preguntar(data: Consulta):
    texto_respuesta = consultar_bot(data.pregunta)
    return {
        "respuesta": texto_respuesta,
        "answer": texto_respuesta
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=10000, reload=True)
