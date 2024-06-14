from fastapi import FastAPI

import models
import routers
from database import engine
from routers import books, comments, users, login

models.Base.metadata.create_all(engine)

app = FastAPI()

app.include_router(login.router)
app.include_router(books.router)
app.include_router(comments.router)
app.include_router(users.router)



