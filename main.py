from fastapi import FastAPI
from fastapi.exceptions import HTTPException
from pydantic import BaseModel

from app.aux import valida_numero_processo

class LawsuitNumber(BaseModel):
    numero_processo: str 

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Bem vindo ao robo crawler do ESAJ Alagoas e Ceara! Use o metodo POST para buscar usando o numero do processo"}

@app.post("/")
def search_lawsuit(numero_processo: LawsuitNumber):

    if not valida_numero_processo(numero_processo.numero_processo):
        raise HTTPException(status_code=400, detail="Número do processo inválido")

    return numero_processo