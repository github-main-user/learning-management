from django.urls import path

from .apps import PaymentsConfig
from .views import PaymentCreateAPIView, PaymentListAPIView, PaymentStatusAPIView

app_name = PaymentsConfig.name


urlpatterns = [
    path("", PaymentListAPIView.as_view(), name="payment-list"),
    path("create/", PaymentCreateAPIView.as_view(), name="payment-create"),
    path(
        "status/<str:stripe_session_id>/",
        PaymentStatusAPIView.as_view(),
        name="payment-status",
    ),
]
