from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import models
import oauth2
import schemas
from database import get_db
from googleBooksApi import get_books, get_book_by_id

router = APIRouter(
    tags=["books"],
    prefix="/books"
)


@router.get("/{title}/{id}", response_model=schemas.showBook)
async def get_book_by_id_route(id: str, db: Session = Depends(get_db),
                               current_user: schemas.User = Depends(oauth2.get_current_user)):
    db_comments = db.query(models.Comment).filter(models.Comment.book_id == id).all()
    comments = []
    for db_comment in db_comments:
        comment = schemas.Comment(
            content=db_comment.content,
            book_id=db_comment.book_id
            # Add other fields as necessary
        )
        comments.append(comment)
    book = await get_book_by_id(id)
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    return schemas.showBook(comments=comments, title=book.get('title'), description=book.get('description'),
                            image_resource=book.get('image_resource'))


# @router.post("/add", status_code=201, )
# async def create_book(book: schemas.Book, db: Session = Depends(get_db)):
#     new_book = models.Book(title=book.title, description=book.description, image_resourse=book.image_resourse)
#     db.add(new_book)
#     db.commit()
#     db.refresh(new_book)
#     return new_book

@router.get("/{title}", response_model=List[schemas.showBooks])
async def find_book(title: str, num_books: int, start_index: int, db: Session = Depends(get_db),
                    current_user: schemas.User = Depends(oauth2.get_current_user)):
    books = await get_books(query=title, num_books=num_books, start_index=start_index)
    if not books:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    return books
