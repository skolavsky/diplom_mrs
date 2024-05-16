import uuid
from datetime import date

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import BooleanField
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.urls import reverse
from simple_history.models import HistoricalRecords


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
        return reverse('clients:client_detail', args=[str(self.id)])

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = uuid.uuid4()
        super().save(*args, **kwargs)

    def get_gender_display(self):
        return dict(self.GENDER_CHOICES).get(self.gender, 'не выбран')

    def __str__(self):
        return f"{self.last_name} {self.first_name} {self.patronymic} "


def validate_integer_size(value):
    if value < 0 or value > 4:
        raise ValidationError('Значение должно быть в диапазоне от 0 до 4')


def validate_forecast(value):
    if value < 0 or value > 100:
        raise ValidationError('Значение должно быть в диапазоне от 0 до 100')


class ClientData(models.Model):
    RESULT_CHOICES = [
        (0, 'processing'),
        (1, 'D'),
        (2, 'H'),
        (3, 'R'),
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
    ventilation_reserve = models.FloatField(null=True, blank=True)
    comorb_ccc = models.BooleanField(default=False, blank=True)
    comorb_bl = models.BooleanField(default=False, blank=True)
    cd_ozhir = models.BooleanField(default=False, blank=True)
    comorb_all = models.BooleanField(default=False, blank=True)
    l_109 = models.FloatField(null=True, blank=True)
    lf = models.FloatField(null=True, blank=True)
    rox = models.FloatField(null=True, blank=True)
    spo2_fio = models.FloatField(null=True, blank=True)
    ch_d = models.IntegerField(null=True, blank=True)
    group = models.IntegerField(null=True, blank=True, validators=[validate_integer_size])
    measurementday = models.IntegerField(null=True, blank=True)
    daystoresult = models.IntegerField(null=True, blank=True)
    week_result = models.BooleanField(default=False, blank=True)
    forecast_for_week = models.IntegerField(null=True, blank=True, validators=[validate_forecast])

    users_note = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                        related_name='clients_noted',
                                        blank=True)

    history = HistoricalRecords(inherit=True)

    def spo2_fio_changed(self):
        """
        Проверяет, изменилось ли значение spo2_fio.
        """
        try:
            old_instance = ClientData.objects.get(pk=self.pk)
            return True if old_instance.spo2_fio != self.spo2_fio else False
        except ClientData.DoesNotExist:
            return False

    def rox_changed(self):
        """
        Проверяет, изменилось ли значение rox.
        """
        try:
            old_instance = ClientData.objects.get(pk=self.pk)
            print(old_instance)
            print(ClientData.objects.get(pk=self.pk))
            return True if old_instance.rox != self.rox else False
        except ClientData.DoesNotExist:
            return False

    @property
    def has_personal_info(self):
        return self.personal_info is not None


@receiver(pre_save, sender=ClientData)
def update_group(sender, instance, **kwargs):
    if instance.spo2_fio is not None and instance.rox is not None:
        if instance.spo2_fio >= 280 and instance.rox >= 15:
            instance.group = 1
        elif instance.spo2_fio < 315 and instance.rox < 15:
            instance.group = 2
        elif 230 <= instance.spo2_fio < 315 and 11 <= instance.rox < 15:
            instance.group = 3
        elif instance.spo2_fio < 280 and instance.rox < 15:
            instance.group = 4
        else:
            instance.group = 0  # Группа для записей без spo2_fio и rox
    else:
        instance.group = None  # или другое значение, обозначающее отсутствие данных



@receiver(post_save, sender=ClientData)
def create_personal_info(sender, instance, created, **kwargs):
    if created and not instance.has_personal_info:
        PersonalInfo.objects.create()


@receiver(post_save, sender=ClientData)
def save_personal_info(sender, instance, **kwargs):
    if instance.has_personal_info:
        instance.personal_info.save()
