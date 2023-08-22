from unittest.mock import patch
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import server

@patch('server.write_data_to_json') # to prevent recording result in production's files, mocking write_data_to_json function with blank (=pass)
def test_reservation_of_places_greater_than_the_number_of_places_Remaining(_, client, clubs, competitions, purchase_context_1):
    """
    Test of purchase competition without enough competition places 
    Club 'Iron Temple' (remain 17 points) purchase 8 places in 'Fall Classic' competition where only 5 places remaining
    Result should be 'You booked more than available place in this competition!'
    """

    server.competitions = competitions
    server.clubs = clubs
    response = client.post('purchasePlaces', data=purchase_context_1)
    with client.session_transaction() as session:
        flashed_messages = session.get('_flashes', [])[0][1] if '_flashes' in session and session['_flashes'] else None
    expected = 'You booked more than available place in this competition!'
    print("\nFLASH", flashed_messages)
    print("EXPECTED2", expected)
    assert response.status_code == 302
    assert flashed_messages == expected

@patch('server.write_data_to_json') # to prevent recording result in production's files, mocking write_data_to_json function with blank (=pass)
def test_purchase_competition_without_enough_club_point(_, client, clubs, competitions, purchase_context_2):
    """
    Test of purchase competition without enough club point 
    Club 'Simply Lift' (remain 1 points) purchase 3 places in 'Fall Classic' competition
    Result should be 'You have not enough point.'
    """

    server.competitions = competitions
    server.clubs = clubs
    response = client.post('purchasePlaces', data=purchase_context_2)
    with client.session_transaction() as session:
        flashed_messages = session.get('_flashes', [])[0][1] if '_flashes' in session and session['_flashes'] else None
    assert response.status_code == 302
    assert flashed_messages == 'You have not enough point.'

@patch('server.write_data_to_json') # to prevent recording result in production's files, mocking write_data_to_json function with blank (=pass)
def test_reservation_ok(_, client, clubs, competitions, purchase_context_3):
    """
    Test of purchase competition with valid entries
    Club 'Iron Temple' (remain 17 points) purchase 3 places in 'Fall Classic' competition where 5 places remaining
    Result must contain None
    """

    server.competitions = competitions
    server.clubs = clubs
    response = client.post('purchasePlaces', data=purchase_context_3)
    with client.session_transaction() as session:
        flashed_messages = session.get('_flashes', [])[0][1] if '_flashes' in session and session['_flashes'] else None
    assert response.status_code == 200
    assert flashed_messages is None

@patch('server.write_data_to_json') # to prevent recording result in production's files, mocking write_data_to_json function with blank (=pass)
def test_purchase_competition_of_more_than_12_points(_, client, clubs, competitions, purchase_context_4):
    """
    Test of purchase competition with valid entries
    Club 'Iron Temple' (remain 17 points) purchase 13 places in 'Test 12' competition where 25 places remaining
    Result must contain 'You can only purchase from 1 to 12 places.'
    """

    server.competitions = competitions
    server.clubs = clubs
    response = client.post('purchasePlaces', data=purchase_context_4)
    with client.session_transaction() as session:
        flashed_messages = session.get('_flashes', [])[0][1] if '_flashes' in session and session['_flashes'] else None
    assert response.status_code == 302
    assert flashed_messages == 'You can only purchase from 1 to 12 places.'

@patch('server.write_data_to_json') # to prevent recording result in production's files, mocking write_data_to_json function with blank (=pass)
def test_purchase_dated_competition(_, client, clubs, competitions, purchase_context_5):
    """
    Test of purchase competition with valid entries
    Club 'Iron Temple' (remain 17 points) purchase 5 places in 'Spring Festival' competition
    Result must contain '"This competition is closed!'
    """

    server.competitions = competitions
    server.clubs = clubs
    response = client.post('purchasePlaces', data=purchase_context_5)
    with client.session_transaction() as session:
        flashed_messages = session.get('_flashes', [])[0][1] if '_flashes' in session and session['_flashes'] else None
    assert response.status_code == 302
    assert flashed_messages == 'This competition is closed!'
    
