# web_handler.models.py
from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User
import uuid
from django.dispatch import receiver
from django.conf import settings
from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator, MaxValueValidator
from PIL import Image
import os
from django.core.files.base import ContentFile


class Article(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = uuid.uuid4()
        super(Article, self).save(*args, **kwargs)


def user_directory_path(instance, filename):
    return 'user_{0}/avatar/{1}'.format(instance.user.id, filename)


def validate_image(image):
    file_size = image.file.size
    limit_mb = 2
    if file_size > limit_mb * 1024 * 1024:
        raise ValidationError("Max file size is %sMB" % limit_mb)
    else:
        img = Image.open(image)
        width, height = img.size
        max_width = 800
        max_height = 600
        if width > max_width or height > max_height:
            raise ValidationError("Max dimensions allowed are {0}x{1} pixels".format(max_width, max_height))


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    telegram_id = models.TextField(max_length=100, blank=True)
    is_white_list = models.BooleanField(default=False)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    avatar = models.ImageField(upload_to=user_directory_path, blank=True, null=True,
                               validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png']),
                                           MaxValueValidator(2 * 1024 * 1024), validate_image])

    def save(self, *args, **kwargs):
        if self.avatar:
            if isinstance(self.avatar, ContentFile):
                # Получаем имя файла
                file_name = os.path.basename(self.avatar.name)
                # Получаем содержимое файла
                file_content = self.avatar.read()
                # Записываем содержимое файла обратно в поле аватара
                self.avatar.save(file_name, ContentFile(file_content), save=False)
        super().save(*args, **kwargs)


@receiver(post_save, sender=get_user_model())
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=get_user_model())
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
