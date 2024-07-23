from rest_framework import viewsets
from ..serializers import ContractSerializer
from ..models import Contract
from rest_framework.permissions import IsAdminUser


class ContractViewSet(viewsets.ModelViewSet):
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer
    permission_classes = [IsAdminUser]
