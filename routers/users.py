from fastapi import APIRouter, HTTPException, status, Depends
from sqlmodel import Session, select
from typing import List
from db import get_session
from schemas import UserCreate, UserUpdate, UserRead
from models import User
from security import hash_password

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/", response_model=List[UserRead])
def get_users(session: Session = Depends(get_session)):
    users = session.exec(select(User)).all()
    return users


@router.get("/{user_id}", response_model=UserRead)
def get_user(user_id: int, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User Not Found"
        )
    return user

@router.post("/", response_model = UserRead,status_code = status.HTTP_201_CREATED)
def create_user(data: UserCreate, session: Session = Depends(get_session)):
    user = User(
        username=data.username,
        hashed_password=hash_password(data.password)
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

@router.put("/{user_id}", response_model=UserRead)
def update_user_put(
    user_id: int, 
    data: UserCreate,
    session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User Not Found"
        )
    user.username = data.username
    user.hashed_password = hash_password(data.password)

    session.add(user)
    session.commit()
    session.refresh(user)
    return user

@router.patch("/{user_id}", response_model=UserRead)
def update_user_patch(
    user_id: int, 
    data: UserUpdate,
    session: Session = Depends(get_session)
    ):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User Not Found"
        )
    
    update_data = data.model_dump(exclude_unset=True)

    if "password" in update_data:
        user.hashed_password = hash_password(update_data.pop("password"))

    for key, value in update_data.items():
        setattr(user, key, value)
    
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

@router.delete("/{user_id}", response_model=UserRead)
def delete_user(
    user_id: int,
    session: Session = Depends(get_session)
    ):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User Not Found"
        )
    session.delete(user)
    session.commit()
    return user
