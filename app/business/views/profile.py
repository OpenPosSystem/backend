from rest_framework import viewsets
from ..serializers import ProfileSerializer
from ..models import Profile
from rest_framework.permissions import IsAdminUser


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAdminUser]
