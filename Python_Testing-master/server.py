import json
from flask import Flask,render_template,request,redirect,flash,url_for
import datetime

def loadClubs():
    with open('clubs.json') as c:
         listOfClubs = json.load(c)['clubs']
         return listOfClubs


def loadCompetitions():
    with open('competitions.json') as comps:
         listOfCompetitions = json.load(comps)['competitions']
         return listOfCompetitions


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = loadCompetitions()
clubs = loadClubs()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/showSummary',methods=['POST'])
def showSummary():
    email = request.form['email']
    filtered_clubs = [club for club in clubs if club['email'] == email]
    if filtered_clubs:
        club = filtered_clubs[0]
        return render_template('welcome.html', club=club, competitions=competitions)
    else:
        return render_template('index.html', error_message=f"L'email {email} n'est pas enregistré sur le site.")


@app.route('/book/<competition>/<club>')
def book(competition,club):
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]

    if foundClub and foundCompetition:
        current_date = datetime.date.today()
        competition_date = datetime.datetime.strptime(foundCompetition['date'], "%Y-%m-%d %H:%M:%S").date()

        if competition_date >= current_date:

                return render_template('booking.html', club=foundClub, competition=foundCompetition)

        else:
            flash("Ce concours a déjà eu lieu. / This competition has already taken place.")
    else:
        flash("Une erreur s'est produite. Veuillez réessayer / Something went wrong - please try again")

    return render_template('welcome.html', club=club, competitions=competitions)


def updateClubs(current_club,file_path='clubs.json'):
    with open(file_path, 'r') as c:
        clubs = json.load(c)
    updated_clubs = []
    for club in clubs['clubs']:
        if club['name'] == current_club['name']:
            club['points'] = int(current_club['points'])
        else:
            club['points'] = int(club['points'])
        updated_clubs.append(club)
    # updated_clubs = [{'name': club['name'], 'email': club['email'], 'points': int(club['points'])} for club in clubs['clubs']]

    with open(file_path, 'w') as c:
        json.dump({'clubs': updated_clubs}, c, indent=4)

def updateCompetitions(current_competition, file_path='competitions.json'):
    with open(file_path, 'r') as c:
        competitions = json.load(c)
    updated_competitions = []
    for competition in competitions['competitions']:
        if competition['name'] == current_competition['name']:
            competition['numberOfPlaces'] = int(current_competition['numberOfPlaces'])
        else:
            competition['numberOfPlaces'] = int(competition['numberOfPlaces'])
        updated_competitions.append(competition)

    # updated_competitions = [{'name': competition['name'], 'date': competition['date'], 'numberOfPlaces': int(competition['numberOfPlaces'])} for competition in competitions['competitions']]
    with open(file_path, 'w') as c:
        json.dump({'competitions': updated_competitions}, c, indent=4)


@app.route('/purchasePlaces', methods=['POST'])
def purchasePlaces():
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    placesRequired = int(request.form['places'])

    if placesRequired <= int(club['points']):
        if placesRequired <= 12:
            competition['numberOfPlaces'] = str(int(competition['numberOfPlaces']) - placesRequired)
            club['points'] = str(int(club['points']) - placesRequired)
            flash('Super votre réservation est bien prise en compte / Great-booking complete!')
            updateClubs(club)
            updateCompetitions(competition)
        else:
            flash('Vous ne pouvez pas réserver plus de 12 places / You cannot book more than 12 places.')
    else:
        flash("Pas assez de points disponibles pour ce club. / Not enough points available for this club.")

    return render_template('welcome.html', club=club, competitions=competitions)


# TODO: Add route for points display
@app.route('/pointsDisplay')
def pointsDisplay():
    club_points = []
    for club in clubs:
        club_points.append({'name': club['name'], 'points': club['points']})

    # Ajouter la variable 'club' au contexte du modèle
    return render_template('points.html', club_points=club_points, club=club['email'])

@app.route('/logout')
def logout():
    return redirect(url_for('index'))