from django.contrib.auth import get_user_model
from rest_framework import viewsets

from .serializers import ProfileSerializer

User = get_user_model()


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = ProfileSerializer
