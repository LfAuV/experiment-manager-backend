from fastapi import FastAPI, Depends, status, HTTPException
from routers import users, experiments
from fastapi.security import OAuth2PasswordRequestForm

app = FastAPI()

app.include_router(users.router)
app.include_router(experiments.router)

fake_users = {
    "alice": {"username": "alice", "password": "123456"},
    "bob": {"username": "bob", "password": "abcdef"}
}

@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = fake_users.get(form_data.username)

    if not user or user["password"] != form_data.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    
    access_token = f"token-{form_data.username}"

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }