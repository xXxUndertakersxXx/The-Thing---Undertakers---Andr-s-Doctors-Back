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


def test_join_user(get_test_db):
    db = get_test_db
    client = TestClient(app)

    nickname = 'andy'
    game_name = 'LaPartidaDeAndy'

    response = client.patch(f'/users/{nickname}?game_name={game_name}')
    assert response.status_code == 404
    assert response.json()['detail'] == f"No existe un Usuario con nickname {nickname}"

    response = client.post(f'/users?nickname={nickname}')
    response = client.patch(f'/users/{nickname}?game_name={game_name}')
    assert response.status_code == 404
    assert response.json()['detail'] == f"No existe una Partida con nombre {game_name}"

    body = {"game_name": game_name, "min_players": 4, "max_players": 12, "creator": nickname}
    response = client.post(f'/games', json=body)
    response = client.patch(f'/users/{nickname}?game_name={game_name}')
    assert response.status_code == 200
    assert response.json()['user']['nickname'] == nickname
    assert response.json()['user']['game_name'] == game_name
    assert response.json()['game']['name'] == game_name
    assert response.json()['game']['player_count'] == 1

    response = client.patch(f'/users/{nickname}?game_name={game_name}')
    assert response.status_code == 400
    assert response.json()['detail'] == f"Usuario {nickname} ya se encuentra en una Partida actualmente"
