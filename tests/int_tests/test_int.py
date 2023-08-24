import pytest
from server import replace_data_files, foundClub, foundCompetition, loadClubs, loadCompetitions


replace_data_files()
clubPointsBeforePurchase = int(foundClub('Iron Temple')['points'])
print('\nclubPointsBeforePurchase1', clubPointsBeforePurchase)

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
def test_purchasing_more_than_12_places_and_balance_keep_unchanged(client, purchase_context_4):
    # purchase_context_4 = 'Iron Temple' purchase 13 places for 'Test 12' competition
    club = purchase_context_4['club']
    clubPointsBeforePurchase = int(foundClub(club)['points'])
    competition = purchase_context_4['competition']
    competitionNumberOfPlacesBeforePurchase = foundCompetition(competition)['numberOfPlaces']
    response = client.post('purchasePlaces', data=purchase_context_4)
    clubs_list = loadClubs()
    competitions_list = loadCompetitions()
    for element in clubs_list:
        if element['name'] == club:
            clubPointsAfterPurchase = element['points']
            break
    for element in competitions_list:
        if element['name'] == competition:
            competitionNmberOfPlacesAfterPurchase = element['numberOfPlaces']
            break
    assert response.status_code == 200
    assert clubPointsBeforePurchase == clubPointsAfterPurchase
    assert competitionNumberOfPlacesBeforePurchase == competitionNmberOfPlacesAfterPurchase

@pytest.mark.int_test
def test_purchasing_and_balance_update_checking(client, purchase_context_3):
    # purchase_context_3 = Iron Temple purchase 3 places for Fall Classic competition where remaing 5 places
    club = purchase_context_3['club']
    clubPointsBeforePurchase = int(foundClub(club)['points'])
    print('\nclubPointsBeforePurchase1', clubPointsBeforePurchase)
    nbPlacesToPurchase = int(purchase_context_3['places'])
    competition = purchase_context_3['competition']
    competitionNumberOfPlacesBeforePurchase = int(foundCompetition(competition)['numberOfPlaces'])
    response = client.post('purchasePlaces', data=purchase_context_3)
    clubs_list = loadClubs()
    competitions_list = loadCompetitions()
    for element in clubs_list:
        if element['name'] == club:
            clubPointsAfterPurchase = element['points']
            break
    for element in competitions_list:
        if element['name'] == competition:
            competitionNmberOfPlacesAfterPurchase = element['numberOfPlaces']
            break
    assert response.status_code == 200
    assert clubPointsBeforePurchase - nbPlacesToPurchase == clubPointsAfterPurchase
    assert competitionNumberOfPlacesBeforePurchase - nbPlacesToPurchase == competitionNmberOfPlacesAfterPurchase
