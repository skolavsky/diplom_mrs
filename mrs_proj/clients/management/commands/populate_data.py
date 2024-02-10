from django.core.management.base import BaseCommand
from django.utils.crypto import get_random_string
from clients.models import PersonalInfo, ClientData
from faker import Faker
import uuid
import secrets

fake = Faker('ru_RU')


class Command(BaseCommand):
    help = 'Populate the database with fake data for ClientData model'

    def add_arguments(self, parser):
        parser.add_argument(
            'count',
            type=int,
            nargs='?',
            default=10,
            help='Number of records to create (1 to 100)',
            choices=range(1, 101),
            metavar='COUNT'
        )

    def handle(self, *args, **options):
        count = options['count']

        for _ in range(count):
            # Создаем объект PersonalInfo
            personal_info = PersonalInfo.objects.create(
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                patronymic=fake.middle_name(),
                gender=fake.random_element(elements=[0, 1]),

            )

            # Создаем объект ClientData с ссылкой на PersonalInfo
            ClientData.objects.create(
                personal_info=personal_info,
                age=fake.random_int(min=18, max=80),
                body_mass_index=fake.pyfloat(min_value=0, max_value=100.0, right_digits=3),
                spo2=fake.random_int(min=90, max=100),
                admission_date=fake.date_between(start_date='-60d', end_date='today'),
                result=fake.random_int(min=0, max=3),
                dayshome=fake.random_int(min=1, max=30),
                f_test_ex=fake.random_int(min=0, max=200),
                f_test_in=fake.random_int(min=0, max=200),
                comorb_ccc=fake.random_element(elements=[True, False]),
                comorb_bl=fake.random_element(elements=[True, False]),
                cd_ozhir=fake.random_element(elements=[True, False]),
                comorb_all=fake.random_element(elements=[True, False]),
                l_109=fake.pyfloat(min_value=0, max_value=50.0, right_digits=3),
                lf=fake.pyfloat(min_value=0, max_value=50.0, right_digits=3),
                rox=fake.pyfloat(min_value=0, max_value=50.0, right_digits=3),
                spo2_fio=fake.pyfloat(min_value=0, max_value=600.0, right_digits=3),
                ch_d=fake.random_int(min=0, max=150),
            )

        self.stdout.write(self.style.SUCCESS(f'Successfully populated the database with {count} ClientData test data'))
