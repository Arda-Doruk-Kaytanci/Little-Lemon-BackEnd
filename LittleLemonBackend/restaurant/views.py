# from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import logout as auth_logout
from .forms import BookingForm
from .models import Menu, Booking
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core import serializers
from .models import Booking
from django.core.exceptions import PermissionDenied
from datetime import datetime
import json
from .serializer import MenuSerializer, BookingSerializer
from rest_framework import generics
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render
from datetime import date, datetime
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated


# Create your views here.
def home(request):
    return render(request, "index.html")


def about(request):
    return render(request, "about.html")


def is_superuser(user):
    if not user.is_superuser:
        raise PermissionDenied
    return True


@user_passes_test(is_superuser)
@login_required
def reservations(request):
    date = request.GET.get("date", datetime.today().date())
    bookings = Booking.objects.all()
    booking_json = serializers.serialize("json", bookings)
    return render(request, "bookings.html", {"bookings": booking_json})


def get_hour_from_time(time_str):
    time_obj = datetime.strptime(time_str, "%H:%M")
    return time_obj.hour


@csrf_protect
def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            response = redirect("home")
            return response
        else:
            return render(request, "login.html", {"error": "Invalid credentials"})

    return render(request, "login.html")


def book(request):
    times = [
        "08:00",
        "09:00",
        "10:00",
        "11:00",
        "12:00",
        "13:00",
        "14:00",
        "15:00",
        "16:00",
        "17:00",
        "18:00",
        "19:00",
        "20:00",
    ]
    form = BookingForm()
    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            form.save()
    context = {
        "form": form,
        "date": date.today().strftime("%Y-%m-%d"),
        "times": [(get_hour_from_time(time), time) for time in times],
    }
    return render(request, "book.html", context)


def menu(request):
    menu_data = Menu.objects.all()
    main_data = {"menu": menu_data}
    return render(request, "menu.html", {"menu": main_data})


def display_menu_item(request, pk=None):
    if pk:
        menu_item = Menu.objects.get(pk=pk)
    else:
        menu_item = ""
    return render(request, "menu_item.html", {"menu_item": menu_item})


@csrf_exempt
def bookings(request):
    if request.method == "POST":
        data = json.load(request)
        exist = (
            Booking.objects.filter(reservation_date=data["reservation_date"])
            .filter(reservation_slot=data["reservation_slot"])
            .exists()
        )
        if exist == False:
            booking = Booking(
                first_name=data["first_name"],
                reservation_date=data["reservation_date"],
                reservation_slot=data["reservation_slot"],
            )
            booking.save()
        else:
            return HttpResponse("{'error':1}", content_type="application/json")

    date = request.GET.get("date", datetime.today().date())

    bookings = Booking.objects.all().filter(reservation_date=date)
    booking_json = serializers.serialize("json", bookings)

    return HttpResponse(booking_json, content_type="application/json")


@login_required
@csrf_protect
def user_logout(request):
    auth_logout(request)
    response = redirect("login")
    return response


@user_passes_test(is_superuser)
@login_required
class MenuView(generics.ListCreateAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    search_fields = ["name"]


@user_passes_test(is_superuser)
@login_required
class BookView(generics.ListCreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer


class SecretMessage(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        return Response({"message": "Wow You found the secret part congrats"}, status=status.HTTP_200_OK)
