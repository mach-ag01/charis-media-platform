from decimal import Decimal
from django.test import TestCase
from rest_framework.test import APIClient
from bookings.models import Booking

class BookingAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.payload = {
            "full_name": "Test Client", "phone": "+254700000000",
            "email": "client@example.com", "services": ["photography"],
            "packages": ["gold"], "coverage_zone": "nairobi",
            "data_protection_consent": True,
            "production_exclusivity_ack": True,
            "financial_terms_ack": True,
        }

    def test_client_can_submit_booking(self):
        response = self.client.post("/api/bookings/", self.payload, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Booking.objects.count(), 1)
        self.assertEqual(response.data["status"], "new")

    def test_required_acknowledgements_are_enforced(self):
        payload = {**self.payload, "financial_terms_ack": False}
        response = self.client.post("/api/bookings/", payload, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Booking.objects.count(), 0)

    def test_quote_calculates_70_30_payment_milestones(self):
        booking = Booking.objects.create(**self.payload, quote_amount=Decimal("10000.00"))
        self.assertEqual(booking.deposit_amount, Decimal("7000.00"))
        self.assertEqual(booking.balance_amount, Decimal("3000.00"))

    def test_dashboard_counts_bookings(self):
        Booking.objects.create(**self.payload)
        response = self.client.get("/api/dashboard/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["total_bookings"], 1)
