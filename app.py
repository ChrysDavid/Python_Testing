"""Module pour traiter les données JSON.

Ce module fournit des fonctions pour charger et manipuler des données JSON.

Attributes:
    NOM_VARIABLE (type): Description de la variable si applicable.
"""
import json
import os
from flask import Flask, render_template, request, redirect, flash, url_for
from datetime import datetime


def load_clubs():
    """Charge la liste des clubs depuis un fichier JSON.

    Cette fonction ouvre le fichier 'clubs.json', charge le contenu JSON,
    et retourne la liste des clubs.

    Returns:
        list: Une liste de clubs extraite du fichier JSON.
    """
    file_path = os.path.join(os.path.dirname(__file__), 'clubs.json')
    with open(file_path) as c:
        list_of_clubs = json.load(c)['clubs']
    return list_of_clubs


def load_competitions():
    """Charge les compétitions depuis un fichier JSON et convertit les dates.

    Cette fonction ouvre le fichier 'competitions.json', charge le contenu
    JSON, convertit les dates de chaque compétition en objets datetime
    et retourne la liste.

    Returns:
        list: Une liste de compétitions avec les dates au format datetime.
    """
    file_path = os.path.join(os.path.dirname(__file__), 'competitions.json')
    with open(file_path) as comps:
        list_of_competitions = json.load(comps)['competitions']
        # Convertir la date de chaque compétition en objet datetime
        for comp in list_of_competitions:
            comp['date'] = datetime.strptime(comp['date'], '%Y-%m-%d %H:%M:%S')
    return list_of_competitions


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = load_competitions()
clubs = load_clubs()
current_date = datetime.now()


@app.route('/')
def index():
    """Affiche la page d'accueil avec la liste des clubs."""
    return render_template('index.html', clubs=clubs)


@app.route('/showSummary', methods=['POST'])
def show_summary():
    """Afficher la page de bienvenue après vérification de l'email."""
    try:
        club = [
            club for club in clubs if club['email'] == request.form['email']
        ][0]
        return render_template(
            'welcome.html', club=club, competitions=competitions,
            current_date=current_date
        )
    except IndexError:
        flash('Email non trouve, veuillez reessayer.')
        return redirect(url_for('index'))


@app.route('/book/<competition>/<club>')
def book(competition, club):
    """Afficher la page de réservation pour un club et une seul compétition."""
    found_club = [c for c in clubs if c['name'] == club][0]
    found_competition = [c for c in competitions if c['name'] == competition]
    [
        0
    ]
    if found_club and found_competition:
        return render_template(
            'booking.html', club=found_club, competition=found_competition
        )
    else:
        flash("Something went wrong-please try again")
        return render_template(
            'welcome.html', club=club, competitions=competitions,
            current_date=current_date
        )


@app.route('/purchasePlaces', methods=['POST'])
def purchase_places():
    """Gestion de l'achat de places avec vérification des conditions."""
    competition = [
        c for c in competitions if c['name'] == request.form['competition']
    ][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]

    try:
        places_required = int(request.form['places'])
    except ValueError:
        flash('Erreur! Vous devez entrer un entier')
        return render_template(
            'welcome.html', club=club, competitions=competitions,
            current_date=current_date
        )

    if places_required <= 0:
        flash('Vous avez entré un nombre négatif.')
        return render_template(
            'welcome.html', club=club, competitions=competitions,
            current_date=current_date
        )

    if places_required > 12:
        flash('Vous ne pouvez pas réserver plus de 12 places.')
        return render_template(
            'welcome.html', club=club, competitions=competitions,
            current_date=current_date
        )

    if places_required > int(competition['numberOfPlaces']):
        flash('Pas assez de places disponibles.')
        return render_template(
            'welcome.html', club=club, competitions=competitions,
            current_date=current_date
        )

    if places_required > int(club['points']):
        flash('Pas assez de points pour réserver ces places.')
        return render_template(
            'welcome.html', club=club, competitions=competitions,
            current_date=current_date
        )

    competition['numberOfPlaces'] = int(competition['numberOfPlaces']) - \
        places_required
    club['points'] = int(club['points']) - places_required
    flash('Réservation effectuée avec succès !')
    return render_template(
        'welcome.html', club=club, competitions=competitions,
        current_date=current_date
    )


@app.route('/logout')
def logout():
    """Déconnexion de l'utilisateur et redirection vers la page d'accueil."""
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run()
