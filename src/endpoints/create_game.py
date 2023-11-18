from fastapi import HTTPException, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from src import app
from src.database import UsersTable, GamesTable, CardsTable, ShowedCardsTable, get_db
from pydantic import BaseModel


class CreateGameModel(BaseModel):
    game_name: str
    min_players: int
    max_players: int
    creator: str


@app.post("/games")
def create_game(body: CreateGameModel, db: Session = Depends(get_db)):
    pass
