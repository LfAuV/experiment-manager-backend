from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from contextlib import asynccontextmanager
from sqlmodel import Session, select


from routers import experiment, users
from db import create_db_and_tables, get_session
from security import verify_password
from models import User
"""
Run Indictate:
uvicorn main:app --reload
"""
@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield
# 还是不理解async和yield的具体用法

app = FastAPI(lifespan=lifespan)

app.include_router(experiment.router)
app.include_router(users.router)

@app.get("/")
def root():
    return {"message": "Backend is running"}

@app.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session)   
):
    statement = select(User).where(User.username == form_data.username)
    user = session.exec(statement).first()

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    access_token = f"token-{user.username}"

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }