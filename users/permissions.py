from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminRole(BasePermission):
    """Только Admin"""
    def has_permission(self, request, view):
        return (request.user.is_authenticated and
                (request.user.role == 'admin' or request.user.is_staff))


class IsBusinessOwner(BasePermission):
    """Только Business Owner"""
    def has_permission(self, request, view):
        return (request.user.is_authenticated and
                request.user.role == 'business_owner')


class IsAdminOrBusinessOwner(BasePermission):
    """Admin или Business Owner"""
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return (request.user.role in ('admin', 'business_owner')
                or request.user.is_staff)


class IsOwnerOrAdmin(BasePermission):
    """Владелец объекта или Admin"""
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        if request.user.role == 'admin' or request.user.is_staff:
            return True
        owner = getattr(obj, 'owner', None) or getattr(obj, 'user', None)
        return owner == request.user
