from server import app
import html
import json
from .conftest import client, mock_competitions, mock_clubs

def test_book_past_competition(mock_competitions, mock_clubs):
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


def test_book_future_competition(mock_clubs, mock_competitions):
    with app.test_request_context():

        competitions = mock_competitions
        clubs = mock_clubs

        # Exécute la fonction book avec une compétition passée
        with app.test_client() as client:
            response = client.get('/book/HollyDays/Simply_Lift')

            # Vérifie que la redirection s'est produite
            assert response.status_code == 200
            assert "Great-booking complete!"