import unittest
from run import app
from app.extensions import db


class ServiceTicketTests(unittest.TestCase):

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
    # CREATE SERVICE TICKET
    # =========================
    def test_create_service_ticket(self):
        response = self.client.post("/service-tickets/", json={
            "description": "Oil change",
            "customer_id": 1
        })
        self.assertEqual(response.status_code, 201)

    # =========================
    # GET SERVICE TICKETS
    # =========================
    def test_get_service_tickets(self):
        self.client.post("/service-tickets/", json={
            "description": "Brake inspection",
            "customer_id": 1
        })

        response = self.client.get("/service-tickets/")
        self.assertEqual(response.status_code, 200)

    # =========================
    # ASSIGN MECHANIC
    # =========================
    def test_assign_mechanic_to_ticket(self):
        mech = self.client.post("/mechanics/", json={
            "name": "Assign Me",
            "specialty": "Tires"
        })
        mechanic_id = mech.get_json()["id"]

        ticket = self.client.post("/service-tickets/", json={
            "description": "Flat tire",
            "customer_id": 1
        })
        ticket_id = ticket.get_json()["id"]

        response = self.client.put(
            f"/service-tickets/{ticket_id}/assign-mechanic/{mechanic_id}"
        )

        self.assertEqual(response.status_code, 200)

    # =========================
    # REMOVE MECHANIC
    # =========================
    def test_remove_mechanic_from_ticket(self):
        mech = self.client.post("/mechanics/", json={
            "name": "Remove Me",
            "specialty": "Engines"
        })
        mechanic_id = mech.get_json()["id"]

        ticket = self.client.post("/service-tickets/", json={
            "description": "Engine noise",
            "customer_id": 1
        })
        ticket_id = ticket.get_json()["id"]

        self.client.put(
            f"/service-tickets/{ticket_id}/assign-mechanic/{mechanic_id}"
        )

        response = self.client.put(
            f"/service-tickets/{ticket_id}/remove-mechanic/{mechanic_id}"
        )

        self.assertEqual(response.status_code, 200)

    # =========================
    # NEGATIVE TEST
    # =========================
    def test_assign_mechanic_not_found(self):
        response = self.client.put(
            "/service-tickets/9999/assign-mechanic/9999"
        )
        self.assertEqual(response.status_code, 404)
