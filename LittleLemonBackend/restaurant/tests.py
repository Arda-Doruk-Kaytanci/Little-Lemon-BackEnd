from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


class ReservationsViewTestCase(TestCase):

    def setUp(self):
        # Create test user and superuser
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.superuser = User.objects.create_superuser(
            username="superuser", password="superpass"
        )

    def test_reservations_view_redirects_unauthenticated_user(self):
        response = self.client.get(reverse("reservations"))
        self.assertEqual(response.status_code, 403)

    def test_reservations_view_denied_for_non_superuser(self):
        # Test that non-superusers receive a 403 Forbidden response
        self.client.login(username="testuser", password="testpass")
        response = self.client.get(reverse("reservations"))
        self.assertEqual(response.status_code, 403)  # Check for Forbidden response

    def test_reservations_view_accessible_for_superuser(self):
        # Test that superusers can access the view
        self.client.login(username="superuser", password="superpass")
        response = self.client.get(reverse("reservations"))
        self.assertEqual(response.status_code, 200)  # Check for OK response
