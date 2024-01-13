from django.core.management.base import BaseCommand
from clients.models import Client
from faker import Faker
import uuid
import secrets
from datetime import date

fake = Faker('ru_RU')  # Указываем локаль русского языка


class Command(BaseCommand):
    help = 'Populate the database with fake data for Client model'

    def add_arguments(self, parser):
        parser.add_argument(
            'count',
            type=int,
            nargs='?',  # Делаем аргумент необязательным
            default=10,  # Значение по умолчанию, если аргумент не передан
            help='Number of records to create (1 to 100)',
            choices=range(1, 101),  # Ограничиваем диапазон значений
            metavar='COUNT'
        )

    def handle(self, *args, **options):
        count = options['count']

        # Ограничим спектр значений
        gender_choices = [0, 1]
        comorb_choices = [True, False]

        # Логика для создания и сохранения тестовых записей
        for _ in range(count):
            Client.objects.create(
                id_token=secrets.token_urlsafe(32),
                id=uuid.uuid4(),
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                patronymic=fake.middle_name(),
                age=fake.random_int(min=18, max=80),
                body_mass_index=fake.pyfloat(min_value=0, max_value=100.0, right_digits=3),
                spo2=fake.random_int(min=90, max=100),
                admission_date=fake.date_between(start_date='-30d', end_date='today'),
                result=fake.random_int(min=0, max=100),
                dayshome=fake.random_int(min=1, max=30),
                gender=fake.random_element(elements=gender_choices),
                f_test_ex=fake.random_int(min=0, max=200),
                f_test_in=fake.random_int(min=0, max=200),
                comorb_ccc=fake.random_element(elements=comorb_choices),
                comorb_bl=fake.random_element(elements=comorb_choices),
                cd_ozhir=fake.random_element(elements=comorb_choices),
                comorb_all=fake.random_element(elements=comorb_choices),
                l_109=fake.pyfloat(min_value=0, max_value=50.0, right_digits=3),
                lf=fake.pyfloat(min_value=0, max_value=50.0, right_digits=3),
                rox=fake.pyfloat(min_value=0, max_value=50.0, right_digits=3),
                spo2_fio=fake.pyfloat(min_value=0, max_value=600.0, right_digits=3),
                ch_d=fake.random_int(min=0, max=150),
            )

        self.stdout.write(self.style.SUCCESS(f'Successfully populated the database with {count} Client test data'))
