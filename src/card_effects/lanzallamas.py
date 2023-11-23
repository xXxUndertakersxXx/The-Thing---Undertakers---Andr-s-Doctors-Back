from fastapi import HTTPException, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List

from src.database import UsersTable, GamesTable, CardsTable, ShowedCardsTable, get_db


def check_end_game(db: Session, game_name):
    alive_humans: List[UsersTable] = (
        db
        .query(UsersTable)
        .filter(UsersTable.game_name == game_name)
        .filter(UsersTable.alive == True)
        .filter(UsersTable.role == 'Human')
        .all()
    )

    the_thing: UsersTable = (
        db
        .query(UsersTable)
        .filter(UsersTable.game_name == game_name)
        .filter(UsersTable.role == 'The Thing')
        .first()
    )

    if alive_humans == [] or the_thing.alive == False:
        game: GamesTable = db.get(GamesTable, game_name)
        game.phase = 'Finished'

        db.commit()


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

    check_end_game(db, game_name)
    db.commit()
