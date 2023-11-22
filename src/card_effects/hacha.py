from fastapi import HTTPException, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from src.database import UsersTable, GamesTable, CardsTable, ShowedCardsTable, get_db


def hacha(user_nickname: str, target_nickname: str, game_name: str, db: Session):
    user = db.get(UsersTable, user_nickname)
    target = db.get(UsersTable, target_nickname)
    target.quarantine = False

    if user.next_user == target_nickname:
        user.stuck_door = False
    else:
        target.stuck_door = False

    db.commit()
