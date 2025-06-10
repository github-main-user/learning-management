from rest_framework.routers import DefaultRouter

from .views import ProfileViewSet

profile_router = DefaultRouter()
profile_router.register("profiles", ProfileViewSet, "profile")

urlpatterns = profile_router.urls
