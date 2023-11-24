from django.db import models
import uuid
import secrets


class Client(models.Model):
    GENDER_CHOICES = [
        (0, 'Female'),
        (1, 'Male'),
    ]

    exclude = ['user', 'age']

    token = models.CharField(max_length=100, default=secrets.token_urlsafe, unique=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    patronymic = models.CharField(max_length=100)
    age = models.IntegerField()
    body_mass_index = models.FloatField()
    SPO2 = models.IntegerField()
    admission_date = models.DateField()
    result = models.IntegerField()
    gender = models.BooleanField(default=False, choices=GENDER_CHOICES)

    def get_gender_display(self):
        return dict(self.GENDER_CHOICES).get(self.gender, 'Unknown')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
