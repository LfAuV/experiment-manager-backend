from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List
from db import get_session
from schemas import ExperimentCreate, ExperimentRead, ExperimentUpdate
from models import Experiment


router = APIRouter(
    prefix="/experiments",
    tags=["experiments"]
)


@router.get("/", response_model=List[ExperimentRead])
def list_experiments(session: Session = Depends(get_session)):
    experiments = session.exec(select(Experiment)).all()
    return experiments

@router.get("/{exp_id}", response_model=ExperimentRead)
def get_experiment(exp_id: int, session: Session = Depends(get_session)):
    experiment = session.get(Experiment, exp_id)
    if not experiment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Experiment Not Found"
        )
    return experiment

@router.post("/", response_model=ExperimentRead, status_code=status.HTTP_201_CREATED)
def create_experiment(data: ExperimentCreate, session: Session = Depends(get_session)):
    experiment = Experiment.model_validate(data)
    session.add(experiment)
    session.commit()
    session.refresh(experiment)
    return experiment

@router.put("/{exp_id}", response_model=ExperimentRead)
def update_experiment_put(
    exp_id: int, 
    data: ExperimentCreate,
    session: Session = Depends(get_session)
    ):
    experiment = session.get(Experiment, exp_id)
    if not experiment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Experiment Not Found"
        )
    experiment.experiment = data.experiment
    experiment.time = data.time
    experiment.status = data.status

    session.add(experiment)
    session.commit()
    session.refresh(experiment)
    return experiment

@router.patch("/{exp_id}", response_model=ExperimentRead)
def update_experiment_patch(
    exp_id: int, 
    data: ExperimentUpdate,
    session: Session = Depends(get_session)):
    experiment = session.get(Experiment, exp_id)
    if not experiment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Experiment Not Found"
        )
    update_data = data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(experiment, key, value)

    session.add(experiment)
    session.commit()
    session.refresh(experiment)

    return experiment

@router.delete("/{exp_id}", response_model=ExperimentRead)
def delete_experiment(
    exp_id: int,
    session: Session = Depends(get_session)
    ):
    experiment = session.get(Experiment, exp_id)
    if not experiment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Experiment Not Found"
        )
    session.delete(experiment)
    session.commit()
    return experiment