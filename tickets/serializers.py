from rest_framework import serializers
from .models import Ticket


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['id', 'title', 'description', 'status', 'created_at',
                 'updated_at', 'assigned_to', 'assigned_at']

        read_only_fields = ['created_at', 'updated_at', 'assigned_at']


class TicketStatusUpdateSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=Ticket.STATUS_CHOICES)


class TicketAssignSerializer(serializers.Serializer):
    batch_size = serializers.IntegerField(default=10, min_value=1, max_value=50)
