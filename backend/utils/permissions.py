from rest_framework import permissions

class IsOwner(permissions.BasePermission):
    accept_methods = ("PUT", "DELETE", "GET")
    
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        return False
    
    def has_object_permission(self, request, view, obj):
        if obj.created_by == request.user and request.method in self.accept_methods:
            return True
        return False
    
class IsInventoryOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        return False
    
    def has_object_permission(self, request, view, obj):
        if obj.product.created_by == request.user and request.method == "PUT":
            return True
        return False