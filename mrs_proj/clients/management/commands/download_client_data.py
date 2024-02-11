from django.core.management.base import BaseCommand
from django.http import HttpResponse

from clients.ClientDataDownloader import ClientDataDownloader
from clients.models import ClientData, PersonalInfo
from datetime import date, datetime
import pandas as pd
import uuid
import xml.etree.ElementTree as ET
import os


class Command(BaseCommand):
    help = 'Download selected client data in various formats'

    def add_arguments(self, parser):
        parser.add_argument('--format', type=str, help='Format of the file (excel/csv/json/xml)')
        parser.add_argument('--all', action='store_true', help='Download all client data')
        parser.add_argument('--file', type=str, help='Path and name of the file')
        parser.add_argument('personal_info_ids', nargs='*', type=uuid.UUID, help='UUIDs of the selected PersonalInfo')

    def handle(self, *args, **kwargs):
        format_type = kwargs['format']
        personal_info_ids = kwargs['personal_info_ids']
        download_all = kwargs['all']
        filename = kwargs['file'] if kwargs['file'] else f'{datetime.now().strftime("%Y%m%d-%H%M")}-data'

        if download_all:
            downloader = ClientDataDownloader(download_all=True)
        elif personal_info_ids:
            downloader = ClientDataDownloader(personal_info_ids)
        else:
            self.stdout.write(self.style.ERROR('No personal info IDs provided.'))
            return

        if format_type == 'excel':
            downloader.save_locally(format_type='excel', filename=filename)
        elif format_type == 'csv':
            downloader.save_locally(format_type='csv', filename=filename)
        elif format_type == 'json':
            downloader.save_locally(format_type='json', filename=filename)
        elif format_type == 'xml':
            downloader.save_locally(format_type='xml', filename=filename)
        else:
            self.stdout.write(self.style.ERROR('Invalid format. Supported formats: excel, csv, json, xml'))
            return

        self.stdout.write(self.style.SUCCESS(
            f'Successfully downloaded {"all" if download_all else "selected"} client data as {format_type}. '
            f'File saved as {filename}'))