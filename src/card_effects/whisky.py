from fastapi import HTTPException, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List

from src.database import UsersTable, GamesTable, CardsTable, ShowedCardsTable, get_db


def whisky(user_nickname: str, target_nickname: str, game_name: str, db: Session):
    hand: List[CardsTable] = db.query(CardsTable).filter(CardsTable.owner == user_nickname).all()
    viewers: List[UsersTable] = db.query(UsersTable).filter(UsersTable.nickname != user_nickname).all()

    showed_cards = [
        ShowedCardsTable(
            card_id=card.id,
            owner=user_nickname,
            viewer=viewer.nickname
        )
        for card in hand
        for viewer in viewers
    ]

    db.add_all(showed_cards)
    db.commit()
