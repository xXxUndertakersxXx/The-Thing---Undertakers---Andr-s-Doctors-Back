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


def test_create_user(get_test_db):
    db = get_test_db
    client = TestClient(app)

    nickname = "andy"
    response = client.post(url=f"/users?nickname={nickname}")
    assert response.status_code == 200
    body = response.json()
    assert body["nickname"] == "andy"
    assert all((key == "nickname" or body[key] is None) for key in body)

    response = client.post(url=f"/users?nickname={nickname}")
    assert response.status_code == 409
    assert response.json()["detail"] == "Ya existe un Usuario con ese nickname"
