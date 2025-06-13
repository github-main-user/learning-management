from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .apps import UsersConfig
from .views import (
    PaymentListCreateView,
    PaymentRetrieveUpdateDestroyView,
    UserCreateView,
    UserListView,
    UserRetrieveUpdateDestroyView,
)

app_name = UsersConfig.name


urlpatterns = [
    path("register/", UserCreateView.as_view(), name="register"),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("profiles/", UserListView.as_view(), name="profile-list"),
    path(
        "profiles/<int:pk>/",
        UserRetrieveUpdateDestroyView.as_view(),
        name="profile-detail",
    ),
    path("payments/", PaymentListCreateView.as_view(), name="payment-list"),
    path(
        "payments/<int:pk>/",
        PaymentRetrieveUpdateDestroyView.as_view(),
        name="payment-detail",
    ),
]
