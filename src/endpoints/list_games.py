from fastapi import HTTPException, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List

from src import app
from src.database import UsersTable, GamesTable, CardsTable, ShowedCardsTable, get_db
from pydantic import BaseModel


@app.get("/games")
def list_games(db: Session = Depends(get_db)):
    games: List[GamesTable] = (
        db
        .query(GamesTable)
        .filter(GamesTable.phase == 'Waiting')
        .filter(GamesTable.player_count < GamesTable.max_players)
        .all()
    )

    return JSONResponse(content={
        'games': [
            {
                "name": game.name,
                "creator": game.creator,
                "users_count": len(db.query(UsersTable).filter(UsersTable.game_name == game.name).all()),
                "users_in": [user.game_name for user in db.query(UsersTable).filter(UsersTable.game_name == game.name).all()],
                "min_players": game.min_players,
                "max_players": game.max_players
            }
            for game in games
        ]
    })
