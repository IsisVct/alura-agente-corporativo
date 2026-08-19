import re
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from src.agente_rag import criar_cadeia_rag
import os

app = FastAPI(title="De Souza Bank - Agente Corporativo")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

agente = criar_cadeia_rag()

class RequisicaoPergunta(BaseModel):
    pergunta: str

@app.post("/api/perguntar")
def endpoint_perguntar(req: RequisicaoPergunta):
    try:
        resposta = agente.invoke(req.pergunta)
        
        resposta_limpa = re.sub(r'<think>.*?</think>\n?', '', resposta, flags=re.DOTALL).strip()
        
        return {"resposta": resposta_limpa}
    except Exception as e:
        return {"resposta": f"Erro interno ao processar a requisição: {str(e)}"}


caminho_dist = os.path.join(os.path.dirname(__file__), "../frontend/dist")

if os.path.exists(caminho_dist):
    app.mount("/assets", StaticFiles(directory=os.path.join(caminho_dist, "assets")), name="assets")

    @app.get("/{full_path:path}")
    def serve_react(full_path: str):
        arquivo_alvo = os.path.join(caminho_dist, full_path)
        if os.path.exists(arquivo_alvo) and os.path.isfile(arquivo_alvo):
            return FileResponse(arquivo_alvo)
        return FileResponse(os.path.join(caminho_dist, "index.html"))