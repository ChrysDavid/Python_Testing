"""Tests pour la page d'index de l'application.

Ce module contient les tests unitaires de la page d'accueil.
"""
import pytest
from app import app

def test_index_login_form(client):
    """Tester la présence du formulaire de login.
    
    Args:
        client: Fixture du client de test Flask
    """
    response = client.get('/')
    assert b'<form' in response.data
    assert b'email' in response.data
    assert b'submit' in response.data