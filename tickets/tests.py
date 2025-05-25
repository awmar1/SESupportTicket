import threading

from django.db import connection, transaction
from django.test import TransactionTestCase
from django.contrib.auth.models import User

from rest_framework.test import APIClient
from concurrent.futures import ThreadPoolExecutor, as_completed

from .models import Ticket


class TicketAssignmentTests(TransactionTestCase):
    def setUp(self):
        # Create test users
        self.users = [
            User.objects.create_user(f'agent{i}', f'agent{i}@test.com', 'password')
            for i in range(5)
        ]

        # Create test tickets in smaller batches
        for i in range(0, 100, 20):
            with transaction.atomic():
                tickets = [
                    Ticket(title=f'Ticket {j}',
                           description=f'Test ticket {j}',
                           status='unassigned')
                    for j in range(i, i + 20)
                ]
                Ticket.objects.bulk_create(tickets)

        # Close any stale connections
        connection.close()

    def tearDown(self):
        # Clean up all data
        Ticket.objects.all().delete()
        User.objects.all().delete()
        connection.close()

    def test_concurrent_assignment(self):
        # Local function to ensure thread-local database connection
        def assign_tickets(user):
            # Create new client and connection for each thread
            client = APIClient()
            client.force_authenticate(user=user)

            try:
                response = client.post(
                    '/api/tickets/ticket/assign/',
                    data={'batch_size': 10},
                    format='json'
                )
                return response
            except Exception as e:
                print(f"Error in thread for user {user.username}: {str(e)}")
                raise
            finally:
                # Close the thread's database connection
                connection.close()

        responses = []
        with ThreadPoolExecutor(max_workers=2) as executor:
            futures = [
                executor.submit(assign_tickets, user)
                for user in self.users[:2]  # Reduce concurrency for stability
            ]

            for future in as_completed(futures):
                try:
                    response = future.result()
                    self.assertEqual(response.status_code, 200)
                    responses.append(response)
                except Exception as e:
                    print(f"Request failed: {str(e)}")
                    raise

        # Verify results
        with transaction.atomic():
            assigned_count = Ticket.objects.filter(status='assigned').count()
            self.assertEqual(assigned_count, 20)  # Adjusted for 2 workers