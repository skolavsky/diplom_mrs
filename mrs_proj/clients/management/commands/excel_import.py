import pandas as pd
from django.core.management.base import BaseCommand
from faker import Faker  # Импорт Faker
from faker.providers import person  # Импорт провайдера person

from clients.models import PersonalInfo, ClientData

RESULT_MAPPING = {
    'D': 1,
    'H': 2,
    'R': 3,
    # Добавьте другие значения, если необходимо
}


class Command(BaseCommand):
    help = 'Загрузка данных из файла Excel в базу данных'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Путь к файлу Excel')

    def handle(self, *args, **kwargs):
        file_path = kwargs['file_path']
        self.excel_import(file_path)

    def excel_import(self, file_path):
        df = pd.read_excel(file_path)

        fake = Faker('ru_RU')
        fake.add_provider(person)  # Добавить провайдер person

        for index, row in df.iterrows():
            first_name = fake.first_name()
            last_name = fake.last_name()
            patronymic = fake.middle_name()
            gender = fake.boolean()

            result_value = RESULT_MAPPING.get(row['result'], 0)

            personal_info = PersonalInfo.objects.create(
                first_name=first_name,
                last_name=last_name,
                patronymic=patronymic,
                gender=gender,
            )

            client_data = ClientData.objects.create(
                personal_info=personal_info,
                age=row['age'],
                body_mass_index=row['body_mass_index'],
                f_test_ex=row['f_test_ex'],
                f_test_in=row['f_test_in'],
                comorb_ccc=row['comorb_ccc'],
                comorb_bl=row['comorb_bl'],
                cd_ozhir=row['cd_ozhir'],
                comorb_all=row['comorb_all'],
                l_109=row['l_109'],
                lf=row['lf'],
                rox=row['rox'],
                spo2=row['spo2'],
                spo2_fio=row['spo2_fio'],
                ch_d=row['ch_d'],
                measurementday=row['measurementday'],
                dayshome=row['dayshome'],
                result=result_value,
                week_result=row['week_result'],
                daystoresult=row['daystoresult'],
                # Добавьте остальные поля согласно вашим данным
            )

            self.stdout.write(
                self.style.SUCCESS(f"Созданы данные для {personal_info.first_name} {personal_info.last_name}"))
