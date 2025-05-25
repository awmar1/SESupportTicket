from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()

class Ticket(models.Model):
    STATUS_CHOICES = [
        ('unassigned', 'Unassigned'),
        ('assigned', 'Assigned'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='unassigned')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    assigned_to = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='assigned_tickets'
    )
    assigned_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['status', 'created_at']),
            models.Index(fields=['assigned_to']),
        ]

    def clean(self):
        """Basic validation rules"""
        if self.status == 'assigned' and not self.assigned_to:
            raise ValidationError("Assigned tickets must have an agent assigned")
        if self.assigned_to and self.status == 'unassigned':
            raise ValidationError("Tickets with assigned agents cannot be unassigned")