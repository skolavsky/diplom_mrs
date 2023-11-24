from django.db import models

# Create your models here.
from django.db import models

class Client(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    patronymic = models.CharField(max_length=100)
    age = models.IntegerField()
    body_mass_index = models.FloatField()
    SPO2 = models.IntegerField()
    admission_date = models.DateField()
    result = models.IntegerField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"