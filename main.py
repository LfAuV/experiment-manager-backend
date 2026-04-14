from fastapi import FastAPI
from pydantic import BaseModel
"""
Run Indictate:
uvicorn main:app --reload
"""
app = FastAPI()


class ExperimentCreate(BaseModel):
    name: str
    status: str


@app.get("/")
def read_root():
    return {"message": "Hello FastAPI"}

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/experiment/{experiment_id}")
def get_experiment_list(experiment_id: int):
    return {"experiment_id": experiment_id}

@app.get("/experiment")
def get_experiment_str(limit: int = 10, status: str = "running"):
    return {"limit": limit, "status": status}

@app.post("/experiment")
def create_experiment(experiment: ExperimentCreate):
    return {
        "message": "Created",
        "data": experiment
    }