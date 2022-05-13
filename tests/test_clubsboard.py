from . conftest import client
from ..app import loadFile


def test_success_display_clubs_points(client, file_name_of_data_test):
    test_clubs = loadFile(file_name_of_data_test['TEST_DATA_CLUBS'])
    response = client.get('/clubsboard', data=dict(clubs=test_clubs))
    assert response.status_code == 200
    data = response.data.decode()
    print(data)
    assert data.find('<td>test1 GUDLFT</td>') != -1
    assert data.find('<td>20</td>') != -1
    assert data.find('<td>test2 GUDLFT</td>') != -1
    assert data.find('<td>20</td>') != -1
    assert data.find('<td>test3 GUDLFT</td>') != -1
    assert data.find('<td>3</td>') != -1
    assert data.find('<td>test4 GUDLFT</td>') != -1
    assert data.find('<td>40</td>') != -1
