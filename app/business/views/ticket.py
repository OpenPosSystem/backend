from rest_framework import viewsets
from ..serializers import TicketSerializer
from ..models import Ticket
from rest_framework.permissions import IsAdminUser


class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [IsAdminUser]
