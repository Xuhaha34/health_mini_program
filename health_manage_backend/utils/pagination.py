"""
DRF 全局分页类
"""
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class StandardPagination(PageNumberPagination):
    """标准分页：支持 page 和 page_size 参数"""
    page_size = 10                  # 默认每页数量
    page_size_query_param = 'page_size'  # 前端可自定义每页数量
    max_page_size = 100             # 每页最大数量限制
    page_query_param = 'page'       # 页码参数名

    def get_paginated_response(self, data):
        """自定义分页响应格式"""
        return Response({
            'code': 200,
            'message': '查询成功',
            'data': {
                'count': self.page.paginator.count,
                'total_pages': self.page.paginator.num_pages,
                'current_page': self.page.number,
                'page_size': self.get_page_size(self.request),
                'results': data
            }
        })