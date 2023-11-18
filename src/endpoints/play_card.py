from fastapi import HTTPException, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from src import app
from src.database import UsersTable, GamesTable, CardsTable, ShowedCardsTable, get_db
from pydantic import BaseModel


@app.post("/games/playing/{nickname}")
def play_card(nickname: str, discard: bool, card_name: str, target: str | None = None, db: Session = Depends(get_db)):
    pass
