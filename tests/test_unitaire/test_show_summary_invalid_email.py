"""
Tests pour la page d'index de l'application.

Ce module contient les tests unitaires de la page d'accueil.
"""
import pytest
from app import app


def test_show_summary_invalid_email(client):
    """Test avec un email invalide pour vérifier la redirection."""
    response = client.post('/showSummary', data={'email': 'invalid@example.com'})
    assert response.status_code == 302  # Vérifie la redirection
    response_follow = client.get(response.headers["Location"])  # Suivre la redirection
    assert b'Email non trouve, veuillez reessayer.' in response_follow.data

def test_show_summary_missing_email(client):
    response = client.post('/showSummary', data={'email': ''})
    assert response.status_code == 302
    response_follow = client.get(response.headers["Location"])
    assert b'Email non trouve, veuillez reessayer.' in response_follow.data

def test_show_summary_malformed_email(client):
    response = client.post('/showSummary', data={'email': 'not-an-email'})
    assert response.status_code == 302