from django.contrib.auth import get_user_model
from rest_framework import generics

from .serializers import ProfileSerializer

User = get_user_model()


class ProfileListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = ProfileSerializer


class ProfileRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = ProfileSerializer
