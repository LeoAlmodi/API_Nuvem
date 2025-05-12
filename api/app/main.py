from fastapi import FastAPI
from auth import init_db
from routers import router

app = FastAPI()

# dispara criação de tabelas antes de aceitar requisições
@app.on_event("startup")
def startup_event():
    init_db()

app.include_router(router)
