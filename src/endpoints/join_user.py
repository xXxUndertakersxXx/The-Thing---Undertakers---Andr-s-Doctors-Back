from fastapi import HTTPException, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from src import app
from src.database import UsersTable, GamesTable, CardsTable, ShowedCardsTable, get_db
from pydantic import BaseModel


@app.patch("/users/{nickname}")
def join_user(nickname: str, game_name: str, db: Session = Depends(get_db)):
    user: UsersTable | None = db.get(UsersTable, nickname)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No existe un Usuario con nickname {nickname}")
    if user.game_name is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Usuario {nickname} ya se encuentra en una Partida actualmente")

    game: GamesTable | None = db.get(GamesTable, game_name)
    if game is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No existe una Partida con nombre {game_name}")

    try:
        user.game_name = game.name
        game.player_count += 1
        db.commit()
    except:
        db.rollback()

    return JSONResponse(content={
        'user': {c.name: getattr(user, c.name) for c in user.__table__.columns},
        'game': {c.name: getattr(game, c.name) for c in game.__table__.columns},
    })
