from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class MessagePagination(PageNumberPagination):
    page_size = 20  # Default page size
    page_size_query_param = 'page_size'  # Allows client to override page size
    max_page_size = 100  # Maximum limit for page size

    def get_paginated_response(self, data):
        # Add pagination metadata including count
        return Response({
            'count': self.page.paginator.count,  # Adding the requested count
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data
        })