import unittest
import os
from flask import json


from src.app import create_app

class ApiTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app(env_name)
        self.client = self.app.test_client

    # Route 1
    def test_200_ping(self):
        res = self.client().get(route_1)
        self.assertEqual(res.status_code, 200)
        self.assertTrue('End point working!!')

    def test_201_create(self):
        res = self.client().post(route_2, json=
                    {'name': 'tester', 'email': 'testing@gmail.com', 'password': 'abc123'})
        self.assertEqual(res.status_code, 201)


if __name__ == "__main__":
    env_name = os.getenv('FLASK_ENV')
    route_1 = "/"
    route_2 = "/api/users/"
    route_3 = "/api/users/login"
    route_4 = "/api/users/me"

    unittest.main()
