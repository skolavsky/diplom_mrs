import uuid
from datetime import date
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import BooleanField
from django.db.models.signals import post_save
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

    def save(self, *args, **kwargs):
        # Проверка наличия записи перед получением значений полей
        if self.pk is not None:
            previous_record = self.__class__.objects.filter(pk=self.pk).first()
            if previous_record:
                previous_spo2_fio = previous_record.spo2_fio
                previous_rox = previous_record.rox
            else:
                previous_spo2_fio = None
                previous_rox = None
        else:
            previous_spo2_fio = None
            previous_rox = None

        # Проверка, изменились ли поля spo2_fio и rox
        spo2_fio_changed = self.spo2_fio != previous_spo2_fio if previous_spo2_fio is not None else True
        rox_changed = self.rox != previous_rox if previous_rox is not None else True

        if rox_changed and self.rox is not None and self.result in [0, 'in progress']:
            # Получаем ближайшие 10 записей с rox меньше или равным введенному значению, исключая записи с результатом 0 "in progress"
            lower_records = ClientData.objects.filter(rox__lte=self.rox, result__in=[1, 2, 3]).exclude(
                result=0).order_by('-rox')[:10]
            # Получаем ближайшие 10 записей с rox больше введенного значения, исключая записи с результатом 0 "in progress"
            higher_records = ClientData.objects.filter(rox__gt=self.rox, result__in=[1, 2, 3]).exclude(
                result=0).order_by('rox')[:10]

            # Собираем значения week_result для найденных записей
            week_results = [record.week_result for record in lower_records] + [record.week_result for record in
                                                                               higher_records]
            # Вычисляем среднее значение week_result
            if week_results:
                # Вычисляем процент истинных значений в week_results
                true_count = sum(1 for result in week_results if result)
                average_week_result = true_count / len(week_results)
                self.forecast_for_week = int(average_week_result * 100)  # Приводим к процентам

        # Вычисление значения группы на основе spo2_fio и rox только если они изменились
        if spo2_fio_changed and rox_changed and self.spo2_fio is not None and self.rox is not None:
            if self.spo2_fio >= 280 and self.rox >= 15:
                self.group = 1
            elif self.spo2_fio < 315 and self.rox < 15:
                self.group = 2
            elif 230 <= self.spo2_fio < 315 and 11 <= self.rox < 15:
                self.group = 3
            elif self.spo2_fio < 280 and self.rox < 15:
                self.group = 4
            else:
                self.group = 0  # Группа для записей без spo2_fio и rox

        # Вызов метода save родительского класса для сохранения модели
        super().save(*args, **kwargs)

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
