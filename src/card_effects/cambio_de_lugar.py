from fastapi import HTTPException, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from src.database import UsersTable, GamesTable, CardsTable, ShowedCardsTable, get_db


def cambio_de_lugar(user_nickname: str, target_nickname: str, game_name: str, db: Session):
    pass
