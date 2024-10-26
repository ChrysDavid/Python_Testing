# tests/conftest.py
"""Configuration globale des fixtures pytest.

Ce module contient les fixtures partagées entre tous les tests.
"""
import pytest
from app import app


@pytest.fixture
def client():
    """Créer un client de test pour l'application Flask.
    
    Returns:
        FlaskClient: Client de test configuré
    """
    app.config['TESTING'] = True
    with app.test_client() as test_client:
        yield test_client