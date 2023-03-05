from django.test import TestCase, SimpleTestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient, APITestCase
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.parsers import MultiPartParser
from .serializers import ImagesBasicUserSerializer

pytest_plugins = ["docker_compose"]

# Create your tests here.
class TestSuperuserCreation(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_superuser(self):
        # Define the data for the new superuser
        data = {
            "email": "test@example.com",
            "username": "test",
            "password": "testowe",
            "is_superuser": True,
            "is_staff": True,
        }

        # Send a POST request to create the new superuser
        response = self.client.post("/admin/", data=data, follow=True)

        # Check that the response status code is 200
        self.assertEqual(response.status_code, 200)

        # Check that the superuser was created successfully
        user = get_user_model()
        admin_user = user.objects.get(username="test")
        self.assertTrue(admin_user.is_superuser)
        self.assertTrue(admin_user.is_staff)


class TestImagesBasicUserSerializer(TestCase):
    def test_image_upload(self):
        image_file = SimpleUploadedFile(
            "test_image.jpg",
            b"binary data for test image",
            content_type="image/jpeg"
        )
        data = {"name": "Test Image", "image": image_file}
        serializer = ImagesBasicUserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
        else:
            self.fail(serializer.errors)

        # assert that the image was saved correctly
        self.assertIsNotNone(serializer.instance.pk)
        self.assertEqual(serializer.instance.name, "Test Image")
        self.assertEqual(serializer.instance.image.read(), b"binary data for test image")

        # cleanup the uploaded image file
        serializer.instance.image.delete()

    def test_image_serializer(self):
        parser_classes = (MultiPartParser,)
        serializer_class = ImagesBasicUserSerializer
        image_file = SimpleUploadedFile(
            "test_image.jpg",
            b"binary data for test image",
            content_type="image/jpeg"
        )
        data = {"name": "Test Image", "image": image_file}
        serializer = serializer_class(data=data, context={"request": None}, parser_classes=parser_classes)
        if serializer.is_valid():
            serializer.save()
        else:
            self.fail(serializer.errors)

        # assert that the serializer returns the expected data
        expected_data = {
            "id": serializer.instance.pk,
            "name": "Test Image",
            "image": serializer.instance.image.url
        }
        self.assertEqual(serializer.data, expected_data)

        # cleanup the uploaded image file
        serializer.instance.image.delete()