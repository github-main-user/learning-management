from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.filters import OrderingFilter

from payments.serializers import PaymentSerializer

from .models import Payment


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
