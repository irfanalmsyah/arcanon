from django.urls import path, include
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path("", login_required(views.IndexView.as_view()), name="index"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", login_required(views.LogoutView.as_view()), name="logout"),
    path("register/", views.RegisterView.as_view(), name="register"),
    path("settings/", login_required(views.SettingsView.as_view()), name="settings"),
]