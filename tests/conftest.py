import pytest

from .. server import create_app


@pytest.fixture
def client():
    app = create_app({'TESTING': True})
    with app.test_client() as client:
        yield client


"""
File name of data used for tests
"""


@pytest.fixture
def file_name_of_data_test():
    file_name = {
        'TEST_DATA_CLUBS': 'features/test_clubs',
        'TEST_DATA_COMPETITIONS': 'features/test_competitions'
    }
    return file_name


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


@pytest.fixture
def second_club_fixture():
    club_data = {
        "name": "test2 GUDLFT",
        "email": "test2_email@gudlft.com",
        "points": "20"
    }
    return club_data


@pytest.fixture
def third_club_fixture():
    club_data = {
        "name": "test3 GUDLFT",
        "email": "test3_email@gudlft.com",
        "points": "3"
    }
    return club_data


@pytest.fixture
def forth_club_fixture():
    club_data = {
        "name": "test4 GUDLFT",
        "email": "test4_email@gudlft.com",
        "points": "40"
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


@pytest.fixture
def second_competition_post_fixture():
    competition_data = {
        "name": "competition test2",
        "date": "2024-10-22 13:30:00",
        "numberOfPlaces": "13"
    }
    return competition_data
