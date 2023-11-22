from fastapi import HTTPException, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from src.database import UsersTable, GamesTable, CardsTable, ShowedCardsTable, get_db
from src.swap_seats import swap_seats


def mas_vale_que_corras(user_nickname: str, target_nickname: str, game_name: str, db: Session):
    swap_seats(user_nickname, target_nickname, game_name, db)
