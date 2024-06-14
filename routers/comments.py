from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import models
import oauth2
import schemas
from database import get_db

router = APIRouter(
    tags=["comments"],
    prefix="/comments"
)

@router.post("/add", status_code=201,)
def post_comment(comment: schemas.Comment, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    user = db.query(models.User).filter(models.User.email == current_user.email).first()
    new_comm = models.Comment(content = comment.content, book_id = comment.book_id, user_id = user.id)
    db.add(new_comm)
    db.commit()
    db.refresh(new_comm)
    return new_comm


@router.get("/getComments", status_code=200)
def get_comments(db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    user = db.query(models.User).filter(models.User.email == current_user.email).first()
    comments = db.query(models.Comment).filter(models.Comment.user_id == user.id).all()
    if not comments:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comments not found")
    return comments

@router.delete("/deleteComment", status_code=200)
def get_comments(comment_id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    user = db.query(models.User).filter(models.User.email == current_user.email).first()
    comment = db.query(models.Comment).filter(models.Comment.id == comment_id)
    if not comment.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")
    if(comment.first().user_id != user.id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="You cannot delete this comment")

    comment.delete(synchronize_session=False)
    db.commit()
    return True