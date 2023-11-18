from fastapi import HTTPException, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from src import app
from src.database import UsersTable, GamesTable, CardsTable, ShowedCardsTable, get_db
from pydantic import BaseModel


class CreateGameModel(BaseModel):
    game_name: str
    min_players: int
    max_players: int
    creator: str


@app.post("/games")
def create_game(body: CreateGameModel, db: Session = Depends(get_db)):
    if body.min_players < 4:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Parámetro `min_players` fuera de los límites")
    if body.max_players > 12:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Parámetro `max_players` fuera de los límites")

    creator_user: UsersTable | None = db.get(UsersTable, body.creator)
    if creator_user is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"No existe un usuario con nickname {body.creator}")
    if creator_user.game_name is not None:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail=f"Usuario {body.creator} ya se encuentra en una Partida actualmente")

    game = GamesTable(
        name=body.game_name,
        creator=body.creator,
        min_players=body.min_players,
        max_players=body.max_players,
        player_count=0,
        phase='Waiting'
    )

    try:
        db.add(game)
        db.commit()
    except:
        db.rollback()
        raise HTTPException(status.HTTP_409_CONFLICT, detail="Ya existe una Partida con ese nombre")

    return JSONResponse(content={c.name: getattr(game, c.name) for c in game.__table__.columns})
