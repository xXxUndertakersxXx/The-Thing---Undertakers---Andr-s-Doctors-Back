from fastapi import HTTPException, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from src import app
from src.database import UsersTable, GamesTable, CardsTable, ShowedCardsTable, get_db
from pydantic import BaseModel


@app.get("/games/waiting/{nickname}")
def get_lobby(nickname: str, db: Session = Depends(get_db)):
    user: UsersTable | None = db.get(UsersTable, nickname)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No existe un Usuario con nickname {nickname}")
    if user.game_name is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Usuario {nickname} no se encuentra en una Partida actualmente")

    game = db.get(GamesTable, user.game_name)
    players_in = [player.nickname for player in db.query(UsersTable).filter(UsersTable.game_name == game.name).all()]

    return JSONResponse(content={
        'game_name': game.name,
        'phase': game.phase,
        'creator': game.creator,
        'players_count': len(players_in),
        'players_in': players_in,
        'min_players': game.min_players,
        'max_players': game.max_players
    })
