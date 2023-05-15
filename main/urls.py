from django.urls import path, include
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path("", login_required(views.IndexView.as_view()), name="home"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", login_required(views.LogoutView.as_view()), name="logout"),
    path("register/", views.RegisterView.as_view(), name="register"),
    path("settings/", login_required(views.SettingsView.as_view()), name="settings"),
    path("profile/", login_required(views.ProfileView.as_view()), name="profile"),
    path("profile/likes/", login_required(views.ProfileLikeView.as_view()), name="profile_likes"),
    path("profile/comments/", login_required(views.ProfileCommentView.as_view()), name="profile_comments"),
    path("top/", login_required(views.TopPostsView.as_view()), name="top"),
]