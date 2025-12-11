from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    message = 'siz admin emassiz'

    def has_permission(self, request, view):
        return request.user and request.user.is_admin

class IsSuperAdmin(BasePermission):
    message = 'siz SuperAdmin emassiz'

    def has_permission(self, request, view):
        return request.user and request.user.is_superadmin