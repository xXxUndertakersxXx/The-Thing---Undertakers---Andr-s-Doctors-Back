import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import Column, Boolean, Integer, String, Enum


__Base__ = declarative_base()


class UsersTable(__Base__):
    __tablename__ = 'users'

    nickname = Column(String(50), primary_key=True)
    game_name = Column(String(50))
    role = Column(Enum('The Thing', 'Infected', 'Human', name='role_enum'))
    alive = Column(Boolean)
    quarantine = Column(Boolean)
    active = Column(Boolean)
    next_user = Column(String(50))


class GamesTable(__Base__):
    __tablename__ = 'games'

    name = Column(String(50), primary_key=True)
    min_players = Column(Integer)
    max_players = Column(Integer)
    player_count = Column(Integer)
    phase = Column(Enum('Waiting', 'Playing', 'Finished', name='phase_enum'))


class CardsTable(__Base__):
    __tablename__ = 'cards'

    id = Column(Integer, primary_key=True)
    game_name = Column(String(50), index=True)
    name = Column(String(50))
    owner = Column(String(50))


class ShowedCardsTable(__Base__):
    __tablename__ = 'showed_cards'

    id = Column(Integer, primary_key=True)
    card_id = Column(Integer)
    owner = Column(String(50))
    viewer = Column(String(50))


load_dotenv(".env")
__URL_DATABASE__ = os.getenv("DATABASE_CONNECTION_STRING")
__engine__ = create_engine(__URL_DATABASE__)
__Base__.metadata.create_all(bind=__engine__)
__SessionLocal__ = sessionmaker(autocommit=False, autoflush=False, bind=__engine__)


def get_db():
    db = __SessionLocal__()
    try:
        yield db
    except:
        db.rollback()
        raise
    finally:
        db.close()
    db.commit()
