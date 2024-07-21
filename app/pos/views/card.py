from rest_framework import viewsets
from ..serializers import CardSerializer, CardDetailSerializer
from ..models import Card
from rest_framework.permissions import IsAuthenticated, IsAdminUser


class CardViewSet(viewsets.ModelViewSet):
    queryset = Card.objects.all()
    serializer_class = CardSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "uid"

    def get_queryset(self):
        user = self.request.user
        if user.is_staff or user.is_superuser:
            return Card.objects.all()
        return Card.objects.filter(user=user)

    def get_permissions(self):
        # Define different permissions for different actions
        if self.action in ["list", "retrieve"]:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        print("Action", self.action)
        if self.action in ["create", "retrieve", "update", "partial_update"]:
            return CardDetailSerializer
        return CardSerializer
