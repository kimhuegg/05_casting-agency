
import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Actor, Movie

# ASSISTANT_TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Il9paHdIMUdMUWxfX3d1WkVlUmp5SSJ9.eyJpc3MiOiJodHRwczovL2h1ZWx0LnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2NjdmZjcyYjgwN2FlMDQwZGUzNTIwM2MiLCJhdWQiOiJ1ZGFjaXR5LWNhcHN0b25lIiwiaWF0IjoxNzIwMDIxNTY0LCJleHAiOjE3MjAwMjg3NjQsInNjb3BlIjoiIiwiYXpwIjoiSzQ5QVFBOWZ5aWJDcG1Ua3FVR1lxMk1RVVllUUFndXIiLCJwZXJtaXNzaW9ucyI6WyJ2aWV3OmFjdG9ycyIsInZpZXc6bW92aWVzIl19.JxWHSj84pv7W0MVZgfK3oBBiiqjWM8pcSwAevlTWsS-YAfM5vqYcvztA9ddVG8IZsBgkeSKJfMyxjQyB26cC6Gq7svzN7ynZ8bdKYqj03mneTvtyyrZIR9YffNYln12_GiXXkhg7DXNgUgEUH5gUZfgfMfHDaWGC9U5xd5IvH4n6h9nu7y03F-WT-HGG1LhIKgES1_ZAN0FwkxZldOeCxjD70vc09YKL-Bz5p-HJwp650qN6AXAoyYDRLOOUZXeFAy_Enykoa-7FtsKbwh_kX34yezLAh0oB2XUxHC1eY1JXgqhnlXWro5H4VLI5Fek7Rlq36ZgN6fP9TH_fDggV4Q'
# DIRECTOR_TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Il9paHdIMUdMUWxfX3d1WkVlUmp5SSJ9.eyJpc3MiOiJodHRwczovL2h1ZWx0LnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2NjdmZjc2MzgwN2FlMDQwZGUzNTIwNjEiLCJhdWQiOiJ1ZGFjaXR5LWNhcHN0b25lIiwiaWF0IjoxNzIwMDIxNjc5LCJleHAiOjE3MjAwMjg4NzksInNjb3BlIjoiIiwiYXpwIjoiSzQ5QVFBOWZ5aWJDcG1Ua3FVR1lxMk1RVVllUUFndXIiLCJwZXJtaXNzaW9ucyI6WyJhZGQ6YWN0b3IiLCJkZWxldGU6YWN0b3IiLCJ1cGRhdGU6YWN0b3IiLCJ1cGRhdGU6bW92aWUiLCJ2aWV3OmFjdG9ycyIsInZpZXc6bW92aWVzIl19.T3Vwhjb4QePIlPhPlNZu6TdLVqg7U2VudM73vVO8_yaT0TGKX755BB7-QQsXpQSqXYf8rpuKVP72JGcvW9zD2P7Ef4f4-V0uCMtiBvr3FE7mSDEzDPVg8awGLsjKDItgvzO9fT1xgWxNtZu-WLN7lH29Mavwym7O5cWp-hmOY_K1a6cHOh94LaQxAQG3LlXnxVBoScgrC1Ima0oAkVUfsX379qxShbyOjxdMdjirqJfsOEifx_PtDgKZ6My2_NXhcrzDcnMTq13sjcPquM4K2kmBdDvT7BK0MiJfjiksVfanJCpHDrF-us5gJtdH4XPdSn268P2_NRtGNvzC3QU84A'
# PRODUCER_TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Il9paHdIMUdMUWxfX3d1WkVlUmp5SSJ9.eyJpc3MiOiJodHRwczovL2h1ZWx0LnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2NjdmZjc4ODgwN2FlMDQwZGUzNTIwN2MiLCJhdWQiOiJ1ZGFjaXR5LWNhcHN0b25lIiwiaWF0IjoxNzIwMDIxNzIyLCJleHAiOjE3MjAwMjg5MjIsInNjb3BlIjoiIiwiYXpwIjoiSzQ5QVFBOWZ5aWJDcG1Ua3FVR1lxMk1RVVllUUFndXIiLCJwZXJtaXNzaW9ucyI6WyJhZGQ6YWN0b3IiLCJhZGQ6bW92aWUiLCJkZWxldGU6YWN0b3IiLCJkZWxldGU6bW92aWUiLCJ1cGRhdGU6YWN0b3IiLCJ1cGRhdGU6bW92aWUiLCJ2aWV3OmFjdG9ycyIsInZpZXc6bW92aWVzIl19.Aeyq8HY56ltHs7wRNjI9W644ZFNs-ndJaVZnLZkFbicKi1EJF6ezX7L1qpKGe05yasvGt3dcMCe1mGjaRkU40BeHdnw2SmX_1xQjVc5QgOqLJYyjRj1MGLN5-ElMRXl17zavxPfOFs4S4l-ljNeWAyNyt0TBGOeYR8t8N5iyTcHlg-jQRkinWpPYxkDX0AXtyC2n-uRwK7kK_DuXcnfbTsJ4BAHt0gyE1FFFOjo_jSYMEp86ZBoG8aKpzdD45vXzNgb-cqR2MM42nE-fVT7eZe76ush3dPo_oJqWo4DURUlXM8wMJ4nG8Arx6pO8BlplL2M2f7WIkpTBaN7kzS66yw'

