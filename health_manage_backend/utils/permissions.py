"""
自定义权限类：用户仅可操作自身数据
"""
from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOrReadOnly(BasePermission):
    """
    仅允许资源所有者或只读操作
    管理员可以操作所有数据
    """

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        if request.user.is_staff or request.user.is_superuser:
            return True
        return hasattr(obj, 'user') and obj.user == request.user


class IsOwnerOrAdmin(BasePermission):
    """
    仅允许资源所有者或管理员操作
    适用于：用户只能查看/修改自己的健康记录、计划等
    """

    def has_object_permission(self, request, view, obj):
        # 管理员拥有所有权限
        if request.user.is_staff:
            return True
        # 普通用户仅能操作自己的数据
        return hasattr(obj, 'user') and obj.user == request.user