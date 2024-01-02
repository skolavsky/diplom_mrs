# файл management/commands/regenerate_tokens.py
import uuid
from django.core.management.base import BaseCommand
from clients.models import Client
import secrets


class Command(BaseCommand):
    help = 'Regenerate tokens for specified clients or all clients'

    def add_arguments(self, parser):
        parser.add_argument('--all', action='store_true', help='Regenerate tokens for all clients')
        parser.add_argument('client_ids', nargs='*', type=uuid.UUID, help='List of client IDs to regenerate tokens for')

    def handle(self, *args, **kwargs):
        regenerate_all = kwargs['all']
        client_ids = kwargs['client_ids']

        if not regenerate_all and not client_ids:
            self.stdout.write(self.style.WARNING('No client IDs provided. Exiting...'))
            return

        if regenerate_all:
            clients = Client.objects.all()
            client_ids = [client.id for client in clients]

        for client_id in client_ids:
            try:
                client = Client.objects.get(pk=client_id)
                client.id_token = secrets.token_urlsafe(32)
                client.save()
                self.stdout.write(self.style.SUCCESS(f'Successfully regenerated token for client {client_id}'))
            except Client.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'Client with ID {client_id} does not exist'))
