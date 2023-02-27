from django.urls import path
from .views import ImagesViewSet
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('api/', ImagesViewSet.as_view(), name='get_api'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)