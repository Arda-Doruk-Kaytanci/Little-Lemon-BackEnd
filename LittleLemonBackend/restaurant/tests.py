from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect


class ReservationsViewTestCaseUnAuth(TestCase):

    def setUp(self):    
        self.user = User.objects.create_user(username="testuser", password="testpass")

    def test_reservations_view_redirects_unauthenticated_user(self):
        response = self.client.get(reverse("reservations"))
        self.assertEqual(response.status_code, HttpResponseRedirect.status_code)
        self.assertRedirects(
            response, f'/accounts/login/?next={reverse("reservations")}'
        )


class ReservationsViewTestCaseNonSuper(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")

    def test_reservations_view_denied_for_non_superuser(self):
        self.client.login(username="testuser", password="testpass")
        response = self.client.get(reverse("reservations"))
        self.assertEqual(response.status_code, 403)


class ReservationsViewTestCaseForSuper(TestCase):

    def setUp(self):
        self.superuser = User.objects.create_superuser(
            username="superuser", password="superpass"
        )

    def test_reservations_view_accessible_for_superuser(self):
        self.client.login(username="superuser", password="superpass")
        response = self.client.get(reverse("reservations"))
        self.assertEqual(response.status_code, 200)  # OK
