from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
"""
Run Indictate:
uvicorn main:app --reload
"""
app = FastAPI()

fake_db = {
    1: {"name": "Tom", "age": 20, "status": "active"},
    2: {"name": "Jerry", "age": 22, "status": "inactive"}
}

class UserCreate(BaseModel):
    name: str
    age: int
    status: str


class UserUpdate(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    status: Optional[str] = None


@app.get("/users/{user_id}")
def get_user(user_id: int):
    if user_id not in fake_db:
        return {"error": "User not found"}
    return fake_db[user_id]

@app.get("/experiment")
def get_experiment_str(limit: int = 10, status: str = "running"):
    return {"limit": limit, "status": status}

@app.post("/users/")
def create_user(user: UserCreate):
    new_id = max(fake_db.keys())+1
    fake_db[new_id] = user.model_dump()
    return {
        "message": "Created Successfully",
        "id": new_id,
        "data": fake_db[new_id]
    }

@app.put("/users/{user_id}")
def update_user_put(user_id: int, user: UserCreate):
    if user_id not in fake_db:
        return {"error": "user not found"}
    fake_db[user_id] = user.model_dump()
    return {
        "message": "Updated Successfully",
        "id": user_id,
        "data": fake_db[user_id]
    }

@app.patch("/users/{user_id}")
def update_user_patch(user_id: int, user:UserUpdate):
    if user_id not in fake_db:
        return {"error": "User not found"}
    stored_user = fake_db[user_id]
    update_data = user.model_dump(exclude_unset=True)
    stored_user.update(update_data)
    fake_db[user_id] = stored_user
    return {
        "message": "updated by patch", 
        "data": fake_db[user_id]
    }

@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    if user_id not in fake_db:
        return {"error": "User not found"}
    
    deleted_user = fake_db.pop(user_id)
    return {
        "message": "Deleted successfully",
        "data": deleted_user
    }