from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from rest_framework.response import Response
# from book_app.api.views import book_lis


class BookListPagination(PageNumberPagination):
    page_size = 3
    page_query_param = 'page'
    page_size_query_param = 'size'
    max_page_size = 10

    def get_paginated_response(self, data):


        return Response({
            'count': self.page.paginator.count,
            'page_number': self.page.number,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data,
        })



# class BookListPagination(LimitOffsetPagination):
#     default_limit = 3
#     max_limit = 5
#     limit_query_param = 'limit'
#     offset_query_param = 'start'
#
#     def get_paginated_response(self, data):
#
#         return Response({
#             'results': data,
#         })
