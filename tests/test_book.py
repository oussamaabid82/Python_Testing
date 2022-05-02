from . conftest import client


"""
/book/<competition>/<club>
"""


def test_book_should_status_code_ok(client, first_club_fixture, firt_competition_past_fixture):
    login = client.post('/showSummary', data=dict(email=first_club_fixture['email']), follow_redirects=True)
    assert login.status_code == 200
    response = client.get(f"/book/{firt_competition_past_fixture['name']}/{first_club_fixture['name']}")
    assert response.status_code == 200


def test_book_user_is_logged_in(client, first_club_fixture, firt_competition_past_fixture):
    login = client.post('/showSummary', data=dict(email=first_club_fixture['email']), follow_redirects=True)
    assert login.status_code == 200
    response = client.get(f"/book/{firt_competition_past_fixture['name']}/{first_club_fixture['name']}")
    data = response.data.decode()
    assert response.status_code == 200
    assert data.find(firt_competition_past_fixture['name']) != -1


def test_book_user_is_not_logged_in(client, first_club_fixture, firt_competition_past_fixture):
    response = client.get(f"/book/{firt_competition_past_fixture['name']}/{first_club_fixture['name']}")
    data = response.data.decode()
    assert response.status_code == 200
    assert data.find("You are not logged in") != -1
