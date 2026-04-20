from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import Optional
"""
Run Indictate:
uvicorn main:app --reload
"""
router = APIRouter(prefix="/users", tags=["users"])

fake_db = {
    1: {"name": "Tom", "age": 20, "status": "active", "password": "002"},
    2: {"name": "Jerry", "age": 22, "status": "inactive", "password": "001"}
}

class UserCreate(BaseModel):
    name: str
    age: int
    status: str


class UserUpdate(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    status: Optional[str] = None


class UserOut(BaseModel):
    name: str
    age: int
    status: str

@router.get("/{user_id}", response_model=UserOut)
def get_user(user_id: int):
    if user_id not in fake_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User Not Found"
        )
    return fake_db[user_id]

@router.post("/", response_model = UserOut,status_code = status.HTTP_201_CREATED)
def create_user(user: UserCreate):
    new_id = max(fake_db.keys())+1
    fake_db[new_id] = user.model_dump()
    return fake_db[new_id]

@router.put("/{user_id}", response_model=UserOut)
def update_user_put(user_id: int, user: UserCreate):
    if user_id not in fake_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User Not Found"
        )
    fake_db[user_id] = user.model_dump()
    return fake_db[user_id]

@router.patch("{user_id}", response_model=UserOut)
def update_user_patch(user_id: int, user:UserUpdate):
    if user_id not in fake_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User Not Found"
        )
    stored_user = fake_db[user_id]
    update_data = user.model_dump(exclude_unset=True)
    stored_user.update(update_data)
    fake_db[user_id] = stored_user
    return fake_db[user_id]

@router.delete("/{user_id}", response_model=UserOut)
def delete_user(user_id: int):
    if user_id not in fake_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User Not Found"
        )
    
    deleted_user = fake_db.pop(user_id)
    return deleted_user