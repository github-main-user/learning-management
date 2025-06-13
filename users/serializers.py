from django.contrib.auth import get_user_model
from rest_framework.serializers import ModelSerializer

from .models import Payment

User = get_user_model()


class PaymentSerializer(ModelSerializer):
    class Meta:
        model = Payment
        fields = ["id", "user", "timestamp", "course", "lesson", "amount", "method"]
        read_only_fields = ["timestamp"]


class UserSerializer(ModelSerializer):
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
