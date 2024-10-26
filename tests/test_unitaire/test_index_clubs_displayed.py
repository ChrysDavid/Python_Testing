"""Tests pour la page d'index de l'application.

Ce module contient les tests unitaires de la page d'accueil.
"""
import pytest
from app import app

def test_index_clubs_displayed(client):
    """Tester l'affichage des clubs sur la page d'accueil.
    
    Args:
        client: Fixture du client de test Flask
    """
    response = client.get('/')
    test_clubs = [b'Simply Lift', b'Iron Temple', b'She Lifts']
    for club in test_clubs:
        assert club in response.data