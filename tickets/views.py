from rest_framework import viewsets, views, status
from rest_framework.response import Response
from rest_framework.decorators import action

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from .models import Ticket
from .services import TicketService
from .serializers import TicketSerializer, TicketStatusUpdateSerializer, TicketAssignSerializer


class TicketViewSet(viewsets.ModelViewSet):
    serializer_class = TicketSerializer

    def get_queryset(self):
        return Ticket.objects.all()

    @swagger_auto_schema(
        operation_description="Get tickets assigned to the current user",
        manual_parameters=[
            openapi.Parameter(
                'status',
                openapi.IN_QUERY,
                description="Filter tickets by status",
                type=openapi.TYPE_STRING,
                enum=['unassigned', 'assigned', 'in_progress', 'resolved']
            )
        ],
        responses={
            200: openapi.Response(
                description="List of tickets",
                examples={
                    "application/json": {
                        "count": 1,
                        "results": [
                            {
                                "id": 1,
                                "title": "Example Ticket",
                                "description": "Description",
                                "status": "assigned",
                                "created_at": "2024-03-21T10:00:00Z",
                                "assigned_at": "2024-03-21T10:01:00Z"
                            }
                        ]
                    }
                }
            )
        }
    )
    @action(detail=False, methods=['get'])
    def my_tickets(self, request):
        tickets = self.get_queryset().filter(
            assigned_to=request.user
        ).order_by('-assigned_at')

        status_filter = request.query_params.get('status')
        if status_filter:
            tickets = tickets.filter(status=status_filter)

        page = self.paginate_queryset(tickets)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    @swagger_auto_schema(
        operation_description="Update ticket status",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['status'],
            properties={
                'status': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    enum=['unassigned', 'assigned', 'in_progress', 'resolved']
                ),
            }
        ),
        responses={
            200: openapi.Response(description="Status updated successfully"),
            400: "Invalid status",
            403: "Not authorized to modify this ticket"
        }
    )
    @action(detail=True, methods=['post'])
    def update_status(self, request, pk=None):
        def update_status(self, request, pk=None):
            ticket = self.get_object()
            serializer = TicketStatusUpdateSerializer(data=request.data)

            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            if ticket.assigned_to != request.user:
                return Response(
                    {'error': 'Not authorized to modify this ticket'},
                    status=status.HTTP_403_FORBIDDEN
                )

            try:
                TicketService.transition_status(
                    ticket=ticket,
                    new_status=serializer.validated_data['status'],
                    user=request.user
                )
                return Response({'status': 'updated'})
            except ValidationError as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Assign unassigned tickets to the requesting agent",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'batch_size': openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    description="Number of tickets to assign",
                    default=10
                ),
            }
        ),
        responses={
            200: openapi.Response(
                description="Tickets assigned successfully",
                examples={
                    "application/json": {
                        "message": "Successfully assigned 5 tickets",
                        "assigned_count": 5,
                        "tickets": [
                            {
                                "id": 1,
                                "title": "Example Ticket",
                                "description": "Description",
                                "created_at": "2024-03-21T10:00:00Z",
                                "assigned_at": "2024-03-21T10:01:00Z"
                            }
                        ]
                    }
                }
            )
        }
    )
    @action(detail=False, methods=['post'])
    def assign(self, request):
        serializer = TicketAssignSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        batch_size = serializer.validated_data['batch_size']
        assigned_tickets = TicketService.assign_tickets_to_agent(
            agent=request.user,
            batch_size=batch_size
        )

        tickets_data = TicketSerializer(assigned_tickets, many=True).data
        return Response({
            'message': f'Successfully assigned {len(assigned_tickets)} tickets',
            'assigned_count': len(assigned_tickets),
            'tickets': tickets_data
        }, status=status.HTTP_200_OK)