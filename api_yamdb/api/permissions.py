from rest_framework import permissions


class IsAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        print(bool(
            request.user.is_authenticated
            and
            (request.user.role == 'admin' or request.user.is_superuser)
            ))
        return (
            request.user.is_authenticated
            and
            (request.user.role == 'admin' or request.user.is_superuser)
            )

    def has_object_permission(self, request, view, obj):
        print(bool(
            request.user.is_authenticated
            and
            (request.user.role == 'admin' or request.user.is_superuser)
            ))
        return (
            request.user.is_authenticated
            and
            (request.user.role == 'admin' or request.user.is_superuser)
            )
