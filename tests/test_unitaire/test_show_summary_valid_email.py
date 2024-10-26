"""
Tests pour la page d'index de l'application.

Ce module contient les tests unitaires de la page d'accueil.
"""
import pytest
from app import app


def test_show_summary_valid_email_simplylift(client):
    """Test avec un email valide pour Simply Lift."""
    response = client.post('/showSummary', data={'email': 'john@simplylift.co'
                                                 })
    assert response.status_code == 200
    assert b'Welcome, john@simplylift.co' in response.data

def test_show_summary_valid_email_irontemple(client):
    """Test avec un email valide pour Iron Temple."""
    response = client.post('/showSummary', data={'email': 'admin@irontemple.com'})
    assert response.status_code == 200
    assert b'Welcome, admin@irontemple.com' in response.data

def test_show_summary_valid_email_shelifts(client):
    """Test avec un email valide pour She Lifts."""
    response = client.post('/showSummary', data={'email': 'kate@shelifts.co.uk'})
    assert response.status_code == 200
    assert b'Welcome, kate@shelifts.co.uk' in response.data
