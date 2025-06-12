from django.contrib.auth import get_user_model
from rest_framework import generics

from .serializers import PaymentSerializer, ProfileSerializer

User = get_user_model()


class ProfileListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = ProfileSerializer


class ProfileRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = ProfileSerializer


class PaymentListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = PaymentSerializer


class PaymentRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = PaymentSerializer
