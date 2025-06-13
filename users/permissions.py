from typing import override

from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    @override
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user
