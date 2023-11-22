from fastapi import HTTPException, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from src.database import UsersTable, GamesTable, CardsTable, ShowedCardsTable, get_db


def cuarentena(user_nickname: str, target_nickname: str, game_name: str, db: Session):
    target = db.get(UsersTable, target_nickname)
    target.quarantine = True
    db.commit()
