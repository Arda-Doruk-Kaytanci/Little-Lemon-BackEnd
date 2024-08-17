from django.urls import path, include
from . import views
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("book/", views.book, name="book"),
    path("reservations/", views.reservations, name="reservations"),
    path("menu/", views.menu, name="menu"),
    path("menu_item/<int:pk>/", views.display_menu_item, name="menu_item"),
    path("bookings", views.bookings, name="bookings"),
    path("accounts/login", views.user_login, name="login"),
    path("logout", views.user_logout, name="logout"),
    path("api/menu", views.MenuView, name="menuapi"),
    path("api/book", views.BookView, name="bookapi"),
    path("api/auth/", include("djoser.urls")),
    path("api/auth/", include("djoser.urls.jwt")),
    path("api/token-auth/", obtain_auth_token, name="token_auth"),
]
