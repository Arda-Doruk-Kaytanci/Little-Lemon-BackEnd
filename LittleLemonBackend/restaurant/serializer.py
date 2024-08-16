from rest_framework import serializers
from .models import Booking, Menu
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model, authenticate


class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = [
            "name",
            "price",
            "menu_item_description",
            "id"
        ]
class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = [
            "first_name",
            "reservation_date",
            "reservation_slot",
            "id"
        ]