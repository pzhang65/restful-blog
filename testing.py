import unittest
import os
from flask import json
from src.app import create_app, db

class UserTestCases(unittest.TestCase):

    def setUp(self):
        self.app = create_app(env_name)
        self.client = self.app.test_client
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_200_ping(self):
        res = self.client().get(route_1)
        self.assertEqual(res.status_code, 200)
        self.assertTrue('End point working!!')

    def test_201_create(self):
        res = self.client().post(route_2, json=
                    {'name': 'tester', 'email': 'testing11@gmail.com', 'password': 'abc123'})
        received = json.loads(res.data)
        self.assertTrue(received.get('jwt_token'))
        self.assertEqual(res.status_code, 201)

    def test_400_create_duplicate(self):
        res = self.client().post(route_2, json=
                    {'name': 'tester', 'email': 'testing11@gmail.com', 'password': 'abc123'})
        received = json.loads(res.data)
        self.assertTrue(received.get('jwt_token'))
        self.assertEqual(res.status_code, 201)
        res = self.client().post(route_2, json=
                    {'name': 'tester', 'email': 'testing11@gmail.com', 'password': 'abc123'})
        received = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertTrue(received.get('error'))

    def test_400_create_empty(self):
        res = self.client().post(route_2, json={})
        received = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertTrue(received.get('error'))

    def test_200_get_all(self):
        res = self.client().post(route_2, json=
                    {'name': 'tester', 'email': 'testing11@gmail.com', 'password': 'abc123'})
        received = json.loads(res.data)
        api_token = received.get('jwt_token')
        res = self.client().get(route_2, headers={'Content-Type': 'application/json', 'api-token': api_token})
        self.assertEqual(res.status_code, 200)

    def test_400_invalid_token(self):
        res = self.client().get(route_2, headers={'Content-Type': 'application/json', 'api-token': ''})
        received = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertTrue(received.get('error'))

    def test_400_unauthorized(self):
        res = self.client().get(route_2)
        received = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertTrue(received.get('error'))

    def test_200_get_a_user(self):
        pass

    def test_200_get_nonexistant(self):
        pass

    def test_200_login(self):
        pass

    def test_400_login_missing_info(self):
        pass

    def test_400_login_nonexistant(self):
        pass

    def test_400_login_invalid_pass(self):
        pass

    def test_200_get_me(self):
        pass

    def test_200_get_me(self):
        pass

    def test_200_update(self):
        pass

    def test_400_update_fail(self):
        pass

    def test_200_delete(self):
        pass


if __name__ == "__main__":
    env_name = os.getenv('FLASK_ENV')
    route_1 = "/"
    route_2 = "/api/users/"
    route_3 = "/api/users/login"
    route_4 = "/api/users/me"

    unittest.main()
