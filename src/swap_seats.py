from fastapi import HTTPException, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List

from src.database import UsersTable, GamesTable, CardsTable, ShowedCardsTable, get_db


def swap_seats(user_nickname: str, target_nickname: str, game_name: str, db: Session):
    user: UsersTable = db.get(UsersTable, user_nickname)

    users: List[UsersTable] = [user]
    user2: UsersTable = db.get(UsersTable, user.next_user)
    while user2 != user:
        users.append(user2)
        user2 = db.get(UsersTable, user2.next_user)

    target_idx = None
    for i, user2 in enumerate(users):
        if(user2.nickname == target_nickname):
            target_idx = i

    users[0], users[target_idx] = users[target_idx], users[0]
    for i in range(-1, len(users) - 1):
        users[i].next_user = users[i + 1].nickname

    db.commit()
