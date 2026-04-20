from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import Optional
from dependencies import get_current_user

router = APIRouter(
    prefix="/experiments",
    tags=["experiments"]
)

fake_db = {
    1: {"experiment": "EXPA", "time": 20, "status": "done", "password": "002"},
    2: {"experiment": "EXPB", "time": 22, "status": "done", "password": "001"}
}

class ExperimentCreate(BaseModel):
    experiment: str
    time: int
    status: str

class ExperimentUpdate(BaseModel):
    experiment: Optional[str] = None
    time: Optional[int] = None
    status: Optional[str] = None

class ExperimentOut(BaseModel):
    experiment: str
    time: int
    status: str

@router.get("/")
def list_experiments(pagination = Depends(get_current_user)):
    return {
        "message": "list experiments",
        "pagination": pagination
    }

@router.get("/{exp_id}", response_model=ExperimentOut)
def get_experiment(exp_id: int):
    if exp_id not in fake_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Experiment Not Found"
        )
    return fake_db[exp_id]

@router.post("/", response_model=ExperimentOut, status_code=status.HTTP_201_CREATED)
def create_experiment(experiment: ExperimentCreate):
    new_id = max(fake_db.keys()) + 1
    fake_db[new_id] = experiment.model_dump()
    return fake_db[new_id]

@router.put("/{exp_id}", response_model=ExperimentOut)
def update_experiment_put(exp_id: int, experiment: ExperimentCreate):
    if exp_id not in fake_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Experiment Not Found"
        )
    fake_db[exp_id] = experiment.model_dump()
    return fake_db[exp_id]

@router.patch("/{exp_id}", response_model=ExperimentOut)
def update_experiment_patch(exp_id: int, experiment: ExperimentUpdate):
    if exp_id not in fake_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Experiment Not Found"
        )
    stored_experiment = fake_db[exp_id]
    update_data = experiment.model_dump(exclude_unset=True)
    stored_experiment.update(update_data)
    fake_db[exp_id] = stored_experiment
    return fake_db[exp_id]

@router.delete("/{exp_id}", response_model=ExperimentOut)
def delete_experiment(exp_id: int):
    if exp_id not in fake_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Experiment Not Found"
        )
    deleted_experiment = fake_db.pop(exp_id)
    return deleted_experiment