# DB_HOST = os.getenv('DB_HOST', 'localhost:5432')
# DB_USER = os.getenv('DB_USER', 'lethihue')
# DB_PASSWORD = os.getenv('DB_PASSWORD','')
# DB_NAME = os.getenv('DB_NAME', "capstone")
# DB_PATH = "postgres://{}:{}@{}/{}".format(DB_USER, DB_PASSWORD, DB_HOST, DB_NAME)

DB_PATH = os.environ['DATABASE_URL']
ASSISTANT_TOKEN = os.environ['ASSISTANT_TOKEN']
DIRECTOR_TOKEN = os.environ['DIRECTOR_TOKEN']
PRODUCER_TOKEN = os.environ['PRODUCER_TOKEN']


class CapstoneTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.client = self.app.test_client
        self.database_path = DB_PATH
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        self.db.session.remove()
        pass

    # TESTCASE: ACTOR
    # GET - successful - all role
    def test_get_actors_success(self):
        # request the actors
        res = self.client().get('/actors')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['actors'])

    # POST - successful - Director or Producer
    def test_post_new_actor_success(self):
        res = self.client().post('/actors',
                json={
                    'name': "George",
                    'age': 28,
                    'gender': 'MALE'
                },
                headers={'Authorization':'Bearer ' + DIRECTOR_TOKEN}
            )
        data = json.loads(res.data)

        actor = Actor.query.filter_by(id=data['created']).one_or_none()

        self.assertEqual(res.status_code, 201)
        self.assertTrue(data['success'])
        self.assertIsNotNone(actor)
    
    # POST - faillfully - Director or Producer - with missing gender
    def test_post_new_actor_(self):
        res = self.client().post('/actors',
                json={
                    'name': "George",
                    'age': 28,
                },
                headers={'Authorization':'Bearer ' + DIRECTOR_TOKEN}
            )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])
    
    # DELETE - successful - Director or Producer
    def test_delete_actor_success(self):
        res = self.client().post('/actors',
                json={
                    'name': "George",
                    'age': 28,
                    'gender': 'MALE'
                },
                headers={'Authorization':'Bearer ' + DIRECTOR_TOKEN}
            )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 201)

        res = self.client().delete('/actors/{}'.format(data['created']),
                headers={'Authorization':'Bearer ' + DIRECTOR_TOKEN}
            )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['actor'])

    # DELETE - faillfully - Director or Producer
    def test_delete_actor_not_found(self):
        # Perform DELETE request for a non-existent actor ID
        res = self.client().delete('/actors/{}'.format(999),
                headers={'Authorization':'Bearer ' + DIRECTOR_TOKEN}
            )
        data = json.loads(res.data)

        # Assert HTTP status code 404 (Not Found)
        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['error'], 404)
    
    # PATCH - successful - Director or Producer
    def test_update_actor_success(self):
        # Create a mock actor in the database
        mock_actor = Actor(name='Test Actor', age=30, gender='Male')
        mock_actor.insert()

        # Update data
        updated_data = {
            'name': 'Updated Actor',
            'age': 35,
            'gender': 'Female'
        }

        # Perform PATCH request to update the actor
        res = self.client().patch('/actors/{}'.format(mock_actor.id), json=updated_data,
                headers={'Authorization':'Bearer ' + DIRECTOR_TOKEN}
            )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['updated'])
        self.assertEqual(data['updated']['name'], 'Updated Actor')

    # PATCH - faillfully - Director or Producer
    def test_update_actor_not_found(self):
        updated_data = {
            'name': 'Updated Actor',
            'age': 35,
            'gender': 'Female'
        }
        
        res = self.client().patch('/actors/{}'.format(999),
                    json=updated_data,
                    headers={'Authorization':'Bearer ' + DIRECTOR_TOKEN}
                )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Not found')

    # TESTCASE: MOVIE ---------------------------------------#
    # GET - successful - all role
    def test_get_movies_success(self):
        # request the actors
        res = self.client().get('/movies')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['movies'])

    # POST - successful - Producer
    def test_post_new_movie_success(self):
        res = self.client().post('/movies',
                json={
                    'title': "MAHABHARATA - 2",
                    'release_date': "2032-10-10"
                },
                headers={'Authorization':'Bearer ' + PRODUCER_TOKEN}
            )
        data = json.loads(res.data)

        movie = Movie.query.filter_by(id=data['created']).one_or_none()

        self.assertEqual(res.status_code, 201)
        self.assertTrue(data['success'])
        self.assertIsNotNone(movie)

    # POST - faillfully - Producer - with missing title
    def test_post_new_movie_success(self):
        res = self.client().post('/movies',
                json={
                    'release_date': "2032-10-10"
                },
                headers={'Authorization':'Bearer ' + PRODUCER_TOKEN}
            )

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])

    # DELETE - successful - Producer
    def test_delete_movie_success(self):
        res = self.client().post('/movies',
                json={
                    'title': "MAHABHARATA - 2",
                    'release_date': "2032-10-10"
                },
                headers={'Authorization':'Bearer ' + PRODUCER_TOKEN}
            )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 201)

        res = self.client().delete('/movies/{}'.format(data['created']),
                headers={'Authorization':'Bearer ' + PRODUCER_TOKEN}
            )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['movie'])

    # DELETE - faillfully - Producer
    def test_delete_movie_not_found(self):
        # Perform DELETE request for a non-existent actor ID
        res = self.client().delete('/movies/{}'.format(999),
                headers={'Authorization':'Bearer ' + PRODUCER_TOKEN}
            )
        data = json.loads(res.data)

        # Assert HTTP status code 404 (Not Found)
        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['error'], 404)
    
    # PATCH - successful - Director or Producer
    def test_update_movie_success(self):
        # Create a mock actor in the database
        mock_movie = Movie(title='Test Movie', release_date="2032-10-10")
        mock_movie.insert()

        # Update data
        updated_data = {
                'title': "Updated Movie",
            }

        # Perform PATCH request to update the actor
        res = self.client().patch('/movies/{}'.format(mock_movie.id), json=updated_data,
                headers={'Authorization':'Bearer ' + DIRECTOR_TOKEN}
            )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['updated'])
        self.assertEqual(data['updated']['title'], 'Updated Movie')

    # PATCH - faillfully - Director or Producer
    def test_update_movie_not_found(self):
        updated_data = {
                'title': "Updated Movie",
            }
        
        res = self.client().patch('/movies/{}'.format(999),
                    json=updated_data,
                    headers={'Authorization':'Bearer ' + DIRECTOR_TOKEN}
                )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Not found')

    # RBAC
    # RBAC POST actors with wrong Authorization header - Assistant Role
    def test_post_actor_wrong_auth(self):
        res = self.client().post('/actors',
            json={
                'name': "George",
                'age': 28,
                'gender': 'male'
            },
            headers={'Authorization':'Bearer ' + ASSISTANT_TOKEN}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Permission not found.')

    # RBAC DELETE actors with wrong Authorization header - Assistant Role
    def test_delete_actor_wrong_auth(self):
        res = self.client().post('/actors',
                json={
                    'name': "George",
                    'age': 28,
                    'gender': 'MALE'
                },
                headers={'Authorization':'Bearer ' + DIRECTOR_TOKEN}
            )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 201)

        res = self.client().delete('/actors/{}'.format(data['created']),
                headers={'Authorization':'Bearer ' + ASSISTANT_TOKEN}
            )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Permission not found.')

    # RBAC DELETE with wrong Authorization header - Director Role
    def test_delete_movie_wrong_auth(self):
        res = self.client().post('/movies',
                json={
                    'title': "MAHABHARATA - 2",
                    'release_date': "2032-10-10"
                },
                headers={'Authorization':'Bearer ' + PRODUCER_TOKEN}
            )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 201)

        res = self.client().delete('/movies/{}'.format(data['created']),
                headers={'Authorization':'Bearer ' + DIRECTOR_TOKEN}
            )

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Permission not found.')

    # RBAC POST with wrong Authorization header - Director Role
    def test_post_new_movie_wrong_auth(self):
        res = self.client().post('/movies',
                json={
                    'title': "MAHABHARATA - 2",
                    'release_date': "2032-10-10"
                },
                headers={'Authorization':'Bearer ' + DIRECTOR_TOKEN}
            )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Permission not found.')

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()