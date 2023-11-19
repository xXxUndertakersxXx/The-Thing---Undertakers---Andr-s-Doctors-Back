from fastapi import HTTPException, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from src.database import UsersTable, GamesTable, CardsTable, ShowedCardsTable, get_db


def mas_vale_que_corras(user_nickname: str, target_nickname: str, game_name: str, db: Session):
    pass
