import random

from django.core.management.base import BaseCommand
from django.utils import timezone

from tickets.models import Ticket


class Command(BaseCommand):
    help = 'Populates the database with dummy tickets'

    def add_arguments(self, parser):
        parser.add_argument('count', type=int)

    def handle(self, *args, **options):
        count = options['count']

        tickets = []
        for i in range(count):
            tickets.append(Ticket(
                title=f'Test Ticket {i + 1}',
                description=f'This is a test ticket #{i + 1} with some random content.',
                status='unassigned',
                created_at=timezone.now()
            ))

        Ticket.objects.bulk_create(tickets)
        self.stdout.write(self.style.SUCCESS(f'Successfully created {count} tickets'))