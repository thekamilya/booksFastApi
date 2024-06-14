from typing import List, Union

from pydantic import BaseModel


class Book(BaseModel):
    title: str
    description: str
    image_resource:str



class Comment(BaseModel):
    content:str
    book_id:str


class User(BaseModel):
    name: str
    email: str
    password: str

class showBook(BaseModel):
    title: str
    description: str
    image_resource:str
    comments: List[Comment]

    class Config:
        orm_mode = True
class showBooks(BaseModel):
    id: str
    title: str
    description: str
    image_resourse:str

    class Config:
        orm_mode = True

class showUser(BaseModel):
    name: str
    email: str

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Union[str, None] = None

class LoginData(BaseModel):
    email:str
    password:str