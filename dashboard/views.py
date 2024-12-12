from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination

from dashboard.queries import cart_price_by_date_user
from dashboard.utils import parse_cart_list


class GetCustomersTotalCart(APIView):
    class CustomPagination(PageNumberPagination):
        page_size = 10
        page_size_query_param = 'page_size'

    def get(self, request):
        cart_date_user_list = parse_cart_list(cart_price_by_date_user())

        paginator = self.CustomPagination()
        paginated_data = paginator.paginate_queryset(cart_date_user_list, request)

        return paginator.get_paginated_response(paginated_data)

