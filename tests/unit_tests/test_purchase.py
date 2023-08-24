from unittest.mock import patch
from server import replace_data_files


replace_data_files()

def test_reservation_of_places_greater_than_the_number_of_places_Remaining(client, purchase_context_1):
    """
    Test of purchase competition without enough competition places 
    Club 'Iron Temple' (remain 17 points) purchase 8 places in 'Fall Classic' competition where only 5 places remaining
    Result should be 'You booked more than available place in this competition!'
    """

    response = client.post('purchasePlaces', data=purchase_context_1)
    assert response.status_code == 200
    assert 'You booked more than available place in this competition!' in response.data.decode('UTF-8')

def test_purchase_competition_without_enough_club_point(client, purchase_context_2):
    """
    Test of purchase competition without enough club point 
    Club 'Simply Lift' (remain 1 points) purchase 3 places in 'Fall Classic' competition
    Result should be 'You have not enough point.'
    """

    response = client.post('/purchasePlaces', data=purchase_context_2)
    assert response.status_code == 200
    assert 'You have not enough point.' in response.data.decode('UTF-8')

@patch('server.write_data_to_json') # to prevent recording result in production's files, mocking write_data_to_json function with blank (=pass)
def test_reservation_ok(_, client, purchase_context_3):
    """
    Test of purchase competition with valid entries
    Club 'Iron Temple' (remain 17 points) purchase 3 places in 'Fall Classic' competition where 5 places remaining
    Result must contain 'Great-booking complete!'
    """

    response = client.post('/purchasePlaces', data=purchase_context_3)
    assert response.status_code == 200
    assert 'Great-booking complete!' in response.data.decode('UTF-8')

def test_purchase_competition_of_more_than_12_points(client, purchase_context_4):
    """
    Test of purchase competition with valid entries
    Club 'Iron Temple' (remain 17 points) purchase 13 places in 'Test 12' competition where 25 places remaining
    Result must contain 'You can only purchase from 1 to 12 places.'
    """

    response = client.post('/purchasePlaces', data=purchase_context_4)
    assert response.status_code == 200
    assert 'You can only purchase from 1 to 12 places.' in response.data.decode('UTF-8')

def test_purchase_dated_competition(client, purchase_context_5):
    """
    Test of purchase competition with valid entries
    Club 'Iron Temple' (remain 17 points) purchase 5 places in 'Spring Festival' competition
    Result must contain '"This competition is closed!'
    """

    response = client.post('/purchasePlaces', data=purchase_context_5)
    assert response.status_code == 200
    assert 'This competition is closed!' in response.data.decode('UTF-8')
    
