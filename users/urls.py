from django.urls import path

from .apps import UsersConfig
from .views import ProfileListCreateView, ProfileRetrieveUpdateDestroyView

app_name = UsersConfig.name


urlpatterns = [
    path("profiles/", ProfileListCreateView.as_view(), name="profile-list"),
    path(
        "profiles/<int:pk>",
        ProfileRetrieveUpdateDestroyView.as_view(),
        name="profile-detail",
    ),
]
