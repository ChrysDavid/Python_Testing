# tests/test_unitaire/test_index_page.py
"""Tests pour la page d'index de l'application.

Ce module contient les tests unitaires de la page d'accueil.
"""
import pytest
from app import app


def test_index_page(client):
    """Tester l'affichage de la page d'accueil.
     
    Args:
        client: Fixture du client de test Flask
    """
    response = client.get('/')
    assert response.status_code == 200
    assert b'Simply Lift' in response.data
