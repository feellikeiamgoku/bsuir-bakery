from rest_framework.permissions import BasePermission


class IsOwnerOrAdmin(BasePermission):
        
    def has_object_permission(self, request, view, obj):
        return obj.user_id==request.user or request.user.is_staff or request.user.is_worker