from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from PIL import Image


# model do zapisywania zdjec
class Images(models.Model):
    objects = None
    title = models.CharField(max_length=250)
    image = models.ImageField(upload_to='profile_pics')
    created = models.DateTimeField(default=timezone.now())
    image_200 = models.ImageField(upload_to='profile_pics')
    image_400 = models.ImageField(upload_to='profile_pics')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img_200 = Image.open(self.image.path)
        img_400 = Image.open(self.image.path)

        output_size_200 = (200, 200)
        output_size_400 = (400, 400)
        img_200.thumbnail(output_size_200)
        img_400.thumbnail(output_size_400)
        img_200.save(self.image_200.path)
        img_400.save(self.image_400.path)

# model dla 3 typow uzytkownikow

class Profiles(models.Model):

    USER_TYPES = (
        ('BASIC', 'Basic'),
        ('PREMIUM', 'Premium'),
        ('ENTERPRISE', 'Enterprise')
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    membership = models.CharField(max_length=10, choices=USER_TYPES, default='BASIC')

    def __str__(self):
        return f"{self.user.username} {self.membership} Profile"