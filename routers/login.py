from fastapi import APIRouter
from fastapi import FastAPI, Depends, status, HTTPException
from sqlalchemy.orm import Session
from schemas import Token
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

import database
import schemas, models
from database import engine, SessionLocal
from hashing import Hash
from my_token import create_access_token

get_db = database.get_db

router = APIRouter(
    tags=["login"]
)


@router.post("/login")
def login(request: OAuth2PasswordRequestForm = Depends(),  db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Incorrect credentials")
    if not Hash.verify(user.password, request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Incorrect password")

    access_token = create_access_token(
        data={"sub": user.email})
    return Token(access_token=access_token, token_type="bearer")
