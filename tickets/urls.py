from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import TicketViewSet


name = 'tickets'

router = DefaultRouter()
router.register(r'ticket', TicketViewSet, basename='ticket')


urlpatterns = [
    path('', include(router.urls)),
]