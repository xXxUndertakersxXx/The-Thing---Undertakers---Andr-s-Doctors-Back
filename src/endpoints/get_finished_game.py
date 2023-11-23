from fastapi import HTTPException, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List

from src import app
from src.database import UsersTable, GamesTable, CardsTable, ShowedCardsTable, get_db
from pydantic import BaseModel


@app.get("/games/finished/{nickname}")
def get_finished_game(nickname: str, db: Session = Depends(get_db)):
    user = db.get(UsersTable, nickname)
    users: List[UsersTable] = (
        db
        .query(UsersTable)
        .filter(UsersTable.game_name == user.game_name)
        .all()
    )

    humans, infecteds, the_thing = [], [], ''
    for user in users:
        if user.role == 'The Thing':
            the_thing = (user.nickname, user.alive)
        elif user.role == 'Infected':
            infecteds.append(user.nickname, user.alive)
        elif user.role == 'Human':
            humans.append((user.nickname, user.alive))

    winners = ''
    if any(human[1] for human in humans):
        winners = 'Humanos'
    elif the_thing[1]:
        winners = 'Infectados'

    return JSONResponse(content={
        'winners': winners,
        'humans': [human[0] for human in humans],
        'infected': [infected[0] for infected in infecteds],
        'the_thing': the_thing[0]
    })
