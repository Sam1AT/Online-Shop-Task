from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from dashboard.queries import cart_price_by_date_user
from dashboard.utils import parse_cart_list
class GetCustomersTotalCart(APIView):
    def get(self, request):
        cart_date_user_list = parse_cart_list(cart_price_by_date_user())

        return Response(cart_date_user_list)

