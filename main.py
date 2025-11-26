from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles   # ← ADICIONE ESTA LINHA

app = FastAPI(title="AOVB Real Estate API", version="1.0.0")

# ← ADICIONE ESTE BLOCO LOGO DEPOIS DA CRIAÇÃO DO APP
app.mount("/.well-known", StaticFiles(directory=".well-known"), name="well-known")

class MatriculaInput(BaseModel):
    texto_matricula: str

@app.get("/")
def home():
    return {"message": "AOVB Real Estate Connect API - Online"}

@app.post("/interpreta_matricula")
def interpreta_matricula(data: MatriculaInput):
    texto = data.texto_matricula.lower()
    resposta = {
        "matricula": texto,
        "titular": "João da Silva" if "joão" in texto else "Titular não identificado",
        "uf": "SP" if "são paulo" in texto or "sp" in texto else "UF desconhecida",
        "riscos": []
    }

    if "hipoteca" in texto:
        resposta["riscos"].append("Hipoteca encontrada - verificar quitação")

    if "averbação" not in texto:
        resposta["riscos"].append("Sem averbações recentes")

    return resposta
