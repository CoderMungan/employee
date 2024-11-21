from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied

# Custom Permissions


class IsAdminWithAuth(permissions.BasePermissions):
    """
    For the admin
    """

    def has_permission(self, request, view) -> bool:
        return request.user and request.user.is_authendicated and request.user.is_admin

    def has_object_permission(self, request, view, obj):
        return True


class IsEmployeeWithAuth(permissions.BasePermission):
    """
    For the employee
    """

    def has_permission(self, request, view) -> bool:
        return (
            request.user and request.user.is_authendicated and request.user.is_employee
        )

    def has_object_permission(self, request, view, obj):
        return True


class IsAdmin(permissions.BasePermission):
    """
    For the admin with out auth
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_admin

    def has_object_permission(self, request, view, obj):
        return True


class IsEmployee(permissions.BasePermission):
    """
    For the employee with out auth
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_employee

    def has_object_permission(self, request, view, obj):
        return True
