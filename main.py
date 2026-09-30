from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from motor import consultar_bot

app = FastAPI(title="Chatbot Administrativo")

class Consulta(BaseModel):
    pregunta: str

@app.post("/preguntar")
def preguntar(consulta: Consulta):
    respuesta = consultar_bot(consulta.pregunta)
    return {"respuesta": respuesta}

@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Asistente Virtual</title>
        <style>
            body { font-family: Arial, sans-serif; background-color: #f4f6f9; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
            .chat-card { width: 100%; max-width: 500px; height: 80vh; background: white; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.1); display: flex; flex-direction: column; overflow: hidden; }
            .chat-header { background: #0056b3; color: white; padding: 15px; font-size: 18px; font-weight: bold; text-align: center; }
            .chat-logs { flex: 1; padding: 15px; overflow-y: auto; display: flex; flex-direction: column; gap: 10px; }
            .msg { padding: 10px 14px; border-radius: 10px; max-width: 80%; line-height: 1.4; font-size: 15px; }
            .bot { background: #e9ecef; color: #333; align-self: flex-start; }
            .user { background: #0056b3; color: white; align-self: flex-end; }
            .chat-input-area { display: flex; padding: 10px; border-top: 1px solid #e0e0e0; background: #fafafa; }
            input { flex: 1; border: 1px solid #ccc; border-radius: 6px; padding: 10px; font-size: 15px; outline: none; }
            button { background: #0056b3; color: white; border: none; padding: 10px 16px; margin-left: 8px; border-radius: 6px; cursor: pointer; font-weight: bold; }
            button:hover { background: #004085; }
        </style>
    </head>
    <body>
        <div class="chat-card">
            <div class="chat-header">🤖 Asistente Virtual Administrativo</div>
            <div class="chat-logs" id="logs">
                <div class="msg bot">¡Hola! 👋 ¿En qué puedo ayudarte hoy con tus consultas o trámites?</div>
            </div>
            <div class="chat-input-area">
                <input type="text" id="userInput" placeholder="Escribe tu consulta aquí..." onkeypress="if(event.key==='Enter') enviar()">
                <button onclick="enviar()">Enviar</button>
            </div>
        </div>

        <script>
            async function enviar() {
                const input = document.getElementById('userInput');
                const logs = document.getElementById('logs');
                const text = input.value.trim();
                if(!text) return;

                // Mensaje usuario
                const userDiv = document.createElement('div');
                userDiv.className = 'msg user';
                userDiv.textContent = text;
                logs.appendChild(userDiv);
                input.value = '';
                logs.scrollTop = logs.scrollHeight;

                // Indicador de respuesta
                const botDiv = document.createElement('div');
                botDiv.className = 'msg bot';
                botDiv.textContent = 'Escribiendo respuesta...';
                logs.appendChild(botDiv);
                logs.scrollTop = logs.scrollHeight;

                try {
                    const res = await fetch('/preguntar', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({pregunta: text})
                    });
                    const data = await res.json();
                    botDiv.textContent = data.respuesta || 'No he obtenido respuesta.';
                } catch(e) {
                    botDiv.textContent = 'Error al conectar con el asistente.';
                }
                logs.scrollTop = logs.scrollHeight;
            }
        </script>
    </body>
    </html>
    """
