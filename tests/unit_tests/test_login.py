def test_login_success(client):
    response = client.post('/showSummary', data={'email': 'john@simplylift.co'})
    assert response.status_code == 200
    assert 'Welcome, john@simplylift.co ' in response.data.decode()

def test_login_unsuccess(client):
    response = client.post('/showSummary', data={'email': 'toto@titi.com'})
    with client.session_transaction() as session:
        flashed_messages = session.get('_flashes', [])[0][1] if '_flashes' in session and session['_flashes'] else None
    assert response.status_code == 302
    assert flashed_messages == 'Club not found for the provided email.'
    assert 'Welcome, toto@titi.com ' not in response.data.decode()