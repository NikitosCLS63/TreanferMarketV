from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated

        
        return obj.owner == request.user or request.user.is_staff

    def has_permission(self, request, view):
        
        if request.method == 'POST':
            return request.user.is_authenticated
        
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated
        
        return request.user.is_authenticated or request.user.is_staff 