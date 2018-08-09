from rest_framework import permissions


class IsSuperUser(permissions.BasePermission):
    """
    Allows to edit only to administration users.
    """

    def has_permission(self, request, view):
        return request.user.is_superuser
