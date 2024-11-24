from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied


class IsManagerWithAuth(permissions.BasePermission):
    """
    For the manager
    """

    def has_permission(self, request, view) -> bool:
        return (
            request.user and request.user.is_authenticated and request.user.is_manager
        )

    def has_object_permission(self, request, view, obj):
        return True


class IsEmployeeWithAuth(permissions.BasePermission):
    """
    For the employee
    """

    def has_permission(self, request, view) -> bool:
        return (
            request.user and request.user.is_authenticated and request.user.is_employee
        )

    def has_object_permission(self, request, view, obj):
        return True


class IsManager(permissions.BasePermission):
    """
    For the manager with out auth
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_manager

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
