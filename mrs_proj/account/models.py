from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone
from easy_thumbnails.fields import ThumbnailerImageField
from auditlog.registry import auditlog
from auditlog.models import AuditlogHistoryField


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = ThumbnailerImageField(upload_to='users/%Y/%m/%d/', blank=True)
    password_changed_at = models.DateTimeField(auto_now_add=True)
    history = AuditlogHistoryField()

    def __str__(self):
        return f'Profile of {self.user.username}'

    @receiver(pre_save, sender=User)
    def update_password_changed_at(sender, instance, **kwargs):
        # Check if the password is being changed
        if instance.pk:
            old_instance = sender.objects.get(pk=instance.pk)
            if instance.password != old_instance.password:
                # Password is being changed, update password_changed_at
                instance.profile.password_changed_at = timezone.now()
                instance.profile.save()


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


auditlog.register(Profile)
