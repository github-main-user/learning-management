from django.urls import path

from .apps import PaymentsConfig
from .views import PaymentListAPIView

app_name = PaymentsConfig.name


urlpatterns = [
    path("payments/", PaymentListAPIView.as_view(), name="payment-list"),
]
