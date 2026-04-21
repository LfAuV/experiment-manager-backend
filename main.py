from fastapi import FastAPI
from contextlib import asynccontextmanager
from routers import experiment
from db import create_db_and_tables

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield
# 还是不理解async和yield的具体用法

app = FastAPI(lifespan=lifespan)

app.include_router(experiment.router)

@app.get("/")
def root():
    return {"message": "Backend is running"}