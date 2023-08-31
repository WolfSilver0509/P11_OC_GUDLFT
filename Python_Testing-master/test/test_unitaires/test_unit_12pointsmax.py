from server import app
import html
import json
from test.conftest import client, mock_competitions, mock_clubs

def test_purchase_places_exceed_max_limit(client , mock_competitions, mock_clubs):
    # charger des données de test pour la compétition et le club pour tester la réservation de places
    competitions = mock_competitions
    clubs = mock_clubs

    # Simulez une requête POST avec un nombre de places supérieur à la limite maximale
    response = client.post('/purchasePlaces', data={ 'club': 'Simply_Lift','competition': 'More_than_12_places_avalaible', 'places': '13'})

    # Vérifiez la réponse et le message flash correspondant
    assert response.status_code == 200
    assert "Vous ne pouvez pas réserver plus de 12 places / You cannot book more than 12 places." in response.data.decode('utf-8')


def test_purchase_valid_places(client, mock_competitions, mock_clubs):
    # Créez des données de test pour la compétition et le club pour tester la réservation de places
    competition = mock_competitions
    club = mock_clubs
    # Simulez une requête POST avec un nombre de places dans la limite maximale
    response = client.post('/purchasePlaces', data={'competition': 'More_than_12_places_avalaible', 'club': 'Simply_Lift', 'places': '6'})
    # Vérifiez la réponse et le message flash correspondant
    assert response.status_code == 200
    assert "Super votre réservation est bien prise en compte / Great-booking complete!" in response.data.decode('utf-8')