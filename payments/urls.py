from django.urls import path

from .apps import PaymentsConfig
from .views import PaymentListCreateAPIView, PaymentRetrieveUpdateDestroyView

app_name = PaymentsConfig.name


urlpatterns = [
    path("payments/", PaymentListCreateAPIView.as_view(), name="payment-list"),
    path(
        "payments/<int:pk>/",
        PaymentRetrieveUpdateDestroyView.as_view(),
        name="payment-detail",
    ),
]
