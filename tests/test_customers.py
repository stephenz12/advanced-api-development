import unittest
from run import app
from app.extensions import db


class CustomerTests(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()
        self.client.testing = True

        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_register_customer(self):
        response = self.client.post("/customers/", json={
            "name": "Test User",
            "email": "test@test.com",
            "password": "password123"
        })
        self.assertEqual(response.status_code, 201)

    def test_register_duplicate_email(self):
        self.client.post("/customers/", json={
            "name": "Test User",
            "email": "dup@test.com",
            "password": "password123"
        })

        response = self.client.post("/customers/", json={
            "name": "Test User",
            "email": "dup@test.com",
            "password": "password123"
        })

        self.assertEqual(response.status_code, 409)

    def test_login_customer(self):
        self.client.post("/customers/", json={
            "name": "Login User",
            "email": "login@test.com",
            "password": "password123"
        })

        response = self.client.post("/customers/login", json={
            "email": "login@test.com",
            "password": "password123"
        })

        self.assertEqual(response.status_code, 200)
        self.assertIn("token", response.get_json())
