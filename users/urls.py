from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .apps import UsersConfig
from .views import (
    PaymentListCreateAPIView,
    PaymentRetrieveUpdateDestroyView,
    UserCreateAPIView,
    UserListAPIView,
    UserRetrieveUpdateDestroyAPIView,
)

app_name = UsersConfig.name


urlpatterns = [
    path("register/", UserCreateAPIView.as_view(), name="register"),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("profiles/", UserListAPIView.as_view(), name="profile-list"),
    path(
        "profiles/<int:pk>/",
        UserRetrieveUpdateDestroyAPIView.as_view(),
        name="profile-detail",
    ),
    path("payments/", PaymentListCreateAPIView.as_view(), name="payment-list"),
    path(
        "payments/<int:pk>/",
        PaymentRetrieveUpdateDestroyView.as_view(),
        name="payment-detail",
    ),
]
