import uuid
from datetime import date

import requests
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import BooleanField
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.urls import reverse
from encrypted_model_fields.fields import EncryptedCharField, EncryptedBooleanField
from mrs_proj.settings_common import FORECAST_URL
from simple_history.models import HistoricalRecords
from auditlog.registry import auditlog
from auditlog.models import AuditlogHistoryField


class PersonalInfo(models.Model):
    GENDER_CHOICES = [
        (False, 'Женский'),
        (True, 'Мужской'),
    ]

    first_name = EncryptedCharField(max_length=100)
    last_name = EncryptedCharField(max_length=100)
    patronymic = EncryptedCharField(max_length=100, blank=True)
    gender = EncryptedBooleanField(default=True, choices=GENDER_CHOICES)
    is_active: BooleanField = models.BooleanField(default=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    history = AuditlogHistoryField()

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

    oxygen_flow = models.FloatField(null=True, blank=True, default=0)  # поток кислорода (литры в минуту)

    mvv = models.FloatField(null=True, blank=True, default=0)  # МВЛ ???
    mv = models.FloatField(null=True, blank=True, default=0)  # МОД ???

    age = models.IntegerField(null=False, blank=True, default=0)
    body_mass_index = models.FloatField(null=True, blank=True)
    spo2 = models.IntegerField(null=True, blank=True)
    admission_date = models.DateField(default=date.today, null=False, blank=True)
    result = models.IntegerField(choices=RESULT_CHOICES, default=0, blank=False)
    dayshome = models.IntegerField(null=True, blank=True)
    f_test_ex = models.IntegerField(null=True, blank=True)
    f_test_in = models.IntegerField(null=True, blank=True)
    ventilation_reserve = models.FloatField(null=True, blank=True, default=0)  # pb (mvv / mv)
    comorb_ccc = models.BooleanField(default=False, blank=True)
    comorb_bl = models.BooleanField(default=False, blank=True)
    cd_ozhir = models.BooleanField(default=False, blank=True)
    comorb_all = models.BooleanField(default=False, blank=True)
    l_109 = models.FloatField(null=True, blank=True)
    lf = models.FloatField(null=True, blank=True)
    rox = models.FloatField(null=True, blank=True)  # rox = (spo2_fio / ch_d)
    spo2_fio = models.FloatField(null=True, blank=True)  # spo2 / (21+3*oxygen_flow) / 100
    ch_d = models.IntegerField(null=True, blank=True, default=0)  # частота дыхания
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
def calculate_values(sender, instance, **kwargs):
    # Проверяем, что поля spo2 и oxygen_flow не равны None для расчета spo2_fio
    if instance.spo2 is not None and instance.oxygen_flow is not None:
        instance.spo2_fio = round(instance.spo2 / ((21 + 3 * instance.oxygen_flow) / 100), 3)
    else:
        instance.spo2_fio = None  # Или другое значение, которое имеет смысл в случае отсутствия данных

    # Проверяем, что поля spo2_fio и ch_d не равны None и ch_d не равен 0 для расчета rox
    if instance.spo2_fio is not None and instance.ch_d is not None and instance.ch_d != 0:
        instance.rox = round(instance.spo2_fio / instance.ch_d, 3)
    else:
        instance.rox = None  # Или другое значение, которое имеет смысл в случае отсутствия данных


@receiver(pre_save, sender=ClientData)
def calculate_ventilation_reserve(sender, instance, **kwargs):
    """
    Calculates ventilation_reserve if MVV or MV are changed and not None or zero.
    """
    if instance.mvv is not None and instance.mv is not None and instance.mv != 0:
        instance.ventilation_reserve = round(instance.mvv / instance.mv, 3)
    else:
        instance.ventilation_reserve = None  # Или другое значение, обозначающее отсутствие данных


@receiver(pre_save, sender=ClientData)
def update_forecast(sender, instance, **kwargs):
    try:
        previous_instance = sender.objects.get(pk=instance.pk)
    except sender.DoesNotExist:
        # Если экземпляр создается впервые, нет необходимости в обновлении прогноза
        return

    if instance.ventilation_reserve != previous_instance.ventilation_reserve and instance.ventilation_reserve != 0:
        url = FORECAST_URL + str(instance.ventilation_reserve)
        try:
            response = requests.get(url)
            if response.status_code == 200:
                result = response.json().get('result')
                # Преобразование значения в проценты
                percent_value = max(min((result * 100), 90), 10)
                instance.forecast_for_week = percent_value
            else:
                # Оставляем старое значение, если запрос завершился неудачно
                instance.forecast_for_week = previous_instance.forecast_for_week
        except requests.RequestException as e:
            # Оставляем старое значение в случае ошибки запроса
            instance.forecast_for_week = previous_instance.forecast_for_week
            print(f"Error fetching data from {url}: {e}")


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


# регистрация для модели логирования
auditlog.register(ClientData)
auditlog.register(PersonalInfo)
