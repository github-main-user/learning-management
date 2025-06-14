from typing import override

from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    @override
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class IsSelfOrReadOnly(permissions.BasePermission):
    @override
    def has_object_permission(self, request, view, obj):
        # SAFE_METHODS = GET, HEAD, OPTIONS
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj == request.user
