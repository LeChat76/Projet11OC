import json
from flask import Flask,render_template,request,redirect,flash,url_for
from datetime import datetime


def write_data_to_json(filename, data):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)

def loadClubs():
    with open('clubs.json') as c:
         listOfClubs = json.load(c)['clubs']
         return listOfClubs


def loadCompetitions():
    with open('competitions.json') as comps:
         listOfCompetitions = json.load(comps)['competitions']
         return listOfCompetitions

def searchClub(email):
    result = [club for club in clubs if club['email'] == email]
    if result:
        return result[0]
    else:
        return None

def foundClub(club_name):
    club = [c for c in clubs if c['name'] == club_name]
    if len(club) > 0:
        return club[0]
    else:
        return None

def foundCompetition(competition_name):
    competition = [c for c in competitions if c['name'] == competition_name]
    if len(competition) > 0:
        return competition[0]
    else:
        return None

app = Flask(__name__)
app.secret_key = 'something_special'

competitions = loadCompetitions()
clubs = loadClubs()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/showSummary',methods=['POST'])
def showSummary():
    club = searchClub(request.form['email'])
    if club:
        return render_template('welcome.html',club=club,competitions=competitions)
    else:
        error_message = "Club not found for the provided email."
        flash(error_message)
        return redirect(url_for('index'))

@app.route('/book/<competition>/<club>')
def book(competition,club):
    club = foundClub(club)
    competition = foundCompetition(competition)
    if club and competition:
        return render_template('booking.html',club=club,competition=competition)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, competitions=competitions)

@app.route('/purchasePlaces',methods=['POST'])
def purchasePlaces():
    competition = foundCompetition(request.form['competition'])
    competition_date = datetime.strptime(competition['date'], '%Y-%m-%d %H:%M:%S')
    competition_name = competition['name']
    competition_numberOfPlaces = int(competition['numberOfPlaces'])
    club = foundClub(request.form['club'])
    club_points = int(club['points'])
    club_name = club['name']
    placesRequired = int(request.form['places'])
    if placesRequired > club_points:
        error_message = "You have not enough point."
        flash(error_message)
        return render_template('welcome.html', club=club, competitions=competitions)
    elif placesRequired > 12 or placesRequired < 1:
        error_message = "You can only purchase from 1 to 12 places."
        flash(error_message)
        return render_template('welcome.html', club=club, competitions=competitions)
    elif datetime.now() > competition_date:
        error_message = "This competition is closed!"
        flash(error_message)
        return render_template('welcome.html', club=club, competitions=competitions)
    elif placesRequired > competition_numberOfPlaces:
        error_message = "You booked more than available place in this competition!"
        flash(error_message)
        return render_template('welcome.html', club=club, competitions=competitions)
    club['points'] = club_points - placesRequired
    competition['numberOfPlaces'] = int(competition['numberOfPlaces'])-placesRequired
    write_data_to_json('clubs.json', {'clubs': clubs})
    write_data_to_json('competitions.json', {'competitions': competitions})
    flash_message = f'Great-booking complete! You had booked {placesRequired} place(s) for competition "{competition_name}".'
    flash(flash_message)
    return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/clubsSummary')
def clubsSummary():
    return render_template('clubsSummary.html', competitions=competitions)


@app.route('/logout')
def logout():
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)