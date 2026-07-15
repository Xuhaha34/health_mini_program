"""
统一接口返回格式封装
所有API接口返回统一JSON结构，便于前端统一处理
"""
from rest_framework.response import Response
from rest_framework import status


def success_response(data=None, message='操作成功', code=200):
    """成功响应快捷函数"""
    return Response({
        'code': code,
        'message': message,
        'data': data
    }, status=status.HTTP_200_OK)


def error_response(message='操作失败', code=400, errors=None):
    """失败响应快捷函数"""
    return Response({
        'code': code,
        'message': message,
        'errors': errors
    }, status=status.HTTP_400_BAD_REQUEST)


class APIResponse:
    """统一响应格式（兼容旧代码）"""

    @staticmethod
    def success(data=None, message='操作成功', code=200):
        """成功响应"""
        return Response({
            'code': code,
            'message': message,
            'data': data
        }, status=status.HTTP_200_OK)

    @staticmethod
    def created(data=None, message='创建成功'):
        """创建成功响应"""
        return Response({
            'code': 201,
            'message': message,
            'data': data
        }, status=status.HTTP_201_CREATED)

    @staticmethod
    def error(message='操作失败', code=400, errors=None):
        """失败响应"""
        return Response({
            'code': code,
            'message': message,
            'errors': errors
        }, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def not_found(message='资源不存在'):
        """404响应"""
        return Response({
            'code': 404,
            'message': message,
            'data': None
        }, status=status.HTTP_404_NOT_FOUND)

    @staticmethod
    def unauthorized(message='未授权，请先登录'):
        """401未授权"""
        return Response({
            'code': 401,
            'message': message,
            'data': None
        }, status=status.HTTP_401_UNAUTHORIZED)