# test login, purchase, logout, display club summary
import pytest
from unittest.mock import patch
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import server


@pytest.mark.int_test
def test_access_homepage(client):
    response = client.get('/')
    assert response.status_code == 200
    assert 'GUDLFT' in response.data.decode()

@pytest.mark.int_test
def test_login(client):
    response = client.post('/showSummary', data={'email': 'admin@irontemple.com'})
    assert response.status_code == 200
    assert 'Welcome, admin@irontemple.com ' in response.data.decode()

@pytest.mark.int_test
@patch('server.write_data_to_json') # to prevent recording result in production's files, mocking write_data_to_json function with blank (=pass)
def test_purchasing(_, client, clubs, competitions, purchase_context_3):
    # Iron Temple purchase 3 places for Fall Classic competition
    server.competitions = competitions
    server.clubs = clubs
    clubCurrentPoints = int(clubs[1]['points'])
    competitionCurrentNumberOfPlaces = int(competitions[1]['numberOfPlaces'])
    response = client.post('purchasePlaces', data=purchase_context_3)
    assert response.status_code == 200
    assert clubCurrentPoints - 3 == int(server.clubs[1]['points'])
    assert competitionCurrentNumberOfPlaces - 3 == int(server.competitions[1]['numberOfPlaces'])

@pytest.mark.int_test
def test_logout(client):
    response = client.get('/logout')
    assert response.status_code == 302
    assert response.headers['Location'] == '/'

@pytest.mark.int_test
def test_access_clubsSummary(client):
    response = client.get('/clubsSummary')
    assert response.status_code == 200
    assert 'Competition Name' in response.data.decode()

