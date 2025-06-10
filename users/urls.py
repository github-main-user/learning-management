from rest_framework.routers import DefaultRouter

from .apps import UsersConfig
from .views import ProfileViewSet

app_name = UsersConfig.name

profile_router = DefaultRouter()
profile_router.register("profiles", ProfileViewSet, "profile")

urlpatterns = profile_router.urls
