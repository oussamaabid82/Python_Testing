import json
from flask import Flask, render_template, request, redirect, flash, url_for, session

"""
Listing all data to read
"""


DATA_CLUBS = 'clubs'
DATA_COMPETITIONS = 'competitions'
TEST_DATA_CLUBS = 'features/test_clubs'
TEST_DATA_COMPETITIONS = 'features/test_competitions'


def loadFile(file_name):
    database_name = list(reversed(file_name.split('/')))
    with open(file_name + '.json') as file:
        data = json.load(file)[database_name[0]]
        return data


"""
Changed the building with 'def create_app'
"""


def create_app(config={}):

    app = Flask(__name__)
    app.config.from_object(config)

    # Set 'TESTING' to True when testing
    app.config.update(config)

    app.secret_key = 'something_special'

    # Changed the method to have the possibility to apply test on fake database
    if app.config['TESTING'] is True:
        competitions = loadFile(TEST_DATA_COMPETITIONS)
        clubs = loadFile(TEST_DATA_CLUBS)
    else:
        competitions = loadFile(DATA_COMPETITIONS)
        clubs = loadFile(DATA_CLUBS)

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/showSummary', methods=['POST'])
    def showSummary():
        # Issue 1 : ERROR entering a unknown email crashes the app
        try:
            club = [club for club in clubs if club['email'] == request.form['email']][0]
        except:
            return (render_template('index.html', error="Sorry, that email is not found."), 403)

        # Init user session to check if the user is logged in
        session['username'] = request.form['email']

        return render_template('welcome.html', club=club, competitions=competitions)

    @app.route('/book/<competition>/<club>')
    def book(competition, club):
        foundClub = [c for c in clubs if c['name'] == club][0]
        foundCompetition = [c for c in competitions if c['name'] == competition][0]
        if foundClub and foundCompetition:
            return render_template('booking.html',club=foundClub,competition=foundCompetition)
        else:
            flash("Something went wrong-please try again")
            return render_template('welcome.html', club=club, competitions=competitions)


    @app.route('/purchasePlaces', methods=['POST'])
    def purchasePlaces():
        if 'username' in session:

            competition = [c for c in competitions if c['name'] == request.form['competition']][0]
            club = [c for c in clubs if c['name'] == request.form['club']][0]
            placesRequired = int(request.form['places'])

            # ISSUE2 : BUG: Clubs should not be able to use more than their points allowed
            if (
                (int(placesRequired)*3) <= int(club['points'])
                and int(placesRequired) >= 0
                and int(placesRequired) <= int(competition['numberOfPlaces'])
            ):

                flash('Great-booking complete!')
                return render_template('welcome.html', club=club, competitions=competitions)

            else:
                # ISSUE2 : ajout d'un message en cas de nombre de place négatif
                if int(placesRequired) < 0:
                    flash('Please, enter a positive number')
                else:
                    flash("Not enough point available.")
                return render_template('booking.html', club=club, competition=competition)

        return 'You are not logged in'

    @app.route('/logout')
    def logout():
        session.pop('username', None)
        return redirect(url_for('index'))

    return app
