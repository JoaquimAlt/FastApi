import csv
import os
from typing import List
from models.mesa import Mesa

ARQUIVO_CSV = "mesas.csv"

# Inicializar o arquivo CSV
def inicializar_csv():
    if not os.path.exists(ARQUIVO_CSV):
        with open(ARQUIVO_CSV, mode="w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=["id", "nome_restaurante", "numero", "ocupada", "especificacao"])
            writer.writeheader()

# Ler mesas do arquivo CSV
def ler_mesas() -> List[Mesa]:
    mesas = []
    if os.path.exists(ARQUIVO_CSV):
        with open(ARQUIVO_CSV, mode="r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                mesa = Mesa(
                    id=int(row.get("id", 0)),
                    nome_restaurante=row.get("nome_restaurante", ""),
                    numero=int(row.get("numero", 0)),
                    ocupada=row.get("ocupada", "False") == "True",
                    especificacao=row.get("especificacao", "")
                )
                mesas.append(mesa)
    return mesas

# Salvar uma nova mesa
def salvar_mesa(mesa: Mesa):
    # Verifica se o arquivo está vazio antes de salvar
    precisa_cabecalho = not os.path.exists(ARQUIVO_CSV) or os.stat(ARQUIVO_CSV).st_size == 0
    with open(ARQUIVO_CSV, mode="a", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["id", "nome_restaurante", "numero", "ocupada", "especificacao"])
        if precisa_cabecalho:
            writer.writeheader()  # Escreve o cabeçalho apenas se necessário
        writer.writerow(mesa.__dict__)


# Sobrescrever todas as mesas
def sobrescrever_csv(mesas: List[Mesa]):
    with open(ARQUIVO_CSV, mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["id", "nome_restaurante", "numero", "ocupada", "especificacao"])
        writer.writeheader()
        for mesa in mesas:
            writer.writerow(mesa.__dict__)

# Inicializar o CSV ao importar
inicializar_csv()
