from rest_framework.permissions import BasePermission

class IsAdminGroup(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.groups.filter(name='ADMIN').exists())

class IsAdminOrInternal(BasePermission):
    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False
        return request.user.groups.filter(name__in=['ADMIN','INTERNO']).exists()

class IsAuditorOrAdmin(BasePermission):
    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False
        return request.user.groups.filter(name__in=['ADMIN','AUDITOR']).exists()

