from rest_framework import serializers
from django_restapi.users.models import Images

class ImagesBasicUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = Images
        fields = ('author', 'title', 'image_200')


class ImagesPremiumUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = Images
        fields = ('author', 'title', 'image_200', 'image_400', 'image')

class ImagesEnterpriseUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = Images
        fields = ('author', 'title', 'image_200', 'image_400', 'image')

