from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from http import HTTPStatus
from utils.operacoes_csv import ler_mesas, salvar_mesa, sobrescrever_csv
from utils.operacoes_arquivo import compactar_csv, calcular_hash_csv
from models.mesa import Mesa

router = APIRouter()

ARQUIVO_ZIP = "mesas.zip"

@router.get("/mesas")
def listar_mesas():
    mesas = ler_mesas()
    if not mesas:
        return {"msg": "Nenhuma mesa cadastrada"}
    return mesas


@router.post("/mesas", status_code=HTTPStatus.CREATED)
def adicionar_mesa(mesa: Mesa):
    mesas = ler_mesas()
    if any(mesa_atual.id == mesa.id for mesa_atual in mesas):
        raise HTTPException(status_code=400, detail="ID da mesa existente")
    salvar_mesa(mesa)
    return mesa


@router.put("/mesas/{mesa_id}")
def atualizar_mesa(mesa_id: int, mesa: Mesa):
    mesas = ler_mesas()
    for index, mesa_atual in enumerate(mesas):
        if mesa_atual.id == mesa_id:
            mesas[index] = mesa
            sobrescrever_csv(mesas)
            return mesa
    raise HTTPException(status_code=404, detail="Mesa não encontrada")


@router.delete("/mesas/{mesa_id}", status_code=HTTPStatus.NO_CONTENT)
def deletar_mesa(mesa_id: int):
    mesas = ler_mesas()
    for index, mesa_atual in enumerate(mesas):
        if mesa_atual.id == mesa_id:
            del mesas[index]
            sobrescrever_csv(mesas)
            return
    raise HTTPException(status_code=404, detail="Mesa não encontrada")


@router.get("/mesas/quantidade")
def quantidade_mesas():
    mesas = ler_mesas()
    return {"quantidade": len(mesas)}


@router.get("/mesas/zip", response_class=FileResponse)
def obter_csv_zip():
    compactar_csv()
    return FileResponse(ARQUIVO_ZIP, media_type="application/zip", filename=ARQUIVO_ZIP)


@router.get("/mesas/hash")
def obter_hash_csv():
    hash_csv = calcular_hash_csv()
    return {"sha256": hash_csv}
