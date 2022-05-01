from . conftest import client



"""
Issue 2 : TEST BUG Clubs should not be able to use more than their points allowed
/book/<competition>/<club>
"""

def test_success_booking_places(client, first_club_fixture, firt_competition_past_fixture):
    login = client.post('/showSummary', data=dict(email=first_club_fixture['email']), follow_redirects=True)
    print(login)
    assert login.status_code == 200
    response = client.post(
        '/purchasePlaces',
        data=dict(
            club=first_club_fixture['name'],
            competition=firt_competition_past_fixture['name'],
            places=5
        )
    )
    assert response.status_code == 200
    data = response.data.decode()
    assert data.find("Great-booking complete!") != -1


def test_cant_take_more_than_possible_places(client, first_club_fixture, firt_competition_past_fixture):
    login = client.post('/showSummary', data=dict(email=first_club_fixture['email']), follow_redirects=True)
    assert login.status_code == 200
    maximum_places = firt_competition_past_fixture['numberOfPlaces']

    response = client.post(
        '/purchasePlaces',
        data=dict(
            club=first_club_fixture['name'],
            competition=firt_competition_past_fixture['name'],
            places=int(maximum_places) + 1
        )
    )
    assert response.status_code == 200
    data = response.data.decode()
    assert data.find("Not enough point available.") != -1


def test_required_places_is_negative(client, first_club_fixture, firt_competition_past_fixture):
    login = client.post('/showSummary', data=dict(email=first_club_fixture['email']), follow_redirects=True)
    assert login.status_code == 200
    response = client.post(
        '/purchasePlaces',
        data=dict(
            club=first_club_fixture['name'],
            competition=firt_competition_past_fixture['name'],
            places=-1
        )
    )
    assert response.status_code == 200
    data = response.data.decode()
    assert data.find('Please, enter a positive number') != -1
    