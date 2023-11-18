from fastapi import HTTPException, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from src import app
from src.database import UsersTable, GamesTable, CardsTable, ShowedCardsTable, get_db
from pydantic import BaseModel


@app.post("/users")
def create_user(nickname: str, db: Session = Depends(get_db)):
    user = UsersTable(
        nickname=nickname,
    )

    try:
        db.add(user)
        db.commit()
        db.refresh(user)
    except:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Ya existe un Usuario con ese nickname")
    finally:
        db.close()

    return JSONResponse(content={c.name: getattr(user, c.name) for c in user.__table__.columns})
