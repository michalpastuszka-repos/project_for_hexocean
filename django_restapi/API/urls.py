from .views import  ImagesViewSet, create_link, verify_link
from django.urls import path, include
from rest_framework import routers



urlpatterns = [
    path('get_api/', ImagesViewSet.as_view(), name='get_api'),
    path('create_link/', create_link, name='create_link'),
    path('verify_link/<str:signed_url>/', verify_link, name='verify_link'),
]