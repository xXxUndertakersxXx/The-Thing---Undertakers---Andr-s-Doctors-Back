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


def test_start_game(get_test_db):
    db = get_test_db
    client = TestClient(app)

    nickname1 = 'andy'
    response = client.post(f'/games/{nickname1}')
    assert response.status_code == 404
    assert response.json()['detail'] == f"No existe un Usuario con nickname {nickname1}"

    response = client.post(f'/users?nickname={nickname1}')
    response = client.post(f'/games/{nickname1}')
    assert response.status_code == 400
    assert response.json()['detail'] == f"Usuario {nickname1} no se encuentra en una Partida actualmente"

    game_name = "Partida de Andy"
    body = {"game_name": game_name, "min_players": 4, "max_players": 12, "creator": nickname1}
    response = client.post(url="/games", json=body)
    response = client.patch(f'/users/{nickname1}?game_name={game_name}')
    response = client.post(f'/games/{nickname1}')
    assert response.status_code == 400
    assert response.json()['detail'] == "Pocos Usuarios en el Lobby"

    nickname2 = 'pepe'
    nickname3 = 'juan'
    nickname4 = 'carla'
    response = client.post(url=f"/users?nickname={nickname2}")
    response = client.patch(f'/users/{nickname2}?game_name={game_name}')
    response = client.post(url=f"/users?nickname={nickname3}")
    response = client.patch(f'/users/{nickname3}?game_name={game_name}')
    response = client.post(url=f"/users?nickname={nickname4}")
    response = client.patch(f'/users/{nickname4}?game_name={game_name}')
    response = client.post(f'/games/{nickname2}')
    assert response.status_code == 400
    assert response.json()['detail'] == f"{nickname2} no es el creador de la Partida"

    response = client.post(f'/games/{nickname1}')
    assert response.status_code == 200
    assert response.json()['game']['name'] == game_name
    assert response.json()['game']['creator'] == nickname1
    assert response.json()['game']['min_players'] == 4
    assert response.json()['game']['max_players'] == 12
    assert response.json()['game']['player_count'] == 4
    assert response.json()['game']['phase'] == 'Playing'

    actives, things, infecteds, humans = 0, 0, 0, 0
    assert len(response.json()['users']) == 4
    for user in response.json()['users']:
        assert user['nickname'] in [nickname1, nickname2, nickname3, nickname4]
        assert user['next_user'] in [nickname1, nickname2, nickname3, nickname4]
        assert user['game_name'] == game_name
        if user['role'] == 'The Thing':
            things += 1
        if user['role'] == 'Infected':
            infecteds += 1
        if user['role'] == 'Human':
            humans += 1
        if user['active']:
            actives += 1
    assert actives == 1
    assert things == 1
    assert infecteds == 0
    assert humans == 3

    things = 0
    cards_count = [0, 0, 0, 0]
    assert len(response.json()['cards']) > 20
    for card in response.json()['cards']:
        assert card['name'] in CARDS_METADATA
        assert card['game_name'] == game_name
        assert card['owner'] in ['Deck', nickname1, nickname2, nickname3, nickname4]
        if card['name'] == 'La Cosa':
            assert card['owner'] != 'Deck'
            things += 1
        if card['name'] == '¡Infectado!' and card['owner'] != 'Deck':
            user = db.get(UsersTable, card['owner'])
            assert user.active
        if card['owner'] == nickname1:
            cards_count[0] += 1
        if card['owner'] == nickname2:
            cards_count[1] += 1
        if card['owner'] == nickname3:
            cards_count[2] += 1
        if card['owner'] == nickname4:
            cards_count[3] += 1
    assert things == 1
    assert sorted(cards_count) == [4, 4, 4, 5]
