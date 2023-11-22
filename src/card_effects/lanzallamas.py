from fastapi import HTTPException, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from src.database import UsersTable, GamesTable, CardsTable, ShowedCardsTable, get_db


def lanzallamas(user_nickname: str, target_nickname: str, game_name: str, db: Session):
    target: UsersTable = db.get(UsersTable, target_nickname)

    users = []
    user = db.get(UsersTable, target.next_user)
    while user != target:
        users.append(user)
        user = db.get(UsersTable, user.next_user)

    user.stuck_door = user.stuck_door or target.stuck_door
    for i in range(-1, len(users) - 1):
        users[i].next_user = users[i+1].nickname

    target.alive = False
    target.next_user = None

    db.commit()
