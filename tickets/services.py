from django.db import transaction
from django.utils import timezone
from django.core.exceptions import ValidationError
from .models import Ticket


class TicketService:
    @staticmethod
    def assign_tickets_to_agent(agent, batch_size=10):
        """Assign tickets to agent (concurrency-safe)"""
        with transaction.atomic():
            tickets = list(
                Ticket.objects
                .filter(status='unassigned')
                .order_by('created_at')
                .select_for_update(skip_locked=True)[:batch_size]
            )

            if not tickets:
                return []

            ticket_ids = [t.id for t in tickets]
            Ticket.objects.filter(id__in=ticket_ids).update(
                status='assigned',
                assigned_to=agent,
                assigned_at=timezone.now()
            )

            return list(Ticket.objects.filter(id__in=ticket_ids))

    @staticmethod
    def transition_status(ticket, new_status, user=None):
        """Handle all status transitions with validation"""
        valid_transitions = {
            'unassigned': ['assigned'],
            'assigned': ['in_progress', 'unassigned'],
            'in_progress': ['resolved'],
            'resolved': ['in_progress']
        }

        if new_status not in valid_transitions.get(ticket.status, []):
            raise ValidationError(f"Invalid status transition from {ticket.status} to {new_status}")

        # Additional business rules
        if new_status == 'assigned' and not user:
            raise ValidationError("Must specify user when assigning ticket")

        with transaction.atomic():
            ticket.status = new_status
            if new_status == 'assigned':
                ticket.assigned_to = user
                ticket.assigned_at = timezone.now()
            ticket.save()

        return ticket