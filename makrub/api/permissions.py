from rest_framework import permissions


class IsOwnerForUserModel(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj

class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Foreign field is named as 'user' in every model
        return request.user == obj.user
