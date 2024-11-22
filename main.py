from fastapi import FastAPI
from routes import mesas

app = FastAPI()

# Registrar as rotas
app.include_router(mesas.router)

@app.get("/")
def root():
    return {"msg": "Bem-vindo à API de Gerenciamento de Mesas!"}
