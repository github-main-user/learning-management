from django.urls import path

from .apps import UsersConfig
from .views import (
    PaymentListCreateView,
    PaymentRetrieveUpdateDestroyView,
    ProfileListCreateView,
    ProfileRetrieveUpdateDestroyView,
)

app_name = UsersConfig.name


urlpatterns = [
    path("profiles/", ProfileListCreateView.as_view(), name="profile-list"),
    path(
        "profiles/<int:pk>/",
        ProfileRetrieveUpdateDestroyView.as_view(),
        name="profile-detail",
    ),
    path("payments/", PaymentListCreateView.as_view(), name="payment-list"),
    path(
        "payments/<int:pk>/",
        PaymentRetrieveUpdateDestroyView.as_view(),
        name="payment-detail",
    ),
]
