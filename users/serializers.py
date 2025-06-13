from typing import override

from django.contrib.auth import get_user_model
from rest_framework.serializers import ModelSerializer

from .models import Payment

User = get_user_model()


class PaymentSerializer(ModelSerializer):
    class Meta:
        model = Payment
        fields = ["id", "user", "timestamp", "course", "lesson", "amount", "method"]
        read_only_fields = ["timestamp"]


class UserCreateSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    @override
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class UserPrivateSerializer(ModelSerializer):
    payments = PaymentSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "phone",
            "city",
            "avatar",
            "payments",
        ]


class UserPublicSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "first_name", "phone", "city", "avatar"]
