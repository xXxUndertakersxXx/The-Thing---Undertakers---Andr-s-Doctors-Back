import sys
import pytest

sys.path.append('../')
from src.database import UsersTable, GamesTable, CardsTable, ShowedCardsTable, __SessionLocal__


@pytest.fixture
def get_test_db():
    db = __SessionLocal__()

    db.query(UsersTable).delete()
    db.query(GamesTable).delete()
    db.query(CardsTable).delete()
    db.query(ShowedCardsTable).delete()
    db.commit()

    try:
        yield db
    except:
        db.rollback()
    finally:
        db.query(UsersTable).delete()
        db.query(GamesTable).delete()
        db.query(CardsTable).delete()
        db.query(ShowedCardsTable).delete()
        db.commit()
        db.close()
