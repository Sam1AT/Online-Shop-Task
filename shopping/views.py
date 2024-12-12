from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions

from django.db import transaction

from utils import get_redis_client
from shopping.models import Product


CART_LIFETIME = 30

class AddToCartView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        user_id = request.user.id
        product_id = str(request.data.get("product_id"))
        quantity = int(request.data.get("quantity", 1))
        redis_client = get_redis_client()

        try:
            with transaction.atomic():
                product = Product.objects.select_for_update(nowait=True).get(id=product_id)

                if not product.is_available(quantity):
                    return Response(
                        {"error": f"Can't provide this amount for {product.name}"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                product.stock -= quantity
                product.save()

                cart_key = f"cart:{user_id}"
                cart = redis_client.hgetall(cart_key)

                if product_id in cart:
                    cart[product_id] = str(int(cart[product_id]) + quantity)
                else:
                    cart[product_id] = str(quantity)

                redis_client.hmset(cart_key, cart)

                shadow_cart_key = f"shadow:{cart_key}"
                redis_client.set(shadow_cart_key, "", ex=CART_LIFETIME)

            return Response(
                {"message": "Added to cart", "cart": cart},
                status=status.HTTP_200_OK,
            )

        except Product.DoesNotExist:
            return Response(
                {"error": "Product with this id does not exists"}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": "An error occurred", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )