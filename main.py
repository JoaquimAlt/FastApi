from typing import List
from http import HTTPStatus
from fastapi import FastAPI, HTTPException
from models import Mesa
import pickle

app = FastAPI()

mesas_file = "mesas_app.pkl"

# Carregar as mesas do arquivo no início
try:
    with open(mesas_file, "rb") as f:
        mesas: List[Mesa] = pickle.load(f)
except Exception as e:
    print(e)
    mesas: List[Mesa] = []

# Função para salvar as mesas no arquivo
def salvar_mesas():
    with open(mesas_file, "wb") as f:
        pickle.dump(mesas, f)

@app.get("/")
def listar_mesas():
    if not mesas:
        return {"msg": "Nenhuma mesa cadastrada"}
    return mesas

@app.post("/mesas", status_code=HTTPStatus.CREATED)
def adicionar_mesa(mesa: Mesa) -> Mesa:
    if any(mesa_atual.id == mesa.id for mesa_atual in mesas):
        raise HTTPException(status_code=400, detail="ID da mesa existente")
    mesas.append(mesa)
    salvar_mesas()  # Salva as mesas atualizadas no arquivo
    return mesa

@app.put("/mesas/{mesa_id}")
def atualizar_mesa(mesa_id: int, mesa: Mesa) -> Mesa:
    for index, mesa_atual in enumerate(mesas):
        if mesa_atual.id == mesa_id:
            mesas[index] = mesa
            salvar_mesas()  # Salva as mesas atualizadas no arquivo
            return mesa
    raise HTTPException(status_code=404, detail="Mesa não encontrada")

@app.delete("/mesas/{mesa_id}", status_code=HTTPStatus.NO_CONTENT)
def deletar_mesa(mesa_id: int):
    for index, mesa_atual in enumerate(mesas):
        if mesa_atual.id == mesa_id:
            del mesas[index]
            salvar_mesas()  # Salva as mesas atualizadas no arquivo
            return  # Retorna sem conteúdo, apenas o status 204
    raise HTTPException(status_code=404, detail="Mesa não encontrada")
