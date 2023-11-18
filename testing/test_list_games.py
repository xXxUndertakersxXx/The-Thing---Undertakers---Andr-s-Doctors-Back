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


def test_list_games(get_test_db):
    db = get_test_db
    client = TestClient(app)

    response = client.get('/games')
    assert response.status_code == 200
    assert response.json()['games'] == []

    creator1 = 'andy'
    response = client.post(f'/users?nickname={creator1}')

    game_name1 = 'Partida de Andy'
    body = {"game_name": game_name1, "min_players": 4, "max_players": 12, "creator": creator1}
    response = client.post(url="/games", json=body)
    game1 = response.json()

    response = client.get('/games')
    assert response.status_code == 200
    assert len(response.json()['games']) == 1

    creator2 = 'pepe'
    response = client.post(f'/users?nickname={creator2}')

    game_name2 = 'Partida de Pepe'
    body = {"game_name": game_name2, "min_players": 4, "max_players": 12, "creator": creator2}
    response = client.post(url="/games", json=body)
    game2 = response.json()

    response = client.get('/games')
    assert response.status_code == 200
    assert len(response.json()['games']) == 2

    assert response.json()['games'][0] == {
        'creator': 'andy',
        'max_players': 12,
        'min_players': 4,
        'name': 'Partida de Andy',
        'users_count': 0,
        'users_in': []
    }

    assert response.json()['games'][1] == {
        'creator': 'pepe',
        'max_players': 12,
        'min_players': 4,
        'name': 'Partida de Pepe',
        'users_count': 0,
        'users_in': []
    }
