from datetime import datetime
import json
from flask import Flask, render_template, request, redirect, flash, url_for, session

"""
Listing all data to read
"""


DATA_CLUBS = 'clubs'
DATA_COMPETITIONS = 'competitions'
TEST_DATA_CLUBS = 'features/test_clubs'
TEST_DATA_COMPETITIONS = 'features/test_competitions'

# ISSUE4 : BUG: Clubs should not be able to use more than their points allowed
MAX_PURCHASE = 12

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
        if 'username' in session:
            foundClub = [c for c in clubs if c['name'] == club][0]
            foundCompetition = [c for c in competitions if c['name'] == competition][0]

            # ISSUE5 : Booking places in past competitions
            # Empeche l'utilisateur d'acceder à une compétition terminée

            USER_DATETIME = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            if foundCompetition['date'] < USER_DATETIME:
                flash("This competition is closed.")
                return render_template('welcome.html', club=foundClub, competitions=competitions)

            # ISSUE6 : Ajout d'une vérification des points du club
            if foundClub['points'] == 0:
                flash("Your cannot book places anymore. You are out of points")
                return render_template('welcome.html', club=foundClub, competitions=competitions)

            if foundClub and foundCompetition:
                return render_template('booking.html', club=foundClub, competition=foundCompetition)

            else:
                flash("Something went wrong-please try again")
                return render_template('welcome.html', club=club, competitions=competitions)
        return 'You are not logged in'

    @app.route('/purchasePlaces', methods=['POST'])
    def purchasePlaces():
        if 'username' in session:

            competition = [c for c in competitions if c['name'] == request.form['competition']][0]
            club = [c for c in clubs if c['name'] == request.form['club']][0]
            placesRequired = int(request.form['places'])

            # ISSUE5 : Booking places in past competitions
            # revérification des dates, si l'utilisateur s'est endormi et que minuit a passé...

            USER_DATETIME = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            if competition['date'] < USER_DATETIME:
                flash('This competition is no more available.')
                return render_template('welcome.html', club=club, competitions=competitions)

            # ISSUE3 : ajout d'une donnée pour le club. {'nom de la compétition': 'places déjà achetées'}
            # L'utilisateur peut acheter 12 places en plusieurs fois

            if str(competition['name']) not in club:
                club[str(competition['name'])] = 0

            # ISSUE2 : BUG: Clubs should not be able to use more than their points allowed
            if (
                (int(placesRequired)*3) <= int(club['points'])
                and int(placesRequired) >= 0
                and int(placesRequired) <= int(competition['numberOfPlaces'])
            ):

                # ISSUE4 : BUG: Clubs should not be able to use more than their points allowed
                if int(club[str(competition['name'])]) + int(placesRequired) > MAX_PURCHASE:
                    flash(f"You can order maximum {MAX_PURCHASE} places.")
                    return render_template('booking.html', club=club, competition=competition)

                competition['numberOfPlaces'] = int(competition['numberOfPlaces'])-placesRequired

                # Incrémente 1 à la nouvelle donnée pour le club {'nom de la compétition': 'places déjà achetées + 1'}
                # décompte le nombre de place des points du club
                club[str(competition['name'])] += int(placesRequired)

                # ISSUE6 : correctif déjà présent, le même que pour l'ISSUE 2 ?
                club['points'] = int(club['points']) - (int(placesRequired)*3)

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
    
    # ajout du nombre de points par club
    @app.route('/clubsboard')
    def clubsboard():
        return render_template('board.html', clubs=clubs)


    @app.route('/logout')
    def logout():
        session.pop('username', None)
        return redirect(url_for('index'))

    return app
