from typing import override

from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated

from .permissions import IsSelfOrReadOnly
from .serializers import (
    UserCreateSerializer,
    UserPrivateSerializer,
    UserPublicSerializer,
)

User = get_user_model()


class UserCreateAPIView(generics.CreateAPIView):
    """Endpoint for user registration. Allows requests from unauthenticated users."""

    serializer_class = UserCreateSerializer
    permission_classes = [AllowAny]


class UserRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    Returns private profile if user in request is owner.
    Otherwise returns public profile (without last_name and payments).
    """

    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, IsSelfOrReadOnly]

    @override
    def get_serializer_class(self):
        if self.request.user == self.get_object():
            return UserPrivateSerializer
        return UserPublicSerializer
