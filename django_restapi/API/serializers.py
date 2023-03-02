from rest_framework import serializers
from users.models import ImageProfile, Images


class ImagesBasicUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Images
        fields = ('user', 'title', 'image_200')


class ImagesPremiumUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Images
        fields = ('user', 'title', 'image_200', 'image_400', 'image')


class ImagesEnterpriseUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Images
        fields = ('user', 'title', 'image_200', 'image_400', 'image')


# Serializator do walidacji danych wejściowych
class LinkSerializer(serializers.Serializer):
    expire_seconds = serializers.IntegerField(min_value=30, max_value=30000)
