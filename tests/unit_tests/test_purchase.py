import pytest
from utils import init_database, loadClubFromFile, loadCompetitionFromFile


@pytest.mark.unit_test
def test_reservation_of_places_greater_than_the_number_of_places_Remaining(client, purchase_context_1):
    """
    Test of purchase competition without enough competition places 
    Club 'Iron Temple' (remain 17 points) purchase 8 places in 'Fall Classic' competition where only 5 places remaining
    Result should be 'You booked more than available place in this competition!' and club points and number of places available of the competition must remain the same
    """

    init_database()
    clubPointsBeforePurchase = loadClubFromFile(purchase_context_1['club'])['points']
    competitionPointsBeforePurchase = loadCompetitionFromFile(purchase_context_1['competition'])['numberOfPlaces']
    response = client.post('purchasePlaces', data=purchase_context_1)
    clubPointsAferPurchase = loadClubFromFile(purchase_context_1['club'])['points']
    competitionPointsAfterPurchase = loadCompetitionFromFile(purchase_context_1['competition'])['numberOfPlaces']
    assert response.status_code == 200
    assert clubPointsBeforePurchase == clubPointsAferPurchase
    assert competitionPointsBeforePurchase == competitionPointsAfterPurchase
    assert 'You booked more than available place in this competition!' in response.data.decode('UTF-8')


@pytest.mark.unit_test
def test_purchase_competition_without_enough_club_point(client, purchase_context_2):
    """
    Test of purchase competition without enough club point 
    Club 'Simply Lift' (remain 1 points) purchase 3 places in 'Fall Classic' competition
    Result should be 'You have not enough point.' and club points and number of places available of the competition must remain the same
    """
    init_database()
    clubPointsBeforePurchase = loadClubFromFile(purchase_context_2['club'])['points']
    competitionPointsBeforePurchase = loadCompetitionFromFile(purchase_context_2['competition'])['numberOfPlaces']
    response = client.post('/purchasePlaces', data=purchase_context_2)
    clubPointsAferPurchase = loadClubFromFile(purchase_context_2['club'])['points']
    competitionPointsAfterPurchase = loadCompetitionFromFile(purchase_context_2['competition'])['numberOfPlaces']
    assert response.status_code == 200
    assert clubPointsBeforePurchase == clubPointsAferPurchase
    assert competitionPointsBeforePurchase == competitionPointsAfterPurchase
    assert 'You have not enough point.' in response.data.decode('UTF-8')

@pytest.mark.unit_test
def test_reservation_ok(client, purchase_context_3):
    """
    Test of purchase competition with valid entries
    Club 'Iron Temple' (remain 17 points) purchase 3 places in 'Fall Classic' competition where 5 places remaining
    Result must contain 'Great-booking complete!' and club points and number of places available of the competition must must be updated in json files
    """
    init_database()
    clubPointsBeforePurchase = loadClubFromFile(purchase_context_3['club'])['points']
    competitionPointsBeforePurchase = loadCompetitionFromFile(purchase_context_3['competition'])['numberOfPlaces']
    pointsPurchased =purchase_context_3['places']
    response = client.post('/purchasePlaces', data=purchase_context_3)
    clubPointsAferPurchase = loadClubFromFile(purchase_context_3['club'])['points']
    competitionPointsAfterPurchase = loadCompetitionFromFile(purchase_context_3['competition'])['numberOfPlaces']
    assert response.status_code == 200
    assert clubPointsAferPurchase == clubPointsBeforePurchase - pointsPurchased
    assert competitionPointsAfterPurchase == competitionPointsBeforePurchase - pointsPurchased
    assert 'Great-booking complete!' in response.data.decode('UTF-8')

@pytest.mark.unit_test
def test_purchase_competition_of_more_than_12_points(client, purchase_context_4):
    """
    Test of purchase competition with valid entries
    Club 'Iron Temple' (remain 17 points) purchase 13 places in 'Test 12' competition where 25 places remaining
    Result must contain 'You can only purchase from 1 to 12 places.'
    """

    init_database()
    clubPointsBeforePurchase = loadClubFromFile(purchase_context_4['club'])['points']
    competitionPointsBeforePurchase = loadCompetitionFromFile(purchase_context_4['competition'])['numberOfPlaces']
    response = client.post('/purchasePlaces', data=purchase_context_4)
    clubPointsAferPurchase = loadClubFromFile(purchase_context_4['club'])['points']
    competitionPointsAfterPurchase = loadCompetitionFromFile(purchase_context_4['competition'])['numberOfPlaces']
    assert response.status_code == 200
    assert clubPointsBeforePurchase == clubPointsAferPurchase
    assert competitionPointsBeforePurchase == competitionPointsAfterPurchase
    assert 'You can only purchase from 1 to 12 places.' in response.data.decode('UTF-8')

@pytest.mark.unit_test
def test_purchase_dated_competition_of_more_than_12_points(client, purchase_context_5):
    """
    Test of purchase competition with valid entries
    Club 'Iron Temple' (remain 17 points) purchase 13 places in 'Spring Festival' competition where 25 places remaining
    Result must contain 'This competition is closed!'
    """

    init_database()
    clubPointsBeforePurchase = loadClubFromFile(purchase_context_5['club'])['points']
    competitionPointsBeforePurchase = loadCompetitionFromFile(purchase_context_5['competition'])['numberOfPlaces']
    response = client.post('/purchasePlaces', data=purchase_context_5)
    clubPointsAferPurchase = loadClubFromFile(purchase_context_5['club'])['points']
    competitionPointsAfterPurchase = loadCompetitionFromFile(purchase_context_5['competition'])['numberOfPlaces']
    assert response.status_code == 200
    assert clubPointsBeforePurchase == clubPointsAferPurchase
    assert competitionPointsBeforePurchase == competitionPointsAfterPurchase
    assert 'This competition is closed!' in response.data.decode('UTF-8')

@pytest.mark.unit_test
def test_purchase_with_non_numeric_value(client, purchase_context_6):
    """
    Test of purchase competition with valid entries
    Club 'Iron Temple' purchase non numeric value
    Result must contain 'Thanks to use numeric value!'
    """
    init_database()
    response = client.post('/purchasePlaces', data=purchase_context_6)
    assert response.status_code == 200
    assert 'Thanks to use numeric value!' in response.data.decode('UTF-8')
