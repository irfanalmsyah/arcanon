from django.urls import path, include

urlpatterns = [
    path('', include('main.urls')),
    path('chat/', include('chat.urls')),
    path('forum/', include('forum.urls')),
]
