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
    print(response)
    data = response.data.decode()
    assert response.status_code == 200
    assert data.find("You are not logged in") != -1


"""
ISSUE 5 : BUG: Booking places in past competitions
"""


def test_cannot_access_to_past_competition(client, first_club_fixture, firt_competition_past_fixture):
    login = client.post('/showSummary', data=dict(email=first_club_fixture['email']), follow_redirects=True)
    assert login.status_code == 200
    response = client.get(f"/book/{firt_competition_past_fixture['name']}/{first_club_fixture['name']}")
    assert response.status_code == 200
    data = response.data.decode()
    assert data.find("This competition is closed.") != -1


def test_can_access_to_post_competition(client, first_club_fixture, second_competition_post_fixture):
    login = client.post('/showSummary', data=dict(email=first_club_fixture['email']), follow_redirects=True)
    assert login.status_code == 200
    response = client.get(f"/book/{second_competition_post_fixture['name']}/{first_club_fixture['name']}")
    assert response.status_code == 200
    

"""
ISSUE 6 : BUG: Point updates are not reflected
"""


def test_cant_access_booking_if_no_point(client, third_club_fixture, second_competition_post_fixture):
    login = client.post('/showSummary', data=dict(email=third_club_fixture['email']), follow_redirects=True)
    assert login.status_code == 200
    booking = client.post(
        '/purchasePlaces',
        data=dict(
            club=third_club_fixture['name'],
            competition=second_competition_post_fixture['name'],
            places=1
        )
    )
    assert booking.status_code == 200
    response = client.get(f"/book/{second_competition_post_fixture['name']}/{third_club_fixture['name']}")
    assert response.status_code == 200
    data = response.data.decode()
    print(data)
    assert data.find('Your cannot book places anymore. You are out of points') != -1