import pytest


@pytest.mark.unit_test
def test_login_success(client):
    response = client.post('/showSummary', data={'email': 'john@simplylift.co'})
    assert response.status_code == 200
    assert 'Welcome, john@simplylift.co ' in response.data.decode('UTF-8')

@pytest.mark.unit_test
def test_login_unsuccess(client):
    response = client.post('/showSummary', data={'email': 'toto@titi.com'})
    assert response.status_code == 302
    assert 'Welcome, toto@titi.com ' not in response.data.decode('UTF-8')