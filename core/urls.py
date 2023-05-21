from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin

urlpatterns = [
    path('', include('main.urls')),
    path('report/', include('report.urls')),
    path('chat/', include('chat.urls')),
    path('forum/', include('forum.urls')),
    path('admin/', admin.site.urls),
]
+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
