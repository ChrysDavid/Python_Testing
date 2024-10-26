import pytest
from app import app

def test_reservation_multiple_clubs(client):
    # Test de réservation pour différents clubs
    for club in [('john@simplylift.co', 'Simply Lift'), ('admin@irontemple.com', 'Iron Temple'), ('kate@shelifts.co.uk', 'She Lifts')]:
        client.post('/showSummary', data={'email': club[0]})
        response = client.post('/purchasePlaces', data={
            'competition': 'Fall Classic',
            'club': club[1],
            'places': '1'
        })
        assert response.status_code == 200
        # assert b"Reservation effectuee avec succes !" in response.data

#     # Vérification que le nombre de places a bien été mis à jour
    # response = client.get('/')
    # assert b"Simply Lift" in response.data
    # assert b"10" in response.data 