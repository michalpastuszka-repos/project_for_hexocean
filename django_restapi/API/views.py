from django_restapi.users.models import Images
from .serializers import ImagesBasicUserSerializer, ImagesPremiumUserSerializer, ImagesEnterpriseUserSerializer
from rest_framework import viewsets

class ImagesViewSet(viewsets.ModelViewSet):

    queryset = Images.objects.all()
    serializer_class = ImagesBasicUserSerializer

    def get_user(self):

        user = self.request.user
        return user

    def get_serializer_class(self):

        user = self.get_user()
        if user.membership == 'Basic':
            return ImagesBasicUserSerializer
        if user.membership == 'Premium':
            return ImagesPremiumUserSerializer
        if user.membership == 'Enterprise':
            return ImagesEnterpriseUserSerializer

    def get_queryset(self):

        user = self.get_user()
        return Images.objects.filter(author=user)
