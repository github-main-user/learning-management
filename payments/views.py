from typing import override

import stripe
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status
from rest_framework.exceptions import APIException
from rest_framework.filters import OrderingFilter

from payments.serializers import PaymentSerializer

from .models import Payment
from .services import (
    create_stripe_checkout_session,
    create_stripe_price,
    create_stripe_product,
    fetch_stripe_session,
)


class PaymentListAPIView(generics.ListAPIView):
    """
    List Endpoint for Payment.
    Allows ordering by "timestamp" and filtering by "course", "lesson" and "method".
    """

    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    filter_backends = [DjangoFilterBackend, OrderingFilter]
    ordering_fields = ["timestamp"]
    filterset_fields = ["course", "lesson", "method"]


class PaymentCreateAPIView(generics.CreateAPIView):
    """
    Create Payment for Course.
    Creates stripe checkout session.
    """

    serializer_class = PaymentSerializer

    @override
    def perform_create(self, serializer):
        user = self.request.user
        course = serializer.validated_data["course"]

        session = None
        try:
            product_id = create_stripe_product(course.title, course.description)
            price_id = create_stripe_price(product_id, int(course.price * 100))

            success_url = self.request.build_absolute_uri(
                f"/payment/success/{user.pk}/"
            )
            cancel_url = self.request.build_absolute_uri(f"/payment/cancel/")
            session = create_stripe_checkout_session(price_id, success_url, cancel_url)
        except stripe.StripeError as e:
            print(f"Failed to create a stripe checkout session: {e}")

        if not session:
            raise APIException(
                code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="An error occured during stripe session creation",
            )

        serializer.save(
            user=user,
            course=course,
            amount=course.price,
            method=Payment.PaymentMethod.STRIPE,
            stripe_session_id=session.id,
            payment_url=session.url,
        )


class PaymentStatusAPIView(generics.RetrieveAPIView):
    """Fetches, updates status and returns stripe payment by a given session id."""

    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    lookup_field = "stripe_session_id"

    @override
    def get(self, request, stripe_session_id: str):
        payment = self.get_object()
        session = fetch_stripe_session(payment.stripe_session_id)
        if session.payment_status == "paid":
            payment.is_paid = True
            payment.save()
        return super().get(request, stripe_session_id)
