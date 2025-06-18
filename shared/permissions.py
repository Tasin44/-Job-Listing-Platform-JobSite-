from rest_framework import permissions
from core.choices import UserRoleChoices


class IsRecruiterUser(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
            request.user and 
            request.user.is_authenticated and 
            request.user.role == UserRoleChoices.RECRUITER
        )


class IsCandidateUser(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
            request.user and 
            request.user.is_authenticated and 
            request.user.role == UserRoleChoices.CANDIDATE
        )


class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):

        if request.method in permissions.SAFE_METHODS:
            return True
        

        if hasattr(obj, 'user'):
            return obj.user == request.user
        elif hasattr(obj, 'created_by'):
            return obj.created_by == request.user
        
        return obj == request.user


class IsRecruiterOwnerOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):

        if request.method in permissions.SAFE_METHODS:
            return True
        

        return (
            request.user.role == UserRoleChoices.RECRUITER and
            hasattr(obj, 'recruiter') and
            obj.recruiter == request.user
        )





