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


def test_create_game(get_test_db):
    db = get_test_db
    client = TestClient(app)

    creator = "andy"
    game_name = "Partida de Andy"

    body = {"game_name": game_name, "min_players": 3, "max_players": 12, "creator": creator}
    response = client.post(url="/games", json=body)
    assert response.status_code == 400
    assert response.json()["detail"] == "Parámetro `min_players` fuera de los límites"

    body = {"game_name": game_name, "min_players": 4, "max_players": 13, "creator": creator}
    response = client.post(url="/games", json=body)
    assert response.status_code == 400
    assert response.json()["detail"] == "Parámetro `max_players` fuera de los límites"

    body = {"game_name": game_name, "min_players": 4, "max_players": 12, "creator": creator}
    response = client.post(url="/games", json=body)
    assert response.status_code == 404
    assert response.json()["detail"] == f"No existe un usuario con nickname {creator}"

    client.post(f"/users?nickname={creator}")
    response = client.post(url="/games", json=body)
    assert response.status_code == 200
    assert response.json()["name"] == game_name
    assert response.json()["creator"] == creator
    assert response.json()["min_players"] == 4
    assert response.json()["max_players"] == 12
    assert response.json()["player_count"] == 0
    assert response.json()["phase"] == "Waiting"

    creator = "pepe"
    body["creator"] = creator
    client.post(f"/users?nickname={creator}")
    response = client.post(url="/games", json=body)
    assert response.status_code == 409
    assert response.json()["detail"] == "Ya existe una Partida con ese nombre"
