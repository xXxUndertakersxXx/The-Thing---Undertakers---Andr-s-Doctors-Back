import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient

from testing import get_test_db
from src import app
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


def test_play_card(get_test_db):
    db = get_test_db
    client = TestClient(app)

    nickname1 = 'andy'
    response = client.post(f'/games/playing/{nickname1}?discard={True}&card_name={"Lanzallamas"}&target={"pepe"}')
    assert response.status_code == 404
    assert response.json()['detail'] == f"No existe un Usuario con nickname {nickname1}"

    response = client.post(f'/users?nickname={nickname1}')
    response = client.post(f'/games/playing/{nickname1}?discard={True}&card_name={"Lanzallamas"}&target={"pepe"}')
    assert response.status_code == 400
    assert response.json()['detail'] == f"Usuario {nickname1} no se encuentra en una Partida actualmente"

    game_name = "Partida de Andy"
    body = {"game_name": game_name, "min_players": 4, "max_players": 12, "creator": nickname1}
    response = client.post(url="/games", json=body)
    response = client.patch(f'/users/{nickname1}?game_name={game_name}')
    response = client.post(f'/games/playing/{nickname1}?discard={True}&card_name={"Lanzallamas"}&target={"pepe"}')
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

    active_player = None
    for user in response.json()['users']:
        if user['active']:
            active_player = user['nickname']
    inactive_player = nickname1 if active_player != nickname1 else nickname2
    active_player_card = None
    for card in response.json()['cards']:
        if card['owner'] == active_player:
            active_player_card = card['name']

    response = client.post(f'/games/playing/{inactive_player}?discard={True}&card_name={"Lanzallamas"}&target={"pepe"}')
    assert response.status_code == 400
    assert response.json()['detail'] == f"Usuario {inactive_player} no es el jugador activo"

    response = client.post(f'/games/playing/{active_player}?discard={True}&card_name={active_player_card}')
    assert response.status_code == 200
    assert response.json()['play_response'] == {}

    next_user = None
    new_active_player = None
    old_active_player = active_player
    for user in response.json()['users']:
        if user['active']:
            assert user['nickname'] != old_active_player
            new_active_player = user['nickname']
        if user['nickname'] == old_active_player:
            next_user = user['next_user']
    assert new_active_player == next_user

    old_active_player_card_count = 0
    new_active_player_card_count = 0
    for card in response.json()['cards']:
        if card['owner'] == old_active_player:
            old_active_player_card_count += 1
        if card['owner'] == new_active_player:
            new_active_player_card_count += 1
    assert old_active_player_card_count == 4
    assert new_active_player_card_count == 5
