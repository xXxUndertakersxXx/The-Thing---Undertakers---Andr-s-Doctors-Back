from fastapi import HTTPException, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List

from src.database import UsersTable, GamesTable, CardsTable, ShowedCardsTable, get_db


def analisis(user_nickname: str, target_nickname: str, game_name: str, db: Session):
    target_hand: List[CardsTable] = db.query(CardsTable).filter(CardsTable.owner == target_nickname).all()
    showed_cards = [
        ShowedCardsTable(
            card_id=card.id,
            owner=target_nickname,
            viewer=user_nickname
        )
        for card in target_hand
    ]
    db.add_all(showed_cards)
    db.commit()
