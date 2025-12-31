import unittest
from run import app
from app.extensions import db
from app.models import Mechanic


class MechanicTests(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()
        self.client.testing = True

        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    # =========================
    # CREATE MECHANIC
    # =========================
    def test_create_mechanic(self):
        response = self.client.post("/mechanics/", json={
            "name": "Mike",
            "specialty": "Brakes"
        })
        self.assertEqual(response.status_code, 201)

    # =========================
    # GET MECHANICS
    # =========================
    def test_get_mechanics(self):
        self.client.post("/mechanics/", json={
            "name": "Sarah",
            "specialty": "Engines"
        })

        response = self.client.get("/mechanics/")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.get_json()) > 0)

    # =========================
    # UPDATE MECHANIC
    # =========================
    def test_update_mechanic(self):
        create = self.client.post("/mechanics/", json={
            "name": "Tom",
            "specialty": "Electrical"
        })

        mechanic_id = create.get_json()["id"]

        response = self.client.put(
            f"/mechanics/{mechanic_id}",
            json={"specialty": "Suspension"}
        )

        self.assertEqual(response.status_code, 200)

    # =========================
    # DELETE MECHANIC
    # =========================
    def test_delete_mechanic(self):
        create = self.client.post("/mechanics/", json={
            "name": "Delete Me",
            "specialty": "General"
        })

        mechanic_id = create.get_json()["id"]

        response = self.client.delete(f"/mechanics/{mechanic_id}")
        self.assertEqual(response.status_code, 200)

    # =========================
    # NEGATIVE TEST
    # =========================
    def test_update_mechanic_not_found(self):
        response = self.client.put("/mechanics/9999", json={
            "name": "Ghost"
        })
        self.assertEqual(response.status_code, 404)
