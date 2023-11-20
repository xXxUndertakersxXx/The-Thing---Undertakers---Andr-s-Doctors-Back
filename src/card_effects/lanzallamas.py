from fastapi import HTTPException, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from src.database import UsersTable, GamesTable, CardsTable, ShowedCardsTable, get_db


def lanzallamas(user_nickname: str, target_nickname: str, game_name: str, db: Session):
    target = db.get(UsersTable, target_nickname)
    target.alive = False

    users = []
    user = db.get(UsersTable, target.next_user)
    while user != target:
        users.append(user)
        user = db.get(UsersTable, user.next_user)

    for i in range(-1, len(users) - 1):
        users[i].next_user = users[i+1].nickname

    db.commit()
