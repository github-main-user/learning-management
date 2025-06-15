from typing import override

from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """Validates if user in request is object owner."""

    @override
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class IsSelfOrReadOnly(permissions.BasePermission):
    """Validates if user in request is given object **or** request method is safe."""

    @override
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj == request.user


class IsModerator(permissions.BasePermission):
    """Validates if user in request is in "moderators" group."""

    @override
    def has_permission(self, request, view):
        return request.user.groups.filter(name="moderators").exists()
