import pytest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from server import app


@pytest.fixture
def client():
    client = app.test_client()
    yield client

@pytest.fixture
def clubs():
    clubs = [{"name": "Simply Lift", "email": "john@simplylift.co", "points": "1"},
             {"name": "Iron Temple", "email": "admin@irontemple.com", "points": "17"},
             {"name": "She Lifts", "email": "kate@shelifts.co.uk", "points": "12"},]
    yield clubs

@pytest.fixture
def competitions():
    competitions =  [{"name": "Spring Festival", "date": "2020-03-27 10:00:00", "numberOfPlaces": "25"},
                     {"name": "Fall Classic", "date": "2027-10-22 13:30:00", "numberOfPlaces": "5"},
                     {"name": "Test 12", "date": "2027-10-22 13:30:00", "numberOfPlaces": "25"},]
    yield competitions

@pytest.fixture
def purchase_context_1():
    data = {'club': 'Iron Temple', 'competition': 'Fall Classic', 'places': 8}
    return data

@pytest.fixture
def purchase_context_2():
    data = {'club': 'Simply Lift', 'competition': 'Fall Classic', 'places': 3}
    return data

@pytest.fixture
def purchase_context_3():
    data = {'club': 'Iron Temple', 'competition': 'Fall Classic', 'places': 3}
    return data

@pytest.fixture
def purchase_context_4():
    data = {'club': 'Iron Temple', 'competition': 'Test 12', 'places': 13}
    return data

@pytest.fixture
def purchase_context_5():
    data = {'club': 'Iron Temple', 'competition': 'Spring Festival', 'places': 5}
    return data

@pytest.fixture
def book_context_1():
    competition = 'Fall Classic'
    club = 'Iron Temple'
    return competition, club

@pytest.fixture
def book_context_2():
    competition = 'Wall Classic'
    club = 'Gold Temple'
    return competition, club