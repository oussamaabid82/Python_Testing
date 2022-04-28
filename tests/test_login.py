from tests.conftest import client


def test_home_should_status_code_ok(client):
   
    response = client.get('/')
    assert response.status_code == 200
   
"""
Issue 1 : ERROR: Entering a unknown email crashes the app

"""


def test_user_invalid_email(client):
    response = client.post('/showSummary', data=dict(email='unknown@gmail.com'))
    assert response.status_code == 403
    print(response)

def test_user_invalid_email_display_message(client):
    response = client.post('/showSummary', data=dict(email='unknown@gmail.com'))
    assert response.status_code == 403
    data = response.data.decode()
    assert data.find('Sorry, that email is not found.')

def test_showsummary_without_login(client):
    response = client.get('/showSummary', follow_redirects=True)
    assert response.status_code == 405