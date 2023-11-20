from fastapi import HTTPException, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from src import app
from src.draw_card import draw_card
from src.CardsMetadata import CARDS_METADATA
from src.database import UsersTable, GamesTable, CardsTable, ShowedCardsTable, get_db
from pydantic import BaseModel


@app.post("/games/playing/{nickname}")
def play_card(nickname: str, discard: bool, card_name: str, target: str | None = None, db: Session = Depends(get_db)):
    user: UsersTable | None = db.get(UsersTable, nickname)
    if user is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"No existe un Usuario con nickname {nickname}")
    if user.game_name is None:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, f"Usuario {nickname} no se encuentra en una Partida actualmente")

    game = db.get(GamesTable, user.game_name)
    if game.phase == 'Waiting':
        raise HTTPException(status.HTTP_400_BAD_REQUEST, f"La Partida en la que se encuentre el Usuario {nickname} aún no ha empezado")
    if game.phase == 'Finished':
        raise HTTPException(status.HTTP_400_BAD_REQUEST, f"La Partida en la que se encuentre el Usuario {nickname} ya terminó")

    if not user.active:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, f"Usuario {nickname} no es el jugador activo")

    play_response = {}
    if not discard:
        target = target if (target is not None) else ""
        play_response = CARDS_METADATA[card_name]['play'](nickname, target, game.name, db)

    card: CardsTable = (
        db
        .query(CardsTable)
        .filter(CardsTable.owner == nickname)
        .filter(CardsTable.name == card_name)
        .first()
    )
    card.owner = 'Graveyard'
    db.query(ShowedCardsTable).filter(ShowedCardsTable.card_id == card.id).delete()

    next_user = db.get(UsersTable, user.next_user)
    draw_card(game.name, next_user.nickname, db)
    user.active = False
    next_user.active = True
    db.commit()

    return JSONResponse(content={
        'play_response': play_response,
        'game': {c.name: getattr(game, c.name) for c in game.__table__.columns},
        'users': [
            {c.name: getattr(user, c.name) for c in user.__table__.columns}
            for user in db.query(UsersTable).all()
        ],
        'cards': [
            {c.name: getattr(card, c.name) for c in card.__table__.columns}
            for card in db.query(CardsTable).all()
        ],
        'showed_cards': [
            {c.name: getattr(card, c.name) for c in card.__table__.columns}
            for card in db.query(CardsTable).all()
        ],
    })
