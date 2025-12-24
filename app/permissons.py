from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    message = "siz admin emassiz"

    def has_permission(self, request, view):
        return request.user and request.user.is_admin


class IsSuperAdmin(BasePermission):
    message = "siz SuperAdmin emassiz"

    def has_permission(self, request, view):
        return request.user and request.user.is_superadmin


class IsAdmin_or_SuperAdmin(BasePermission):
    message = "siz adminlik huquqiga ega emassiz"

    def has_permission(self, request, view):
        return (request.user and request.user.is_admin) or (
            request.user and request.user.is_superadmin
        )
