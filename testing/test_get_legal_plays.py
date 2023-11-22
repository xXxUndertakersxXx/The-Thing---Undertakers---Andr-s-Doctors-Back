import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient

from src import app
from testing import get_test_db
from src.CardsMetadata import CARDS_METADATA
from src.database import UsersTable, GamesTable, CardsTable, ShowedCardsTable, __SessionLocal__
from src.endpoints.create_game import create_game, CreateGameModel
from src.endpoints.create_user import create_user
from src.endpoints.get_finished_game import get_finished_game
from src.endpoints.get_legal_plays import get_legal_plays
from src.endpoints.get_lobby import get_lobby
from src.endpoints.get_started_game import get_started_game
from src.endpoints.join_user import join_user
from src.endpoints.list_games import list_games
from src.endpoints.play_card import play_card
from src.endpoints.start_game import start_game


def test_get_legal_plays(get_test_db):
    db = get_test_db
    client = TestClient(app)

    nickname1 = 'andy'
    response = client.get(f'/games/playing/{nickname1}/active')
    assert response.status_code == 404
    assert response.json()['detail'] == f"No existe un Usuario con nickname {nickname1}"

    response = client.post(f'/users?nickname={nickname1}')
    response = client.get(f'/games/playing/{nickname1}/active')
    assert response.status_code == 400
    assert response.json()['detail'] == f"Usuario {nickname1} no se encuentra en una Partida actualmente"

    game_name = "Partida de Andy"
    body = {"game_name": game_name, "min_players": 4, "max_players": 12, "creator": nickname1}
    response = client.post(url="/games", json=body)
    response = client.patch(f'/users/{nickname1}?game_name={game_name}')
    response = client.get(f'/games/playing/{nickname1}/active')
    assert response.status_code == 400
    assert response.json()['detail'] == f"La Partida en la que se encuentre el Usuario {nickname1} aún no ha empezado"

    nickname2 = 'pepe'
    response = client.post(f'/users?nickname={nickname2}')
    response = client.patch(f'/users/{nickname2}?game_name={game_name}')
    nickname3 = 'carla'
    response = client.post(f'/users?nickname={nickname3}')
    response = client.patch(f'/users/{nickname3}?game_name={game_name}')
    nickname4 = 'juan'
    response = client.post(f'/users?nickname={nickname4}')
    response = client.patch(f'/users/{nickname4}?game_name={game_name}')
    response = client.post(f'/games/{nickname1}')

    active_user = None
    for user in response.json()['users']:
        if user['active']:
            active_user = user['nickname']
    inactive_user = nickname1 if active_user != nickname1 else nickname2

    response = client.get(f'/games/playing/{inactive_user}/active')
    assert response.status_code == 400
    assert response.json()['detail'] == f"Usuario {inactive_user} no es el jugador activo"

    response = client.get(f'/games/playing/{active_user}/active')
    assert response.status_code == 200
    for card_name in response.json()['playable_cards']:
        card = response.json()['playable_cards'][card_name]

        needs_target = card['needs_target']
        valid_targets = card['valid_targets']
        target_type = CARDS_METADATA[card_name]['target_type']

        assert card_name in CARDS_METADATA
        assert needs_target == (target_type != "NA")

        if target_type == "NA":
            assert valid_targets is None
        elif target_type == "ADYACENT":
            assert len(valid_targets) == 2
        elif target_type == "ANY":
            assert len(valid_targets) == 3
        else:
            assert False
