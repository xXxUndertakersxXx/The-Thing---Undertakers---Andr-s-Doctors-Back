from fastapi import HTTPException, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from src.database import UsersTable, GamesTable, CardsTable, ShowedCardsTable, get_db


def puerta_atrancada(user_nickname: str, target_nickname: str, game_name: str, db: Session):
    user = db.get(UsersTable, user_nickname)
    target = db.get(UsersTable, target_nickname)

    if user.next_user == target_nickname:
        user.stuck_door = True
    else:
        target.stuck_door = True

    db.commit()
