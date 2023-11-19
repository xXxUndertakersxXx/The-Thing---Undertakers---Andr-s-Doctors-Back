import random
from typing import List
from fastapi import HTTPException, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from src import app
from src.CardsMetadata import CARDS_METADATA
from src.database import UsersTable, GamesTable, CardsTable, ShowedCardsTable, get_db
from src.draw_card import draw_card


@app.post("/games/{nickname}")
def start_game(nickname: str, db: Session = Depends(get_db)):
    user: UsersTable | None = db.get(UsersTable, nickname)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No existe un Usuario con nickname {nickname}")
    if user.game_name is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Usuario {nickname} no se encuentra en una Partida actualmente")

    game: GamesTable = db.get(GamesTable, user.game_name)
    if game.phase != 'Waiting':
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"La Partida de {nickname} no está esperando jugadores")
    if game.creator != user.nickname:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"{nickname} no es el creador de la Partida")
    if game.player_count < game.min_players:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Pocos Usuarios en el Lobby")

    users = init_users_stats(game.name, db)
    cards = create_cards(game.name, db)
    deal_cards(game, users, cards, db)

    for user in users:
        if user.active:
            draw_card(game.name, user.nickname, db)
            break

    game.phase = 'Playing'
    db.commit()

    return JSONResponse(content={
        'game': {c.name: getattr(game, c.name) for c in game.__table__.columns},
        'users': [
            {c.name: getattr(user, c.name) for c in user.__table__.columns}
            for user in users
        ],
        'cards': [
            {c.name: getattr(card, c.name) for c in card.__table__.columns}
            for card in cards
        ]
    })


def init_users_stats(game_name: str, db: Session):
    users: List[UsersTable] = db.query(UsersTable).filter(UsersTable.game_name == game_name).all()
    for user in users:
        user.role = 'Human'
        user.alive = True
        user.quarantine = False
        user.active = False

    i = random.randint(0, len(users) - 1)
    users[i].active = True

    random.shuffle(users)
    for i in range(-1, len(users) - 1):
        users[i].next_user = users[i + 1].nickname

    db.commit()
    return users


def create_cards(game_name: str, db: Session):
    cards: List[CardsTable] = []
    for card_name in CARDS_METADATA:
        cards += [
            CardsTable(
                game_name=game_name,
                name=card_name,
                owner='Deck'
            )
            for _ in range(CARDS_METADATA[card_name]['quantity'])
        ]

    db.add_all(cards)
    db.commit()

    return cards


def deal_cards(game: GamesTable, users: List[UsersTable], cards: List[CardsTable], db: Session):
    cards = [card for card in cards if (card.name != "La Cosa" and card.name != "¡Infectado!")]
    cards = cards[:(4*game.player_count - 1)]
    the_thing_card = (
        db
        .query(CardsTable)
        .filter(CardsTable.game_name == game.name)
        .filter(CardsTable.name == "La Cosa")
        .first()
    )

    cards.append(the_thing_card)
    random.shuffle(cards)

    for i in range(4 * game.player_count):
        card = cards[i]
        user = users[i // 4]

        card.owner = user.nickname
        if card.name == "La Cosa":
            user.role = 'The Thing'

    db.commit()
