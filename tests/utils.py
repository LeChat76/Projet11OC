import shutil, json


def init_database():
    shutil.copyfile('datas/clubs.json', 'clubs.json')
    shutil.copyfile('datas/competitions.json', 'competitions.json')

def loadClubFromFile(club_name):
    with open('clubs.json') as c:
        clubs = json.load(c)['clubs']
        club = [c for c in clubs if c['name'] == club_name]
        if len(club) > 0:
            return club[0]
        else:
            return None

def loadCompetitionFromFile(competition_name):
    with open('competitions.json') as comps:
        competitions = json.load(comps)['competitions']
        competition = [c for c in competitions if c['name'] == competition_name]
        if len(competition) > 0:
            return competition[0]
        else:
            return None