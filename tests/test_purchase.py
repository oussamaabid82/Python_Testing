from . conftest import client


"""
/purchasePlaces
"""


def test_purchaseplaces_should_status_code_ok(client, first_club_fixture, firt_competition_past_fixture):
    response = client.post(
        '/purchasePlaces',
        data=dict(
            club=first_club_fixture['name'],
            competition=firt_competition_past_fixture['name'],
            places=3
        )
    )
    assert response.status_code == 200


def test_purchaseplaces_user_is_logged_in(client, first_club_fixture, firt_competition_past_fixture):
    login = client.post('/showSummary', data=dict(email=first_club_fixture['email']), follow_redirects=True)
    assert login.status_code == 200
    response = client.post(
        '/purchasePlaces',
        data=dict(
            club=first_club_fixture['name'],
            competition=firt_competition_past_fixture['name'],
            places=3
        )
    )
    assert response.status_code == 200
    data = response.data.decode()
    assert data.find('Welcome, ' + first_club_fixture['email']) != -1


def test_purchaseplaces_user_is_not_logged_in(client, first_club_fixture, firt_competition_past_fixture):
    response = client.post(
        '/purchasePlaces',
        data=dict(
            club=first_club_fixture['name'],
            competition=firt_competition_past_fixture['name'],
            places=3
        )
    )
    assert response.status_code == 200
    data = response.data.decode()
    assert data.find("You are not logged in") != -1


"""
ISSUE5 :
Changement du test à cause de l'implémentation du controle de la date des compétitions
Il n'est plus possible d'accéder à une compétition terminée
Modification :
    - changement de la ficture: firt_competition_past_fixture -> second_competition_post_fixture
    - Ajout d'un nouveau test si la compétition est terminée dans test_server_issue5.py
"""


def test_purchaseplaces_display_flash_message_after_buying_places_on_post_competition(
    client,
    first_club_fixture,
    second_competition_post_fixture
):
    login = client.post('/showSummary', data=dict(email=first_club_fixture['email']), follow_redirects=True)
    assert login.status_code == 200
    response = client.post(
        '/purchasePlaces',
        data=dict(
            club=first_club_fixture['name'],
            competition=second_competition_post_fixture['name'],
            places=3
        )
    )
    assert response.status_code == 200
    data = response.data.decode()
    assert data.find("Great-booking complete!") != -1


"""
Issue 2 : BUG: Clubs should not be able to use more than their points allowed
"""


def test_success_booking_places(client, first_club_fixture, second_competition_post_fixture):
    login = client.post('/showSummary', data=dict(email=first_club_fixture['email']), follow_redirects=True)
    assert login.status_code == 200
    response = client.post(
        '/purchasePlaces',
        data=dict(
            club=first_club_fixture['name'],
            competition=second_competition_post_fixture['name'],
            places=5
        )
    )
    assert response.status_code == 200
    data = response.data.decode()
    assert data.find("Great-booking complete!") != -1


def test_cant_take_more_than_possible_places(client, first_club_fixture, second_competition_post_fixture):
    login = client.post('/showSummary', data=dict(email=first_club_fixture['email']), follow_redirects=True)
    assert login.status_code == 200
    maximum_places = second_competition_post_fixture['numberOfPlaces']

    response = client.post(
        '/purchasePlaces',
        data=dict(
            club=first_club_fixture['name'],
            competition=second_competition_post_fixture['name'],
            places=int(maximum_places) + 1
        )
    )
    assert response.status_code == 200
    data = response.data.decode()
    assert data.find("Not enough point available.") != -1


def test_required_places_is_negative(client, first_club_fixture, second_competition_post_fixture):
    login = client.post('/showSummary', data=dict(email=first_club_fixture['email']), follow_redirects=True)
    assert login.status_code == 200
    response = client.post(
        '/purchasePlaces',
        data=dict(
            club=first_club_fixture['name'],
            competition=second_competition_post_fixture['name'],
            places=-1
        )
    )
    assert response.status_code == 200
    data = response.data.decode()
    assert data.find('Please, enter a positive number') != -1


"""
Issue 4 : BUG: Clubs shouldn't be able to book more than 12 places per competition
"""


"""
ISSUE5 :
Changement du test à cause de l'implémentation du controle de la date des compétitions
Il n'est plus possible d'accéder à une compétition terminée
Modification :
    - changement de la ficture: firt_competition_past_fixture -> second_competition_post_fixture
"""


def test_cant_take_more_than_twelve_places(client, forth_club_fixture, second_competition_post_fixture):
    login = client.post('/showSummary', data=dict(email=forth_club_fixture['email']), follow_redirects=True)
    assert login.status_code == 200

    response = client.post(
        '/purchasePlaces',
        data=dict(
            club=forth_club_fixture['name'],
            competition=second_competition_post_fixture['name'],
            places=13
        )
    )
    assert response.status_code == 200
    data = response.data.decode()
    assert data.find("You can order maximum 12 places.") != -1


def test_cant_take_more_than_twelve_places_with_many_tries(
    client,
    forth_club_fixture,
    second_competition_post_fixture
):
    login = client.post('/showSummary', data=dict(email=forth_club_fixture['email']), follow_redirects=True)
    assert login.status_code == 200

    response = client.post(
        '/purchasePlaces',
        data=dict(
            club=forth_club_fixture['name'],
            competition=second_competition_post_fixture['name'],
            places=10
        )
    )

    response = client.post(
        '/purchasePlaces',
        data=dict(
            club=forth_club_fixture['name'],
            competition=second_competition_post_fixture['name'],
            places=3
        )
    )
    assert response.status_code == 200
    data = response.data.decode()

    assert data.find("You can order maximum 12 places.") != -1


"""
ISSUE 5 : BUG: Booking places in past competitions
"""


def test_cannot_take_places_from_past_competition(
    client,
    first_club_fixture,
    firt_competition_past_fixture
):
    login = client.post('/showSummary', data=dict(email=first_club_fixture['email']), follow_redirects=True)
    assert login.status_code == 200
    response = client.post(
        '/purchasePlaces',
        data=dict(
            club=first_club_fixture['name'],
            competition=firt_competition_past_fixture['name'],
            places=3
        )
    )
    assert response.status_code == 200
    data = response.data.decode()
    assert data.find("This competition is no more available.") != -1


def test_can_take_places_from_post_competition(client, first_club_fixture, second_competition_post_fixture):
    login = client.post('/showSummary', data=dict(email=first_club_fixture['email']), follow_redirects=True)
    assert login.status_code == 200
    response = client.post(
        '/purchasePlaces',
        data=dict(
            club=first_club_fixture['name'],
            competition=second_competition_post_fixture['name'],
            places=3
        )
    )

    assert response.status_code == 200
    data = response.data.decode()
    assert data.find('Great-booking complete!') != -1
