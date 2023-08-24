from .conftest import client

def test_user_path_valid(client):
    """ Test sur le chemin d'un utilisateur valide"""
    def show_summary_with_existing_email(client):
        # Simule une requête POST à '/showSummary' avec un email existant
        response = client.post('/showSummary', data={'email': 'kate@shelifts.co.uk'})

        # Assert retourne le code 200 (OK)
        assert response.status_code == 200

        assert 'Welcome' in response.get_data(as_text=True)
        assert 'kate@shelifts.co.uk' in response.get_data(as_text=True)

    def purchase_places_with_enough_points_available(client):
        # Charger les données des fichiers JSON
        with open("clubs.json") as clubs_file:
            clubs_data = json.load(clubs_file)

        with open("competitions.json") as competitions_file:
            competitions_data = json.load(competitions_file)

        # Simuler une requête POST avec suffisamment de points disponibles
        response = client.post('/purchasePlaces',
                               data={'competition': 'Fall Classic', 'club': 'Simply Lift', 'places': '3'})

        # Vérifier la réponse
        assert response.status_code == 200
        assert "Great-booking complete!" in response.data.decode('utf-8')

    def purchase_valid_places(client, mock_competitions, mock_clubs):
        # Créez des données de test pour la compétition et le club pour tester la réservation de places
        competition = mock_competitions
        club = mock_clubs
        # Simulez une requête POST avec un nombre de places dans la limite maximale
        response = client.post('/purchasePlaces',
                               data={'competition': 'More_than_12_places_avalaible', 'club': 'Simply_Lift',
                                     'places': '6'})
        # Vérifiez la réponse et le message flash correspondant
        assert response.status_code == 200
        assert "Super votre réservation est bien prise en compte / Great-booking complete!" in response.data.decode(
            'utf-8')


def test_user_path_invalid(client):
    """ Test sur le chemin d'un utilisateur invalide"""
    def show_summary_with_non_existing_email(client):
        # Simule une requête POST à '/showSummary' avec un email non existant
        response = client.post('/showSummary', data={'email': 'nonexisting@example.com'})

        # Assert retourne le code 200 (OK)
        assert response.status_code == 200

        error_message = "L'email nonexisting@example.com n'est pas enregistré sur le site."
        decoded_response = html.unescape(response.get_data(as_text=True))
        assert error_message in decoded_response


def test_user_path_valid_morepointallowed(client):
    """ Test sur le chemin d'un utilisateur valide avec un probléme de trop de points"""
    def show_summary_with_existing_email(client):
        # Simule une requête POST à '/showSummary' avec un email existant
        response = client.post('/showSummary', data={'email': 'kate@shelifts.co.uk'})

        # Assert retourne le code 200 (OK)
        assert response.status_code == 200

        assert 'Welcome' in response.get_data(as_text=True)
        assert 'john@simplylift.co' in response.get_data(as_text=True)

    def purchase_places_with_not_enough_points_available(client):
        # Charger les données des fichiers JSON
        with open("clubs.json") as clubs_file:
            clubs_data = json.load(clubs_file)

        with open("competitions.json") as competitions_file:
            competitions_data = json.load(competitions_file)

        # Simuler une requête POST avec un nombre de points supérieur à ceux disponibles
        response = client.post('/purchasePlaces',
                               data={'competition': 'Fall Classic', 'club': 'Iron Temple', 'places': '5'})

        # Vérifier la réponse
        assert response.status_code == 200
        assert "Not enough points available for this club." in response.data.decode('utf-8')

    def test_purchase_places_exceed_max_limit(client, mock_competitions, mock_clubs):
        # charger des données de test pour la compétition et le club pour tester la réservation de places
        competitions = mock_competitions
        clubs = mock_clubs

        # Simulez une requête POST avec un nombre de places supérieur à la limite maximale
        response = client.post('/purchasePlaces',
                               data={'club': 'Simply_Lift', 'competition': 'More_than_12_places_avalaible',
                                     'places': '13'})

        # Vérifiez la réponse et le message flash correspondant
        assert response.status_code == 200
        assert "Vous ne pouvez pas réserver plus de 12 places / You cannot book more than 12 places." in response.data.decode(
            'utf-8')