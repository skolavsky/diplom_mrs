from datetime import datetime

import pandas as pd
import xml.etree.ElementTree as ET
import io

from clients.models import ClientData


class ClientDataDownloader:
    def __init__(self, personal_info_ids=None, download_all=False):
        self.fields = ['id', 'age', 'body_mass_index', 'spo2', 'admission_date', 'result', 'dayshome', 'rox',
                       'f_test_ex', 'f_test_in', 'comorb_ccc', 'comorb_bl', 'cd_ozhir', 'ch_d', 'lf', 'l_109',
                       'spo2_fio']
        if download_all:
            self.queryset = ClientData.objects.all()
        elif personal_info_ids:
            self.queryset = ClientData.objects.filter(personal_info_id__in=personal_info_ids)
        else:
            raise ValueError('No personal info IDs provided.')

    def generate_df(self):
        data = self.queryset.values(*self.fields)
        return pd.DataFrame(data)

    def generate_excel(self):
        df = self.generate_df()
        buffer = io.BytesIO()
        df.to_excel(buffer, index=False, engine='openpyxl')
        return buffer

    def generate_csv(self):
        df = self.generate_df()
        buffer = io.StringIO()
        df.to_csv(buffer, index=False)
        return buffer

    def generate_json(self):
        df = self.generate_df()
        buffer = io.BytesIO()
        df.to_json(buffer, orient='records', lines=True)
        return buffer

    def generate_xml(self):
        df = self.generate_df()
        root = ET.Element("clients")
        for _, row in df.iterrows():
            client_elem = ET.SubElement(root, "client")
            for field in self.fields:
                value = str(row[field])  # Преобразуем значение в строку
                field_elem = ET.SubElement(client_elem, field)
                field_elem.text = value
        buffer = io.BytesIO()
        tree = ET.ElementTree(root)
        tree.write(buffer)
        return buffer

    def save_locally(self, filename, format_type):
        if format_type == 'excel':
            buffer = self.generate_excel()
            filename += '.xlsx'
        elif format_type == 'csv':
            buffer = self.generate_csv()
            filename += '.csv'
        elif format_type == 'json':
            buffer = self.generate_json()
            filename += '.json'
        elif format_type == 'xml':
            buffer = self.generate_xml()
            filename += '.xml'
        else:
            raise ValueError('Invalid format type')

        with open(filename, 'wb') as f:
            f.write(buffer.getvalue())

        return filename
