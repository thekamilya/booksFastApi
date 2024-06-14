from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import hashing
import models
import schemas
from database import get_db

router = APIRouter(
    tags=["users"],
    prefix="/users"
)

@router.post("/", response_model= schemas.showUser)
async def addUser(user: schemas.User, db: Session = Depends(get_db)):
    new_user = models.User(name=user.name, email=user.email, password= hashing.Hash.bcrypt(user.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

