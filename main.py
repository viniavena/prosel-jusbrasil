from fastapi import FastAPI
from fastapi.exceptions import HTTPException
from pydantic import BaseModel
import asyncio


from src.app.aux import busca_primeira_instancia, busca_segunda_instancia, valida_numero_processo
from src.app.db_services import buscar_tribunal_por_id, listar_tribunais

class LawsuitNumber(BaseModel):
    numero_processo: str 

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Bem vindo ao robo crawler do ESAJ Alagoas e Ceara! Use o metodo POST para buscar usando o numero do processo"}


@app.post("/")
async def search_lawsuit(load: LawsuitNumber):

    if not valida_numero_processo(load.numero_processo):
        raise HTTPException(status_code=400, detail="Número do processo inválido")

    # tribunais = {
    # '02': {'uf': 'AL', 'base_url': 'https://www2.tjal.jus.br'},
    # '06': {'uf': 'CE', 'base_url': 'https://esaj.tjce.jus.br'}
    # }

    digito_tribunal = load.numero_processo[18:20]

    objeto_tribunal = buscar_tribunal_por_id(digito_tribunal)
    if objeto_tribunal:
        tribunal = objeto_tribunal.__dict__
    else:
        raise HTTPException(status_code=404, detail="Tribunal não encontrado")

    # Cria as tasks para as duas buscas paralelas
    task1 = asyncio.create_task(busca_primeira_instancia(load.numero_processo, tribunal))
    task2 = asyncio.create_task(busca_segunda_instancia(load.numero_processo, tribunal))

    # Espera pelas duas tasks serem concluídas
    await asyncio.gather(task1, task2)

    # Obtem os resultados das buscas
    resultado1 = task1.result()
    resultado2 = task2.result()

    resultados = []

    if resultado1:
        resultados.append(resultado1)

    if resultado2:
        resultados.append(resultado2)

    if len(resultados) == 0:
        raise HTTPException(status_code=404, detail="Nenhum resultado encontrado")
    
    return resultados

@app.get("/tribunais")
async def get_tribunais():
    tribunais = listar_tribunais()
    return tribunais

@app.get("/tribunais/{tribunal_id}")
async def buscar_tribunal(tribunal_id: str):
    tribunal = buscar_tribunal_por_id(tribunal_id)
    if tribunal:
        return tribunal.__dict__
    else:
        raise HTTPException(status_code=404, detail="Tribunal não encontrado")
    
