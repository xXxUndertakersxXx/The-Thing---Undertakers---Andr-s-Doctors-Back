import random
from typing import List
from fastapi import HTTPException, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from src import app
from src.database import UsersTable, GamesTable, CardsTable, ShowedCardsTable, get_db

def draw_card(game_name: str, nickname: str, db: Session):
    deck: List[CardsTable] = (
        db
        .query(CardsTable)
        .filter(CardsTable.game_name == game_name)
        .filter(CardsTable.owner == 'Deck')
        .all()
    )

    i = random.randint(0, len(deck) - 1)
    deck[i].owner = nickname

    db.commit()
