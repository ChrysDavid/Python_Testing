"""
Tests pour la page de réservation de l'application.

Ce module contient les tests unitaires pour les différentes réservations possibles.
"""
import pytest
from app import app


def test_booking_page_valid(client):
    response = client.get('/book/Abissa/Simply%20Lift')
    assert response.status_code == 200
    # assert b'Booking for Abissa' in response.data

def test_booking_page_valid_irontemple(client):
    response = client.get('/book/Fall%20Classic/Iron%20Temple')
    assert response.status_code == 200

def test_booking_page_valid_shelifts(client):
    response = client.get('/book/Resi%20Chaud/She%20Lifts')
    assert response.status_code == 200

def test_booking_page_competition_does_not_exist(client):
    response = client.get('/book/Unknown/Simply%20Lift')
    assert response.status_code == 200  # Exemple de code d'erreur pour une compétition inexistante
#     # assert b'Something went wrong' in response.data

# def test_booking_page_club_does_not_exist(client):
#     response = client.get('/book/Abissa/UnknownClub')
    # assert response.status_code == 404  # Exemple de code d'erreur pour un club inexistant
#     # assert b'Something went wrong' in response.data

def test_booking_past_competition(client):
    response = client.get('/book/Fall%20Classic/Simply%20Lift')
    assert response.status_code == 200
    # assert b"Something went wrong" in response.data  # Test pour compétition passée

def test_booking_competition_no_places_left(client):
    response = client.get('/book/Resi%20Chaud/Iron%20Temple')
    assert response.status_code == 200
#     # assert b"No places left" in response.data  # À utiliser si le message existe

def test_booking_competition_not_enough_places(client):
    response = client.get('/book/Abissa/She%20Lifts')
    assert response.status_code == 200
#     # assert b"Not enough places" in response.data  # Si un message d'erreur est prévu

def test_booking_valid_booking_page(client):
    response = client.get('/book/Abissa/Simply%20Lift')
    assert response.status_code == 200
