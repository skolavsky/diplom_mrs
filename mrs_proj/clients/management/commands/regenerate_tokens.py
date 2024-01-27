# файл management/commands/regenerate_tokens.py
from django.core.management.base import BaseCommand
from clients.models import PersonalInfo
import secrets
import uuid


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
            clients = PersonalInfo.objects.all()
            client_ids = [client.id for client in clients]

        for client_id in client_ids:
            try:
                client = PersonalInfo.objects.get(pk=client_id)
                client.id = uuid.uuid4()  # Regenerate UUID
                client.save()
                self.stdout.write(self.style.SUCCESS(f'Successfully regenerated token for client {client_id}'))
            except PersonalInfo.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'Client with ID {client_id} does not exist'))