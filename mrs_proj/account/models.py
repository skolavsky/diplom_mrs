from django.conf import settings
from django.db import models
from easy_thumbnails.fields import ThumbnailerImageField


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = ThumbnailerImageField(upload_to='users/%Y/%m/%d/', blank=True)
    def __str__(self):
        return f'Profile of {self.user.username}'
