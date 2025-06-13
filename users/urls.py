from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .apps import UsersConfig
from .views import (
    PaymentListCreateView,
    PaymentRetrieveUpdateDestroyView,
    ProfileListCreateView,
    ProfileRetrieveUpdateDestroyView,
)

app_name = UsersConfig.name


urlpatterns = [
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
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
