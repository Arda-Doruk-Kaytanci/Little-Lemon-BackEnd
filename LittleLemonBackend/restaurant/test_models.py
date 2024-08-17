from django.test import TestCase
from .models import Booking, Menu


class BookingModelTest(TestCase):
    def setUp(self):
        self.booking = Booking.objects.create(
            first_name="John Doe", reservation_date="2024-08-17", reservation_slot=12
        )

    def test_booking_creation(self):
        self.assertEqual(self.booking.first_name, "John Doe")
        self.assertEqual(self.booking.reservation_date, "2024-08-17")
        self.assertEqual(self.booking.reservation_slot, 12)

    def test_booking_string_representation(self):
        self.assertEqual(str(self.booking), "John Doe")


class MenuModelTest(TestCase):
    def setUp(self):
        self.menu = Menu.objects.create(
            name="Cheeseburger",
            price=499,
            menu_item_description="A delicious cheeseburger with all the fixings.",
        )

    def test_menu_creation(self):
        self.assertEqual(self.menu.name, "Cheeseburger")
        self.assertEqual(self.menu.price, 499)
        self.assertEqual(
            self.menu.menu_item_description,
            "A delicious cheeseburger with all the fixings.",
        )

    def test_menu_string_representation(self):
        self.assertEqual(str(self.menu), "Cheeseburger")
