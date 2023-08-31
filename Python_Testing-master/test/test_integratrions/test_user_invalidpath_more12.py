from server import app

from test.conftest import client, mock_competitions, mock_clubs

def test_user_invalid_path_more_12(client, mock_competitions, mock_clubs):
    """ Parcours d'un user avec trop de places """
    email = 'kate@shelifts.co.uk'
    data = {'email': email}

    # Simuler la requête
    with app.test_client() as client:
        response = client.post('/showSummary', data=data)

    # Vérifier la réponse
    assert response.status_code == 200
    assert b'Welcome' in response.data
    assert b'kate@shelifts.co.uk' in response.data

    # charger des données de test pour la compétition et le club pour tester la réservation de places
    competitions = mock_competitions
    clubs = mock_clubs

    # Simulez une requête POST avec un nombre de places supérieur à la limite maximale
    response = client.post('/purchasePlaces', data={ 'club': 'Simply_Lift','competition': 'More_than_12_places_avalaible', 'places': '13'})

    # Vérifiez la réponse et le message flash correspondant
    assert response.status_code == 200
    assert "Vous ne pouvez pas réserver plus de 12 places / You cannot book more than 12 places." in response.data.decode('utf-8')