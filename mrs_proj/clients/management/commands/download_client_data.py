from django.core.management.base import BaseCommand
from clients.models import ClientData, PersonalInfo
from datetime import date
import pandas as pd
import uuid
import xml.etree.ElementTree as ET
import os


class Command(BaseCommand):
    help = 'Download selected client data in various formats'

    def add_arguments(self, parser):
        parser.add_argument('format', type=str, help='Format of the file (excel/csv/json/xml)')
        parser.add_argument('personal_info_ids', nargs='*', type=uuid.UUID, help='UUIDs of the selected PersonalInfo')
        parser.add_argument('--all', action='store_true', help='Download all client data')
        parser.add_argument('--file', type=str, help='Path and name of the file')

    def handle(self, *args, **kwargs):
        format_type = kwargs['format']
        personal_info_ids = kwargs['personal_info_ids']
        download_all = kwargs['all']
        filename = kwargs['file'] if kwargs['file'] else 'data'

        if download_all:
            queryset = ClientData.objects.all()
        elif personal_info_ids:
            queryset = ClientData.objects.filter(personal_info_id__in=personal_info_ids)
        else:
            self.stdout.write(self.style.ERROR('No personal info IDs provided.'))
            return

        # Определяем список полей, которые нужно включить в запрос
        fields = ['age', 'body_mass_index', 'spo2', 'admission_date', 'result', 'dayshome', 'rox',
                  'f_test_ex', 'f_test_in', 'comorb_ccc', 'comorb_bl', 'cd_ozhir', 'ch_d', 'lf', 'l_109', 'spo2_fio']

        data = queryset.values(*fields)
        df = pd.DataFrame(data)

        if format_type == 'excel':
            filename += '.xlsx'
            # Запись DataFrame в файл Excel
            df.to_excel(filename, index=False, engine='openpyxl')
        elif format_type == 'csv':
            filename += '.csv'
            df.to_csv(filename, index=False)
        elif format_type == 'json':
            filename += '.json'
            # Запись DataFrame в файл JSON
            df.to_json(filename, orient='records', lines=True)
        elif format_type == 'xml':
            filename += '.xml'
            # Создаем XML файл
            root = ET.Element("clients")
            for _, row in df.iterrows():
                client_elem = ET.SubElement(root, "client")
                for field in fields:
                    value = str(row[field])  # Преобразуем значение в строку
                    field_elem = ET.SubElement(client_elem, field)
                    field_elem.text = value
            tree = ET.ElementTree(root)
            tree.write(filename)

        else:
            self.stdout.write(self.style.ERROR('Invalid format. Supported formats: excel, csv, json, xml'))
            return

        self.stdout.write(self.style.SUCCESS(
            f'Successfully downloaded {"all" if download_all else "selected"} client data as {format_type}. '
            f'File saved as {filename}'))
