import pytest
from app import app

def test_flux_complet(client):
    # Préparation et lancement de l'application (simulation)
    response = client.get('/')
    assert response.status_code == 200  
    assert b"GUDLFT Registration" in response.data 
    assert b"Simply Lift" in response.data 
    assert b"Iron Temple" in response.data 
    assert b"She Lifts" in response.data 

    # 1. Connexion
    response = client.post('/showSummary', data={'email': 'john@simplylift.co'})
    print(response.data.decode('utf-8'))  # Gardez-le pour voir le contenu
    assert response.status_code == 200
    assert b"Welcome, john@simplylift.co" in response.data

    # # 2. Visualisation des compétitions
    # assert b"Abissa" in response.data  
    # assert b"Resi Chaud" in response.data 

    # 3. Réservation
    # response = client.post('/purchasePlaces', data={
    #     'competition': 'Abissa',
    #     'club': 'Simply Lift',
    #     'places': '2'
    # })
    # assert response.status_code == 200
    # assert b"Reservation effectuee avec succes !" in response.data

    # # # 4. Vérification de la mise à jour des points
    # response = client.get('/')
    # assert b"Simply Lift" in response.data
    # assert b"11" in response.data 

    # # 5. Déconnexion
    response = client.get('/logout')
    assert response.status_code == 302
    # assert response.headers['Location'] == '/'

    # 6. Echec de connexion
    response = client.post('/showSummary', data={'email': 'john@simplylift.com'}, follow_redirects=True)
    assert response.status_code == 200
    assert b"Email non trouve, veuillez reessayer." in response.data 

