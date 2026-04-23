from typing import Optional
from sqlmodel import SQLModel, Field


class Experiment(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    experiment: str
    time: int
    status: str

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    hashed_password: str
    is_active: bool = True