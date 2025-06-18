from rest_framework import serializers

from .models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ["id", "user", "timestamp", "course", "lesson", "amount", "method"]
        read_only_fields = ["timestamp"]
