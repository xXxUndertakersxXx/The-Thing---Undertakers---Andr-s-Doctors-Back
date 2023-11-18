from fastapi import HTTPException, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from src import app
from src.database import UsersTable, GamesTable, CardsTable, ShowedCardsTable, get_db
from pydantic import BaseModel


@app.patch("/users/{nickname}")
def join_user(nickname: str, game_name: str, db: Session = Depends(get_db)):
    pass
