import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel

from motor import consultar_bot

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
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


@app.get("/salud")
def salud():
    return {"status": "ok"}


@app.post("/preguntar")
def preguntar(data: Consulta):
    pregunta = data.pregunta.strip()
    if not pregunta:
        return {"respuesta": "Escribe tu consulta y te ayudo.", "answer": "Escribe tu consulta y te ayudo."}
    texto = consultar_bot(pregunta)
    return {"respuesta": texto, "answer": texto}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
