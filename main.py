from fastapi import FastAPI
from fastapi.exceptions import HTTPException
from pydantic import BaseModel

from app.aux import busca_primeira_instancia, valida_numero_processo

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

    tribunais = {
    '02': {'uf': 'AL', 'base_url': 'https://www2.tjal.jus.br'},
    '06': {'uf': 'CE', 'base_url': 'https://esaj.tjce.jus.br'}
    }

    digito_tribunal = numero_processo.numero_processo[18:20]
    tribunal = tribunais[digito_tribunal]
    
    resultado = busca_primeira_instancia(numero_processo.numero_processo,tribunal)

    return resultado