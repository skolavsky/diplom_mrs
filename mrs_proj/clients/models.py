from django.db import models
import uuid
from django.db.models import BooleanField
from django.urls import reverse
from simple_history.models import HistoricalRecords
from datetime import date
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class PersonalInfo(models.Model):
    GENDER_CHOICES = [
        (False, 'Женский'),
        (True, 'Мужской'),
    ]

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    patronymic = models.CharField(max_length=100, blank=True)
    gender: BooleanField = models.BooleanField(default=True, choices=GENDER_CHOICES)
    is_active: BooleanField = models.BooleanField(default=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    def get_absolute_url(self):
        return reverse('client_detail', args=[str(self.id)])

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = uuid.uuid4()
        super().save(*args, **kwargs)

    def get_gender_display(self):
        return dict(self.GENDER_CHOICES).get(self.gender, 'не выбран')

    def __str__(self):
        return f"{self.last_name} {self.first_name} {self.patronymic} "


class ClientData(models.Model):
    RESULT_CHOICES = [
        (0, 'В процессе'),
        (1, 'Значение 1'),
        (2, 'Значение 2'),
        (3, 'Значение 3'),
    ]

    personal_info = models.OneToOneField(PersonalInfo, null=True, blank=True, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)
    date_last_modified = models.DateTimeField(auto_now=True)

    age = models.IntegerField(null=False, blank=True, default=0)
    body_mass_index = models.FloatField(null=True, blank=True)
    spo2 = models.IntegerField(null=True, blank=True)
    admission_date = models.DateField(default=date.today, null=False, blank=True)
    result = models.IntegerField(choices=RESULT_CHOICES, default=0, blank=False)
    dayshome = models.IntegerField(null=True, blank=True)
    f_test_ex = models.IntegerField(null=True, blank=True)
    f_test_in = models.IntegerField(null=True, blank=True)
    comorb_ccc = models.BooleanField(default=False, blank=True)
    comorb_bl = models.BooleanField(default=False, blank=True)
    cd_ozhir = models.BooleanField(default=False, blank=True)
    comorb_all = models.BooleanField(default=False, blank=True)
    l_109 = models.FloatField(null=True, blank=True)
    lf = models.FloatField(null=True, blank=True)
    rox = models.FloatField(null=True, blank=True)
    spo2_fio = models.FloatField(null=True, blank=True)
    ch_d = models.IntegerField(null=True, blank=True)

    history = HistoricalRecords(inherit=True)

    @property
    def has_personal_info(self):
        return self.personal_info is not None


@receiver(post_save, sender=ClientData)
def create_personal_info(sender, instance, created, **kwargs):
    if created and not instance.has_personal_info:
        PersonalInfo.objects.create()


@receiver(post_save, sender=ClientData)
def save_personal_info(sender, instance, **kwargs):
    if instance.has_personal_info:
        instance.personal_info.save()
