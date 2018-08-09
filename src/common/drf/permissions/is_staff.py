from rest_framework import permissions


class IsStaff(permissions.BasePermission):
    """
    Allows to edit and see only to staff users.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_staff
