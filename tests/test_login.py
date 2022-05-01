from . conftest import client
from .. server import loadFile


def test_home_should_status_code_ok(client):
    response = client.get('/')
    assert response.status_code == 200
    data = response.data.decode()
    assert data.find('Welcome to the GUDLFT Registration Portal!') != -1


"""
Issue 1 : ERROR: Entering a unknown email crashes the app
/book/<competition>/<club>
"""


def test_user_invalid_email(client):
    response = client.post('/showSummary', data=dict(email='unknown@gmail.com'))
    assert response.status_code == 403


def test_user_invalid_email_display_message(client):
    response = client.post('/showSummary', data=dict(email='unknown@gmail.com'))
    assert response.status_code == 403
    data = response.data.decode()
    assert data.find('Sorry, that email is not found.')

def test_showsummary_without_login(client):
    response = client.get('/showSummary', follow_redirects=True)
    assert response.status_code == 405


def test_logout(client, first_club_fixture):
    login = client.post('/showSummary', data=dict(email=first_club_fixture['email']), follow_redirects=True)
    assert login.status_code == 200
    response = client.get('/logout', follow_redirects=True)
    data = response.data.decode()
    assert data.find('Welcome to the GUDLFT Registration Portal!') != -1
