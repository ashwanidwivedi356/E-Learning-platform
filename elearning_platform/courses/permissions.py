# # courses/permissions.py

from rest_framework import permissions

class IsInstructorOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        print("User:", request.user)
        print("Role:", getattr(request.user, 'role', None))
        # Allow SAFE methods for anyone
        if request.method in permissions.SAFE_METHODS:
            return True
        # Only instructors can create/update/delete
        return request.user.is_authenticated and request.user.role in ['instructor', 'admin']

    def has_object_permission(self, request, view, obj):
        # Only instructor who created can modify
        return obj.instructor == request.user


# class IsInstructorOrReadOnly(permissions.BasePermission):
#     def has_permission(self, request, view):
#         if request.method in permissions.SAFE_METHODS:
#             return True
#         return request.user.is_authenticated and request.user.role in ['instructor', 'admin']

#     def has_object_permission(self, request, view, obj):
#         return obj.instructor == request.user or request.user.role == 'admin'


from rest_framework.permissions import BasePermission

class IsEnrolledOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        if request.user == obj.instructor:
            return True
        return request.user in obj.students.all()
