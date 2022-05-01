import json
from traceback import print_tb
from flask import Flask,render_template,request,redirect,flash, session,url_for


def loadClubs():
    with open('clubs.json') as c:
         listOfClubs = json.load(c)['clubs']
         return listOfClubs


def loadCompetitions():
    with open('competitions.json') as comps:
         listOfCompetitions = json.load(comps)['competitions']
         return listOfCompetitions

competitions = loadCompetitions()
clubs = loadClubs()

def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)

    app.config.update(config)
    app.secret_key = 'something_special'

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/showSummary',methods=['POST'])
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
        if 'username' in session:
            competition = [c for c in competitions if c['name'] == request.form['competition']][0]
            club = [c for c in clubs if c['name'] == request.form['club']][0]
            placesRequired = int(request.form['places'])
                       
            # ISSUE2 : BUG: Clubs should not be able to use more than their points allowed
            if (
                int(placesRequired) <= int(club['points'])
                and int(placesRequired) >= 0
                and int(placesRequired) <= int(competition['numberOfPlaces'])
            ):

                competition['numberOfPlaces'] = int(competition['numberOfPlaces'])-placesRequired

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



    # TODO: Add route for points display


    @app.route('/logout')
    def logout():
        return redirect(url_for('index'))

    return app
    