from fastapi import HTTPException, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List

from src import app
from src.CardsMetadata import CARDS_METADATA
from src.database import UsersTable, GamesTable, CardsTable, ShowedCardsTable, get_db


@app.get("/games/playing/{nickname}/active")
def get_legal_plays(nickname: str, db: Session = Depends(get_db)):
    user: UsersTable | None = db.get(UsersTable, nickname)
    if user is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"No existe un Usuario con nickname {nickname}")
    if user.game_name is None:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, f"Usuario {nickname} no se encuentra en una Partida actualmente")

    game: GamesTable = db.get(GamesTable, user.game_name)
    if game.phase == 'Waiting':
        raise HTTPException(status.HTTP_400_BAD_REQUEST, f"La Partida en la que se encuentre el Usuario {nickname} aún no ha empezado")
    if game.phase == 'Finished':
        raise HTTPException(status.HTTP_400_BAD_REQUEST, f"La Partida en la que se encuentre el Usuario {nickname} ya terminó")

    if not user.active:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, f"Usuario {nickname} no es el jugador activo")

    hand: List[CardsTable] = db.query(CardsTable).filter(CardsTable.owner == nickname).all()
    players: List[UsersTable] = db.query(UsersTable).filter(UsersTable.game_name == user.game_name).all()
    adyacent_players: List[UsersTable] = list(filter(lambda player: player.next_user == user.nickname or user.next_user == player.nickname, players))
    players_nicknames: List[str] = [player.nickname for player in players if player.nickname != user.nickname]
    adyacent_players_nicknames = [adyacent_player.nickname for adyacent_player in adyacent_players]

    def valid_targets(card_name):
        if CARDS_METADATA[card_name]['target_type'] == "NA":
            return None
        elif CARDS_METADATA[card_name]['target_type'] == "ADYACENT":
            return adyacent_players_nicknames
        elif CARDS_METADATA[card_name]['target_type'] == "ANY":
            return players_nicknames

    return JSONResponse(content={
        'playable_cards': [
            {
                'name': card.name,
                'needs_target': CARDS_METADATA[card.name]['target_type'] != "NA",
                'valid_targets': valid_targets(card.name)
            }
            for card in hand
        ]
    })