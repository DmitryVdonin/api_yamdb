from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """Дает разрешение на чтение, добавление, изменения объекта
     суперпользователю и администратору.
    """

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and (request.user.role == 'admin' or request.user.is_superuser)
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.user.is_authenticated
            and (request.user.role == 'admin' or request.user.is_superuser)
        )


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or (request.user.is_authenticated and (
                request.user.role == 'admin' or request.user.is_superuser)))


class IsOwnerOrModeratorOrReadOnly(permissions.BasePermission):
    """Дает разрешение на чтение любому пользователю,
    разрешение на добавление аутентифицированному пользователю,
    разрешение на изменение или удаление суперпользователю, администратору и
    автору объекта.
    """

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user == obj.author
            or request.user.role == 'moderator'
            or request.user.is_superuser
        )
