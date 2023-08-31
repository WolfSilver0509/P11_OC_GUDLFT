from server import app
from test.conftest import client, mock_competitions, mock_clubs

def test_user_path_past_competition(mock_competitions, mock_clubs):
    """ Parcours d'un user avec une compétition passée"""

    email = 'kate@shelifts.co.uk'
    data = {'email': email}

    # Simuler la requête
    with app.test_client() as client:
        response = client.post('/showSummary', data=data)

    # Vérifier la réponse
    assert response.status_code == 200
    assert b'Welcome' in response.data
    assert b'kate@shelifts.co.uk' in response.data

    with app.test_request_context():

        competitions = mock_competitions
        clubs = mock_clubs

        # Exécute la fonction book avec une compétition passée
        with app.test_client() as client:
            response = client.get('/book/Date_Over/Simply_Lift')

            # Vérifie que la redirection s'est produite
            assert response.status_code == 200
            assert "Ce concours a déjà eu lieu." in response.data.decode('utf-8')
            assert "This competition has already taken place." in response.data.decode('utf-8')