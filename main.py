from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
# Importamos la función que creamos en el archivo motor.py
from motor import preguntar_al_chatbot

app = FastAPI()

# Definimos cómo debe ser la pregunta que nos envían (un texto)
class PreguntaRequest(BaseModel):
    pregunta: str

@app.get("/")
def home():
    return {"mensaje": "API del Asistente Administrativo activa"}

# Esta es la dirección web real a la que llamará Moodle: TU_URL/preguntar
@app.post("/preguntar")
async def recibir_pregunta(request: PreguntaRequest):
    if not request.pregunta:
        raise HTTPException(status_code=400, detail="La pregunta no puede estar vacía")
    
    # Usamos nuestro motor Python para obtener la respuesta
    try:
        respuesta_ia = preguntar_al_chatbot(request.pregunta)
        return {"respuesta": respuesta_ia}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    # Esto es para probar en tu ordenador. Luego lo cambiaremos.
    uvicorn.run(app, host="127.0.0.1", port=8000)