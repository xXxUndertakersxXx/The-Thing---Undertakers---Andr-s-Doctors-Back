from fastapi import HTTPException, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List
import random

from src.database import UsersTable, GamesTable, CardsTable, ShowedCardsTable, get_db


def sospecha(user_nickname: str, target_nickname: str, game_name: str, db: Session):
    target_hand: List[CardsTable] = db.query(CardsTable).filter(CardsTable.owner == target_nickname).all()

    i = random.randint(0, len(target_hand) - 1)
    showed_card: ShowedCardsTable = ShowedCardsTable(
        card_id=target_hand[i].id,
        owner=target_nickname,
        viewer=user_nickname
    )

    db.add(showed_card)
    db.commit()
