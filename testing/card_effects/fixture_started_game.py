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

nickname1 = 'andy'
nickname2 = 'pepe'
nickname3 = 'carla'
nickname4 = 'juan'
game_name = 'Partida de Andy'
active_player = None

@pytest.fixture
def fixture_started_game():
    client = TestClient(app)

    response = client.post(f'/users?nickname={nickname1}')
    response = client.post(f'/users?nickname={nickname2}')
    response = client.post(f'/users?nickname={nickname3}')
    response = client.post(f'/users?nickname={nickname4}')

    body = {"game_name": game_name, "min_players": 4, "max_players": 12, "creator": nickname1}
    response = client.post(url="/games", json=body)

    response = client.patch(f'/users/{nickname1}?game_name={game_name}')
    response = client.patch(f'/users/{nickname2}?game_name={game_name}')
    response = client.patch(f'/users/{nickname3}?game_name={game_name}')
    response = client.patch(f'/users/{nickname4}?game_name={game_name}')

    response = client.post(f'/games/{nickname1}')

    global active_player
    response = client.get(f'/games/playing/{nickname1}')
    active_player = response.json()['active_player']


def get_active_player_with_card(card_name, client):
    active_player = None
    active_player_has_card = False
    while not active_player_has_card:
        response = client.get(f'/games/playing/{nickname1}')
        active_player = response.json()['active_player']
        response = client.get(f'/games/playing/{active_player}')
        active_player_has_card = (card_name in [card['name'] for card in response.json()['player_hand']])
        if not active_player_has_card:
            card_name = None
            any((card_name := card['name']) not in ["La Cosa", "¡Infectado!"] for card in response.json()['player_hand'])
            response = client.post(f'/games/playing/{active_player}?discard={True}&card_name={card_name}')

    active_player_idx = None
    order = response.json()['alive_players']
    for i in range(len(order)):
        if order[i] == active_player:
            active_player_idx = i
            break

    return active_player, active_player_idx, response
