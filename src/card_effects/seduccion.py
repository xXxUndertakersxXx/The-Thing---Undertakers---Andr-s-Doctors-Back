import random
from fastapi import HTTPException, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List

from src.database import UsersTable, GamesTable, CardsTable, ShowedCardsTable, get_db


def seduccion(user_nickname: str, target_nickname: str, game_name: str, db: Session):
    user_hand: List[CardsTable] = db.query(CardsTable).filter(CardsTable.owner == user_nickname).all()
    target_hand: List[CardsTable] = db.query(CardsTable).filter(CardsTable.owner == target_nickname).all()

    i = random.randint(0, len(user_hand) - 1)
    j = random.randint(0, len(target_hand) - 1)

    user_hand[i].owner = target_nickname
    target_hand[j].owner = user_nickname

    db.commit()
