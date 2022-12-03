from unittest import TestCase

from app import app, games

# Make Flask errors be real errors, not HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']


class BoggleAppTestCase(TestCase):
    """Test flask app of Boggle."""

    def setUp(self):
        """Stuff to do before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_homepage(self):
        """Make sure information is in the session and HTML is displayed"""

        with self.client as client:
            response = client.get('/')
            html = response.get_data(as_text=True )

            self.assertEqual(response.status_code, 200)
            self.assertIn("""<!-- ultimately, you'll write the JS to make a dynamic board ---
         when you do, it will look like this: -->""", html)

    def test_api_new_game(self):
        """Test starting a new game."""

        with self.client as client:
            response = client.post('/api/new-game')
            response_data = response.get_json()
            game_id = response_data['gameId']
            board = response_data['board']

            self.assertTrue(isinstance(board, list))
            self.assertTrue(isinstance(board[0], list))

            self.assertTrue(isinstance(game_id, str))
            self.assertIn(game_id, games)

    def test_score_word(self):
        """Test if word is valid"""

        with self.client as client:
            # make a post request to /api/new-game
            game_response = client.post('/api/new-game')
            # get the response body as json using .get_json()
            game_id = game_response.get_json()['gameId']
            # find that game in the dictionary of games (imported from app.py above)
            game = games[game_id]

            # manually change the game board's rows so they are not random
            game.board[0] = ['H', 'O', 'T', 'Z', 'I']
            game.board[1] = ['H', 'O', 'O', 'Z', 'I']
            game.board[2] = ['H', 'O', 'O', 'Z', 'I']
            game.board[3] = ['H', 'O', 'T', 'T', 'I']
            game.board[4] = ['H', 'O', 'H', 'Z', 'I']

            # test to see that a valid word on the altered board returns {'result': 'ok'}
            # Horizontal
            response = self.client.post(
                '/api/score-word',
                json = {'gameId': game_id, 'word': 'HOT'})
            self.assertEqual(response.get_json(), {'result': 'ok'})

            # Vertical
            response = self.client.post(
                '/api/score-word',
                json = {'gameId': game_id, 'word': 'TOOTH'})
            self.assertEqual(response.get_json(), {'result': 'ok'})

            # Diagonal
            response = self.client.post(
                '/api/score-word',
                json = {'gameId': game_id, 'word': 'HOOT'})
            self.assertEqual(response.get_json(), {'result': 'ok'})

            # test to see that a valid word not on the altered board returns {'result': 'not-on-board'}
            response = self.client.post(
                '/api/score-word',
                json = {'gameId': game_id, 'word': 'FUN'})
            self.assertEqual(response.get_json(), {'result': 'not-on-board'})
            # test to see that an invalid word returns {'result': 'not-word'}
            response = self.client.post(
                '/api/score-word',
                json = {'gameId': game_id, 'word': 'XYZ'})
            self.assertEqual(response.get_json(), {'result': 'not-word'})