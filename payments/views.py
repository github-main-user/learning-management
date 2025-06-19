from typing import override

import stripe
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status
from rest_framework.exceptions import APIException
from rest_framework.filters import OrderingFilter

from materials.models import Course
from payments.serializers import CoursePaymentSerializer, PaymentSerializer

from .models import Payment
from .services import (
    create_stripe_checkout_session,
    create_stripe_price,
    create_stripe_product,
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

    serializer_class = CoursePaymentSerializer

    @override
    def perform_create(self, serializer):
        user = self.request.user
        course_id = serializer.course
        course = get_object_or_404(Course, id=course_id)

        product_id = create_stripe_product(course.title, course.description)
        price_id = create_stripe_price(product_id, course.price)

        session = None
        try:
            success_url = self.request.build_absolute_uri(
                f"/payment/success/{user.id}/"
            )
            cancel_url = self.request.build_absolute_uri(f"/payment/cancel/")
            session = create_stripe_checkout_session(price_id, success_url, cancel_url)
        except stripe.StripeError:
            pass

        if not session:
            raise APIException(
                code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="An error occured during stripe session creation",
            )

        Payment.objects.create(
            user=user,
            course=course,
            amount=course.price,
            method=Payment.PaymentMethod.STRIPE,
            stripe_session_id=session.id,
            payment_url=session.url,
        )
