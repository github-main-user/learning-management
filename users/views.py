from typing import override

from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import AllowAny

from .models import Payment
from .permissions import IsSelfOrReadOnly
from .serializers import (
    PaymentSerializer,
    UserCreateSerializer,
    UserPrivateSerializer,
    UserPublicSerializer,
)

User = get_user_model()


class UserCreateAPIView(generics.CreateAPIView):
    """Endpoint for user registration. Allows requests from unauthenticated users."""

    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = [AllowAny]


class UserRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    Returns private profile if user in request is owner.
    Otherwise returns public profile (without last_name and payments).
    """

    queryset = User.objects.all()
    permission_classes = [IsSelfOrReadOnly]

    @override
    def get_serializer_class(self):
        if self.request.user == self.get_object():
            return UserPrivateSerializer
        return UserPublicSerializer


class PaymentListCreateAPIView(generics.ListCreateAPIView):
    """
    Create/List Endpoint for Payment.
    Allows ordering by "timestamp" and filtering by "course", "lesson" and "method".
    """

    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    filter_backends = [DjangoFilterBackend, OrderingFilter]
    ordering_fields = ["timestamp"]
    filterset_fields = ["course", "lesson", "method"]


class PaymentRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve/Update/Destroy Endpoint for Payment."""

    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
