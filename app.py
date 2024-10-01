import json
from flask import Flask, render_template, request, redirect, flash, url_for
from datetime import datetime

def loadClubs():
    with open('clubs.json') as c:
         listOfClubs = json.load(c)['clubs']
         return listOfClubs

def loadCompetitions():
    with open('competitions.json') as comps:
         listOfCompetitions = json.load(comps)['competitions']
         # Convertir la date de chaque compétition en objet datetime
         for comp in listOfCompetitions:
             comp['date'] = datetime.strptime(comp['date'], '%Y-%m-%d %H:%M:%S')
         return listOfCompetitions

app = Flask(__name__)
app.secret_key = 'something_special'

competitions = loadCompetitions()
clubs = loadClubs()
current_date = datetime.now()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/showSummary',methods=['POST'])
def showSummary():
    try:
        club = [club for club in clubs if club['email'] == request.form['email']][0]
        return render_template('welcome.html', club=club, competitions=competitions, current_date=current_date)
    except:
        flash('Email non trouvé, veuillez réessayer.')
        return redirect(url_for('index'))

@app.route('/book/<competition>/<club>')
def book(competition,club):
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]
    if foundClub and foundCompetition:
        return render_template('booking.html', club=foundClub, competition=foundCompetition)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, competitions=competitions, current_date=current_date)

@app.route('/purchasePlaces',methods=['POST'])
def purchasePlaces():
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    
    try:
        placesRequired = int(request.form['places'])
    except:
        flash('Erreur!!!! Vous devez entrer un entier')
        return render_template('welcome.html', club=club, competitions=competitions, current_date=current_date)
    
    if placesRequired <= 0:
        flash('Vous avez entré un nombre négatif.')
        return render_template('welcome.html', club=club, competitions=competitions, current_date=current_date)

    if placesRequired > 12:
        flash('Vous ne pouvez pas réserver plus de 12 places.')
        return render_template('welcome.html', club=club, competitions=competitions, current_date=current_date)
    
    if placesRequired > int(competition['numberOfPlaces']):
        flash('Pas assez de places disponibles.')
        return render_template('welcome.html', club=club, competitions=competitions, current_date=current_date)
    
    if placesRequired > int(club['points']):
        flash('Pas assez de points pour réserver ces places.')
        return render_template('welcome.html', club=club, competitions=competitions, current_date=current_date)
    
    competition['numberOfPlaces'] = int(competition['numberOfPlaces']) - placesRequired
    club['points'] = int(club['points']) - placesRequired
    flash('Réservation effectuée avec succès !')
    return render_template('welcome.html', club=club, competitions=competitions, current_date=current_date)

@app.route('/logout')
def logout():
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5080, debug=True)