import pytest

@pytest.mark.unit_test
def test_access_homepage(client):
    response = client.get('/')
    output = response.status_code
    data = response.data.decode('UTF-8')
    expected = 200
    assert output == expected
    assert 'GUDLFT' in response.data.decode('UTF-8')

@pytest.mark.unit_test
def test_access_clubsSummary(client):
    response = client.get('/clubsSummary')
    assert response.status_code == 200
    assert 'Competition Name' in response.data.decode('UTF-8')

@pytest.mark.unit_test
def test_invalid_url(client):
    response = client.get('/GUDLFT')
    assert response.status_code == 404

@pytest.mark.unit_test
def test_logout(client):
    response = client.get('/logout')
    assert response.status_code == 302

@pytest.mark.unit_test
def test_valid_booking(client, book_context_1):
    competition, club = book_context_1
    response = client.get(f'/book/{competition}/{club}')
    assert response.status_code == 200

@pytest.mark.unit_test
def test_invalib_booking(client, book_context_2):
    competition, club = book_context_2
    response = client.get(f'/book/{competition}/{club}')
    assert response.status_code == 200


