from .views import ImagesViewSet, create_link
from django.urls import path, include
from rest_framework import routers


# router = routers.DefaultRouter()
# router.register(r'test/', ImagesViewSet, basename='test')
urlpatterns = [
    path('get_api/', ImagesViewSet.as_view(), name='get_api'),

    path('create_link/', create_link, name='link')
]