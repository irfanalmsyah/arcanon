from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path("chat/<str:room_name>/", login_required(views.RoomView.as_view()), name="room"),
    path("request/", login_required(views.RequesterView.as_view()), name="request"),
    path("respond/", login_required(views.ResponderView.as_view()), name="respond"),
]