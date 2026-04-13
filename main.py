from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello FastAPI"}

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/experiment/{experiment_id}")
def get_experiment(experiment_id: int):
    return {"experiment_id": experiment_id}