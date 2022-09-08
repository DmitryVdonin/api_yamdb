from rest_framework import permissions


class IsAdmin(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):

        return request.user.is_authenticated and (request.user.role == 'admin' or request.user.is_superuser)


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        # or request.user.is_admin
        # AttributeError: 'AnonymousUser' object has no attribute 'is_admin'
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_superuser)
