import unittest
import os
from flask import json
from src.app import create_app, db

class UserTestCases(unittest.TestCase):

    def setUp(self):
        self.app = create_app(env_name)
        self.client = self.app.test_client
        self.user = {'name': 'tester', 'email': 'testing11@gmail.com', 'password': 'abc123'}
        # new db context for every test
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_200_ping(self):
        # Create user request
        req = self.client().get(route_1)
        self.assertEqual(req.status_code, 200)
        self.assertTrue('End point working!!')

    def test_201_create(self):
        # Create user request
        req = self.client().post(route_2, json=self.user)
        resp = json.loads(req.data)
        # check response provided a jwt token
        self.assertTrue(resp.get('jwt_token'))
        self.assertEqual(req.status_code, 201)

    def test_400_create_duplicate(self):
        # Create user request
        req = self.client().post(route_2, json=self.user)
        resp = json.loads(req.data)
        #Create a duplicate user
        req = self.client().post(route_2, json=self.user)
        resp = json.loads(req.data)
        self.assertEqual(req.status_code, 400)
        self.assertTrue(resp.get('error'))

    def test_400_create_empty(self):
        # Create user request with empty body
        req = self.client().post(route_2, json={})
        resp = json.loads(req.data)
        self.assertEqual(req.status_code, 400)
        self.assertTrue(resp.get('error'))

    def test_200_get_all(self):
        # Create user request
        req = self.client().post(route_2, json=self.user)
        # Get api token from response
        api_token = json.loads(req.data).get('jwt_token')
        req = self.client().get(route_2, headers={'Content-Type': 'application/json', 'api-token': api_token})
        self.assertEqual(req.status_code, 200)

    def test_400_invalid_token(self):
        # Create user request
        req = self.client().get(route_2, headers={'Content-Type': 'application/json', 'api-token': ''})
        resp = json.loads(req.data)
        self.assertEqual(req.status_code, 400)
        self.assertTrue(resp.get('error'))

    def test_400_unauthorized(self):
        # Create user request
        req = self.client().get(route_2)
        resp = json.loads(req.data)
        self.assertEqual(req.status_code, 400)
        self.assertTrue(resp.get('error'))

    def test_200_get_a_user(self):
        # Create user request
        req = self.client().post(route_2, json=self.user)
        # Get api token from response
        api_token = json.loads(req.data).get('jwt_token')
        # get user with valid user id
        req = self.client().get(route_2+str(1), headers={'Content-Type': 'application/json', 'api-token': api_token})
        self.assertEqual(req.status_code, 200)

    def test_200_get_nonexistant(self):
        # Create user request
        req = self.client().post(route_2, json=self.user)
        # Get api token from response
        api_token = json.loads(req.data).get('jwt_token')
        # get user with invalid user id
        req = self.client().get(route_2+str(123), headers={'Content-Type': 'application/json', 'api-token': api_token})
        self.assertEqual(req.status_code, 404)

    def test_200_login(self):
        # Create user request
        req = self.client().post(route_2, json=self.user)
        # Login request with new user credentials
        login = self.client().post(route_3, json={'email': 'testing11@gmail.com', 'password': 'abc123'})
        resp = json.loads(login.data)
        self.assertEqual(login.status_code, 200)
        self.assertTrue(resp.get('jwt_token'))

    def test_400_login_missing_info(self):
        # Create user request
        req = self.client().post(route_2, json=self.user)
        # Login request with missing password field
        login = self.client().post(route_3, json={'email': 'testing11@gmail.com'})
        resp = json.loads(login.data)
        self.assertEqual(login.status_code, 400)
        self.assertTrue(resp.get('error'))

    def test_400_login_nonexistant(self):
        # Create user request
        req = self.client().post(route_2, json=self.user)
        # Login request with non-existant user
        login = self.client().post(route_3, json={'email': 'nonexistant@gmail.com', 'password': 'abc123'})
        resp = json.loads(login.data)
        self.assertEqual(login.status_code, 400)
        self.assertTrue(resp.get('error'))

    def test_400_login_invalid_pass(self):
        # Create user request
        req = self.client().post(route_2, json=self.user)
        # Login request with invalid user credentials
        login = self.client().post(route_3, json={'email': 'testing11@gmail.com', 'password': 'invalid'})
        resp = json.loads(login.data)
        self.assertEqual(login.status_code, 400)
        self.assertTrue(resp.get('error'))

    def test_200_get_me(self):
        # Create user request
        req = self.client().post(route_2, json=self.user)
        # Get api token from reqponse
        api_token = json.loads(req.data).get('jwt_token')
        # New request with api token in header
        req = self.client().get(route_4, headers={'Content-Type': 'application/json', 'api-token': api_token})
        self.assertEqual(req.status_code, 200)

    def test_200_update(self):
        # Create user request
        req = self.client().post(route_2, json=self.user)
        # Get api token from reqponse
        api_token = json.loads(req.data).get('jwt_token')
        # New request with api token in header
        req = self.client().put(route_4, headers={'Content-Type': 'application/json', 'api-token': api_token}, json={'name': 'New name', 'password': 'new password'})
        resp = json.loads(req.data)
        self.assertEqual(req.status_code, 200)

    def test_400_update_fail(self):
        # Create user request
        req = self.client().post(route_2, json=self.user)
        # Get api token from reqponse
        api_token = json.loads(req.data).get('jwt_token')
        # New request with api token in header
        req = self.client().put(route_4, headers={'Content-Type': 'application/json', 'api-token': api_token}, json={'not a field': 'badfield', 'password': 'new password'})
        resp = json.loads(req.data)
        self.assertEqual(req.status_code, 400)
        self.assertTrue(resp.get('error'))

    def test_200_delete(self):
        # Create user request
        req = self.client().post(route_2, json=self.user)
        # Get api token from reqponse
        api_token = json.loads(req.data).get('jwt_token')
        # New request with api token in header
        req = self.client().delete(route_4, headers={'Content-Type': 'application/json', 'api-token': api_token})
        resp = json.loads(req.data)
        self.assertEqual(req.status_code, 200)
        self.assertTrue(resp.get('message'))

if __name__ == "__main__":
    env_name = os.getenv('FLASK_ENV')
    route_1 = "/"
    route_2 = "/api/users/"
    route_3 = "/api/users/login"
    route_4 = "/api/users/me"

    unittest.main()
