from pydantic import BaseModel

class Mesa(BaseModel):
    id: int
    nome_restaurante: str
    numero: int
    ocupada: bool
    especificacao: str
