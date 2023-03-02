from users.models import ImageProfile, Profiles, Images
from .serializers import ImagesBasicUserSerializer, ImagesPremiumUserSerializer, ImagesEnterpriseUserSerializer, \
    LinkSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from django.core.signing import Signer
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from datetime import datetime, timedelta
from rest_framework.decorators import api_view, action
from rest_framework.response import Response


class ImagesViewSet(APIView):
    queryset = ImageProfile.objects.all()
    serializer_class = ImagesBasicUserSerializer

    @action(methods=['GET'], detail=False)
    def list(self, request):
        serializer_class = self.get_serializer_class()
        queryset = self.filter_queryset(self.get_queryset())
        serializer = serializer_class(queryset, many=True)

        return Response(serializer.data)

    def get_user(self):
        user = self.request.user
        try:
            profile = Profiles.objects.get(user=user)
            user.membership = profile.membership
        except Profiles.DoesNotExist:
            user.membership = 'BASIC'
        return user

    def get_serializer_class(self):
        user = self.get_user()
        input(user)
        if user.membership == 'Basic':
            return ImagesBasicUserSerializer
        if user.membership == 'Premium':
            return ImagesPremiumUserSerializer
        if user.membership == 'Enterprise':
            return ImagesEnterpriseUserSerializer
        input(user)

    def get_queryset(self):

        user = self.get_user()
        return Profiles.objects.filter(user=user)


# Widok do generowania linku
@api_view(['POST'])
def create_link(request):
    serializer = LinkSerializer(data=request.data)
    if serializer.is_valid():
        signer = Signer()
        expire_seconds = serializer.validated_data['expire_seconds']
        url = reverse('my_view_name')
        signature = signer.sign(url)
        signed_url = urlsafe_base64_encode(force_bytes(signature))
        expire_date = datetime.now() + timedelta(seconds=expire_seconds)
        data = {
            'link': signed_url,
            'expire_date': expire_date
        }
        return Response(data)
    else:
        return Response(serializer.errors, status=400)


# Widok do weryfikacji linku
@api_view(['GET'])
def verify_link(request, signed_url):
    signer = Signer()
    try:
        signature = signer.unsign(urlsafe_base64_decode(signed_url))
        if request.session.get('signed_url') == signed_url and datetime.now() < request.session.get('expire_date'):
            data = {
                'status': 'OK',
                'url': reverse(signature)
            }
            return Response(data)
        else:
            return Response({'status': 'ERROR', 'message': 'Nieprawidłowy lub wygasły link'}, status=400)
    except signer.BadSignature:
        return Response({'status': 'ERROR', 'message': 'Nieprawidłowy link'}, status=400)
