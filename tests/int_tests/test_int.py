import pytest
import shutil
# import sys
# import os
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from server import replace_data_files, foundClub, foundCompetition, loadClubs, loadCompetitions


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
    replace_data_files()
    club = foundClub(purchase_context_3['club'])
    clubPointsBeforePurchase = club['points']
    nbPlacesToPurchase = int(purchase_context_3['places'])
    competition = foundCompetition(purchase_context_3['competition'])
    competitionNumberOfPlacesBeforePurchase = competition['numberOfPlaces']
    response = client.post('purchasePlaces', data=purchase_context_3)
    clubPointsAfterPurchase = (foundClub(purchase_context_3['club']))['points']
    competitionNmberOfPlacesAfterPurchase = (foundCompetition(purchase_context_3['competition']))['numberOfPlaces']
    assert response.status_code == 200
    assert clubPointsBeforePurchase - nbPlacesToPurchase == clubPointsAfterPurchase
    assert competitionNumberOfPlacesBeforePurchase - nbPlacesToPurchase == competitionNmberOfPlacesAfterPurchase

@pytest.mark.int_test
def test_purchasing_more_than_12_places_and_balance_keep_unchanged(client, purchase_context_4):
    # purchase_context_4 = 'Iron Temple' purchase 13 places for 'Test 12' competition
    replace_data_files()
    club = foundClub(purchase_context_4['club'])
    clubPointsBeforePurchase = club['points']
    competition = foundCompetition(purchase_context_4['competition'])
    competitionNumberOfPlacesBeforePurchase = competition['numberOfPlaces']
    response = client.post('purchasePlaces', data=purchase_context_4)
    clubPointsAfterPurchase = (foundClub(purchase_context_4['club']))['points']
    competitionNmberOfPlacesAfterPurchase = (foundCompetition(purchase_context_4['competition']))['numberOfPlaces']
    assert response.status_code == 200
    assert clubPointsBeforePurchase == clubPointsAfterPurchase
    assert competitionNumberOfPlacesBeforePurchase == competitionNmberOfPlacesAfterPurchase