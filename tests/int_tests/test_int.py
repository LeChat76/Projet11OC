import pytest
from utils import loadClubFromFile, loadCompetitionFromFile, init_database

@pytest.mark.int_test
def test_login_and_logout(client):
    response = client.post('/showSummary', data={'email': 'admin@irontemple.com'})
    assert response.status_code == 200
    assert 'Welcome, admin@irontemple.com ' in response.data.decode()
    response = client.get('/logout')
    assert response.status_code == 302
    assert response.headers['Location'] == '/'

@pytest.mark.int_test
def test_access_clubsSummary(client):
    response = client.get('/clubsSummary')
    assert response.status_code == 200
    assert 'Competition Name' in response.data.decode()

@pytest.mark.int_test
def test_purchasing_and_balance_update_checking(client, purchase_context_3):
    # purchase_context_3 = Iron Temple purchase 3 places for Fall Classic competition where remaing 5 places
    init_database()
    club = loadClubFromFile(purchase_context_3['club'])
    print('\nclubBefore', club)
    competition = loadCompetitionFromFile(purchase_context_3['competition'])
    print('competitionBefore', competition)
    nbPlacesToPurchase = int(purchase_context_3['places'])
    print('nbPlacesToPurchase', nbPlacesToPurchase)
    clubPointsBeforePurchase = club['points']
    print('clubPointsBeforePurchase', clubPointsBeforePurchase)
    competitionNumberOfPlacesBeforePurchase = competition['numberOfPlaces']
    print('competitionNumberOfPlacesBeforePurchase', competitionNumberOfPlacesBeforePurchase)
    response = client.post('purchasePlaces', data=purchase_context_3)
    club = loadClubFromFile(purchase_context_3['club'])
    print('clubAfter', club)
    competition = loadCompetitionFromFile(purchase_context_3['competition'])
    print('competitionAfter', competition)
    clubPointsAfterPurchase = club['points']
    print('clubPointsAfterPurchase', clubPointsAfterPurchase)
    competitionNmberOfPlacesAfterPurchase = competition['numberOfPlaces']
    print('competitionNmberOfPlacesAfterPurchase', competitionNmberOfPlacesAfterPurchase)
    assert response.status_code == 200
    assert clubPointsBeforePurchase - nbPlacesToPurchase == clubPointsAfterPurchase
    assert competitionNumberOfPlacesBeforePurchase - nbPlacesToPurchase == competitionNmberOfPlacesAfterPurchase
    assert 'Great-booking complete!' in response.data.decode('UTF-8')

@pytest.mark.int_test
def test_purchasing_more_than_12_places_and_balance_keep_unchanged(client, purchase_context_4):
    # purchase_context_4 = 'Iron Temple' purchase 13 places for 'Test 12' competition
    init_database()
    club = loadClubFromFile(purchase_context_4['club'])
    competition = loadCompetitionFromFile(purchase_context_4['competition'])
    clubPointsBeforePurchase = club['points']
    competitionNumberOfPlacesBeforePurchase = competition['numberOfPlaces']
    response = client.post('purchasePlaces', data=purchase_context_4)
    club = loadClubFromFile(purchase_context_4['club'])
    competition = loadCompetitionFromFile(purchase_context_4['competition'])
    clubPointsAfterPurchase = club['points']
    competitionNmberOfPlacesAfterPurchase = competition['numberOfPlaces']
    assert response.status_code == 200
    assert clubPointsBeforePurchase == clubPointsAfterPurchase
    assert competitionNumberOfPlacesBeforePurchase == competitionNmberOfPlacesAfterPurchase
    assert 'You can only purchase from 1 to 12 places.' in response.data.decode('UTF-8')
