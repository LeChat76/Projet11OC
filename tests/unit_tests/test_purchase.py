import pytest
from server import replace_data_files


@pytest.mark.unit_test
def test_reservation_of_places_greater_than_the_number_of_places_Remaining(client, purchase_context_1):
    """
    Test of purchase competition without enough competition places 
    Club 'Iron Temple' (remain 17 points) purchase 8 places in 'Fall Classic' competition where only 5 places remaining
    Result should be 'You booked more than available place in this competition!'
    """

    replace_data_files()
    response = client.post('purchasePlaces', data=purchase_context_1)
    assert response.status_code == 200
    assert 'You booked more than available place in this competition!' in response.data.decode('UTF-8')

@pytest.mark.unit_test
def test_purchase_competition_without_enough_club_point(client, purchase_context_2):
    """
    Test of purchase competition without enough club point 
    Club 'Simply Lift' (remain 1 points) purchase 3 places in 'Fall Classic' competition
    Result should be 'You have not enough point.'
    """
    replace_data_files()

    response = client.post('/purchasePlaces', data=purchase_context_2)
    assert response.status_code == 200
    assert 'You have not enough point.' in response.data.decode('UTF-8')

@pytest.mark.unit_test
def test_reservation_ok(client, purchase_context_3):
    """
    Test of purchase competition with valid entries
    Club 'Iron Temple' (remain 17 points) purchase 3 places in 'Fall Classic' competition where 5 places remaining
    Result must contain 'Great-booking complete!'
    """
    replace_data_files()
    response = client.post('/purchasePlaces', data=purchase_context_3)
    assert response.status_code == 200
    assert 'Great-booking complete!' in response.data.decode('UTF-8')

@pytest.mark.unit_test
def test_purchase_competition_of_more_than_12_points(client, purchase_context_4):
    """
    Test of purchase competition with valid entries
    Club 'Iron Temple' (remain 17 points) purchase 13 places in 'Test 12' competition where 25 places remaining
    Result must contain 'You can only purchase from 1 to 12 places.'
    """

    replace_data_files()
    response = client.post('/purchasePlaces', data=purchase_context_4)
    assert response.status_code == 200
    assert 'You can only purchase from 1 to 12 places.' in response.data.decode('UTF-8')

@pytest.mark.unit_test
def test_purchase_with_non_numeric_value(client, purchase_context_6):
    """
    Test of purchase competition with valid entries
    Club 'Iron Temple' purchase non numeric value
    Result must contain 'Thanks to use numeric value!'
    """
    replace_data_files()
    response = client.post('/purchasePlaces', data=purchase_context_6)
    assert response.status_code == 200
    assert 'Thanks to use numeric value!' in response.data.decode('UTF-8')


