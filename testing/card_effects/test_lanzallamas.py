import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient

from src import app
from testing import get_test_db
from testing.card_effects.fixture_started_game import fixture_started_game, get_active_player_with_card
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


def test_lanzallamas(get_test_db, fixture_started_game):
    db = get_test_db
    client = TestClient(app)

    active_player, active_player_idx, response = get_active_player_with_card("Lanzallamas", client)

    order = response.json()['alive_players']
    target = order.pop(active_player_idx - 1)
    response = client.post(f'/games/playing/{active_player}?discard={False}&card_name={"Lanzallamas"}&target={target}')
    response = client.get(f'/games/playing/{active_player}')
    assert sorted(response.json()['alive_players']) == sorted(order)
