from django.db import models
import uuid
import secrets
from simple_history.models import HistoricalRecords


class Client(models.Model):
    GENDER_CHOICES = [
        (0, 'Female'),
        (1, 'Male'),
    ]

    exclude = ['user', 'age']

    token = models.CharField(max_length=100, default=secrets.token_urlsafe, unique=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    patronymic = models.CharField(max_length=100, blank=True)
    age = models.IntegerField(null=False)
    body_mass_index = models.FloatField(null=True, blank=True)
    spo2 = models.IntegerField(null=True, blank=True)
    admission_date = models.DateField(null=False)
    result = models.IntegerField(null=True, blank=True)
    gender = models.BooleanField(default=True, choices=GENDER_CHOICES)
    history = HistoricalRecords(inherit=True)

    # New Fields
    f_test_ex = models.IntegerField(null=True, blank=True)
    f_test_in = models.IntegerField(null=True, blank=True)
    comorb_ccc = models.BooleanField(default=False, blank=True)
    comorb_bl = models.BooleanField(default=False, blank=True)
    cd_ozhir = models.BooleanField(default=False, blank=True)
    comorb_all = models.BooleanField(default=False, blank=True)
    l_109 = models.FloatField(null=True, blank=True)
    lf = models.IntegerField(null=True, blank=True)
    rox = models.FloatField(null=True, blank=True)
    spo2_fio = models.FloatField(null=True, blank=True)
    ch_d = models.IntegerField(null=True, blank=True)

    def get_gender_display(self):
        return dict(self.GENDER_CHOICES).get(self.gender, 'Unknown')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

