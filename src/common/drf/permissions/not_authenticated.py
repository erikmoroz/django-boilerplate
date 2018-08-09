from rest_framework import permissions


class NotAuthenticated(permissions.BasePermission):
    """
    Allows access only to not authenticated users.
    """

    def has_permission(self, request, view):
        return not request.user or not request.user.is_authenticated
