from fastapi import HTTPException, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List

from src import app
from src.database import UsersTable, GamesTable, CardsTable, ShowedCardsTable, get_db
from src.CardsMetadata import CARDS_METADATA

@app.get("/games/playing/{nickname}")
def get_started_game(nickname: str, db: Session = Depends(get_db)):
    user: UsersTable | None = db.get(UsersTable, nickname)
    if user is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"No existe un Usuario con nickname {nickname}")
    if user.game_name is None:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, f"Usuario {nickname} no se encuentra en una Partida actualmente")

    game: GamesTable = db.get(GamesTable, user.game_name)
    if game.phase != 'Playing' and game.phase != 'Finished':
        raise HTTPException(status.HTTP_400_BAD_REQUEST, f"La Partida en la que se encuentre el Usuario {nickname} aún no ha empezado")

    alive_users: List[UsersTable] = (
        db
        .query(UsersTable)
        .filter(UsersTable.game_name == user.game_name)
        .filter(UsersTable.alive == True)
        .all()
    )

    active_user: UsersTable
    any((active_user := user).active for user in alive_users)

    for i in range(len(alive_users) - 1):
        for j in range(i + 1, len(alive_users)):
            if alive_users[j].nickname == alive_users[i].next_user:
                alive_users[i+1], alive_users[j] = alive_users[j], alive_users[i+1]
                break

    return JSONResponse(content={
        'game_name': game.name,
        'phase': game.phase,
        'creator': game.creator,
        'active_player': active_user.nickname,
        'alive_players': [user.nickname for user in alive_users],
        'locked_doors': [user.stuck_door for user in alive_users],
        'quarantines': [user.quarantine for user in alive_users],
        'player_hand': [
            {
                'name': card.name,
                'description': CARDS_METADATA[card.name]['description']
            }
            for card in db.query(CardsTable).filter(CardsTable.owner == nickname).all()
        ],
        'visible_cards': [
            {
                'name': card.name,
                'description': CARDS_METADATA[card.name]['description'],
                'owner': showed_card.owner
            }
            for showed_card in db.query(ShowedCardsTable).filter(ShowedCardsTable.viewer == nickname).all()
            if (card := db.get(CardsTable, showed_card.card_id))
        ]
    })
