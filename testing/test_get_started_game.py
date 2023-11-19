import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient

from src import app
from testing import get_test_db
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


def test_get_started_game(get_test_db):
    db = get_test_db
    client = TestClient(app)

    nickname1 = 'andy'
    response = client.get(f'/games/playing/{nickname1}')
    assert response.status_code == 404
    assert response.json()['detail'] == f"No existe un Usuario con nickname {nickname1}"

    response = client.post(f'/users?nickname={nickname1}')
    response = client.get(f'/games/playing/{nickname1}')
    assert response.status_code == 400
    assert response.json()['detail'] == f"Usuario {nickname1} no se encuentra en una Partida actualmente"

    game_name = 'Partida de Andy'
    body = {"game_name": game_name, "min_players": 4, "max_players": 12, "creator": nickname1}
    response = client.post(url="/games", json=body)
    response = client.patch(f'/users/{nickname1}?game_name={game_name}')
    response = client.get(f'/games/playing/{nickname1}')
    assert response.status_code == 400
    assert response.json()['detail'] == f"La Partida en la que se encuentre el Usuario {nickname1} aún no ha empezado"

    nickname2 = 'pepe'
    nickname3 = 'carla'
    nickname4 = 'juan'
    response = client.post(f'/users?nickname={nickname2}')
    response = client.post(f'/users?nickname={nickname3}')
    response = client.post(f'/users?nickname={nickname4}')
    response = client.patch(f'/users/{nickname2}?game_name={game_name}')
    response = client.patch(f'/users/{nickname3}?game_name={game_name}')
    response = client.patch(f'/users/{nickname4}?game_name={game_name}')
    response = client.post(f'/games/{nickname1}')
    response = client.get(f'/games/playing/{nickname1}')
    assert response.status_code == 200
    assert response.json()['game_name'] == game_name
    assert response.json()['phase'] == 'Playing'
    assert response.json()['creator'] == nickname1
    assert response.json()['active_player'] in [nickname1, nickname2, nickname3, nickname4]
    assert sorted(response.json()['alive_players']) == sorted([nickname1, nickname2, nickname3, nickname4])
    assert response.json()['locked_doors'] == [False, False, False, False]
    assert response.json()['quarantines'] == [False, False, False, False]
    assert len(response.json()['player_hand']) == 4 or response.json()['active_player'] == nickname1
    assert len(response.json()['player_hand']) == 5 or response.json()['active_player'] != nickname1
    assert response.json()['visible_cards'] == []
