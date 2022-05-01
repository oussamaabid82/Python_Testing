import pytest

from ..server import create_app


@pytest.fixture
def client():
    app = create_app({'TESTING': True})
    with app.test_client() as client:
        yield client


"""
Club data
"""

@pytest.fixture
def first_club_fixture():
    club_data = {
        "name": "test1 GUDLFT",
        "email": "test1_email@gudlft.com",
        "points": "20"
    }
    return club_data


"""
competition data
assuming past_ is first observation and post_ is second
"""

@pytest.fixture
def firt_competition_past_fixture():
    competition_data = {
        "name": "competition test1",
        "date": "2020-03-27 10:00:00",
        "numberOfPlaces": "25"
    }
    return competition_data

