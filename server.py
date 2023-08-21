import json
from flask import Flask,render_template,request,redirect,flash,url_for
from datetime import datetime

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
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]
    if foundClub and foundCompetition:
        return render_template('booking.html',club=foundClub,competition=foundCompetition)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/purchasePlaces',methods=['POST'])
def purchasePlaces():
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    competition_date = datetime.strptime(competition['date'], '%Y-%m-%d %H:%M:%S')
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    club_points = int(club['points'])
    placesRequired = int(request.form['places'])
    if placesRequired > club_points:
        error_message = "You have not enough point."
        flash(error_message)
        return redirect(url_for('book', club=club['name'], competition=competition['name']))
    elif placesRequired > 12 or placesRequired < 1:
        error_message = "You can only purchase from 1 to 12 places."
        flash(error_message)
        return redirect(url_for('book', club=club['name'], competition=competition['name']))
    elif datetime.now() > competition_date:
        error_message = "This competition is closed!"
        flash(error_message)
        return redirect(url_for('book', club=club['name'], competition=competition['name']))
    club['points'] = str((int(club['points']) - placesRequired))
    competition['numberOfPlaces'] = int(competition['numberOfPlaces'])-placesRequired
    flash('Great-booking complete!')
    return render_template('welcome.html', club=club, competitions=competitions)


# TODO: Add route for points display


@app.route('/logout')
def logout():
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)