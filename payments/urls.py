from django.urls import path

from .apps import PaymentsConfig
from .views import PaymentCreateAPIView, PaymentListAPIView

app_name = PaymentsConfig.name


urlpatterns = [
    path("payments/", PaymentListAPIView.as_view(), name="payment-list"),
    path("payments/", PaymentCreateAPIView.as_view(), name="payment-create"),
]
