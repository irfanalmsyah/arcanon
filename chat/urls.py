from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path("room/<str:room_name>/", login_required(views.RoomView.as_view()), name="room"),
    path("room/", login_required(views.GetRoom.as_view()), name="get_room"),
    path("create/", login_required(views.CreateRoom.as_view()), name="create_room"),
    path("close/", login_required(views.CloseRoom.as_view()), name="close_room"),
]