from rest_framework import serializers

from .models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = [
            "id",
            "user",
            "timestamp",
            "course",
            "lesson",
            "amount",
            "method",
            "stripe_session_id",
            "payment_url",
            "is_paid",
        ]
        read_only_fields = [f for f in fields if f != "course"]
