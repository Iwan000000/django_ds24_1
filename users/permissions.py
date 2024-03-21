from rest_framework import permissions
from rest_framework.permissions import BasePermission


from rest_framework import permissions

class IsModerator(permissions.BasePermission):
    """Проверка, является ли пользователь модератором?"""

    def has_permission(self, request, view):
        """Проверка прав пользователя"""
        return request.user.groups.filter(name='Moderators').exists()


class IsOwner(permissions.BasePermission):
    """Проверка, является ли пользователь владельцем объекта."""

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user
