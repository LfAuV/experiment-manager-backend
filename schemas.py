from typing import Optional
from sqlmodel import SQLModel


class ExperimentCreate(SQLModel):
    experiment: str
    time: int
    status: str

class ExperimentUpdate(SQLModel):
    experiment: Optional[str] = None
    time: Optional[int] = None
    status: Optional[str] = None

class ExperimentRead(SQLModel):
    id: int
    experiment: str
    time: int
    status: str


class UserCreate(SQLModel):
    username: str
    password: str

class UserUpdate(SQLModel):
    username: Optional[str] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None

class UserRead(SQLModel):
    id: int
    username: str
    is_active: bool
