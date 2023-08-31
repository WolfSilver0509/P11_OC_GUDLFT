from server import app
import json
from test.conftest import client, mock_competitions, mock_clubs

def test_user_path_valid(monkeypatch,mock_competitions, mock_clubs ):
    """ Parcour d'un user valide avec uen réservation de places """
    # Définir les données simulées pour la requête
    email = 'kate@shelifts.co.uk'
    data = {'email': email}

    # Simuler la requête
    with app.test_client() as client:
        response = client.post('/showSummary', data=data)

    # Vérifier la réponse
    assert response.status_code == 200
    assert b'Welcome' in response.data
    assert b'kate@shelifts.co.uk' in response.data

    # Charger les données des fichiers JSON
    with open("clubs.json") as clubs_file:
        clubs_data = json.load(clubs_file)

    with open("competitions.json") as competitions_file:
        competitions_data = json.load(competitions_file)

    # Simuler une requête POST avec suffisamment de points disponibles
    response = client.post('/purchasePlaces', data={'competition': 'HollyDays', 'club': 'Club_2', 'places': '3'})

    # Vérifier la réponse
    assert response.status_code == 200
    assert "Great-booking complete!" in response.data.decode('utf-8')