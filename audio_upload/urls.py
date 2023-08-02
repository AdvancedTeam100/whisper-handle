from django.urls import path
from . import views
from whisperHandle import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', views.create_upload, name = 'create'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
