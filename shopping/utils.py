from shopping.models import (
    Cart,
    CartItem
)



def create_cart_in_db(cart, user_id):
    cart_obj = Cart.objects.create(user_id=user_id)

    for product_id, quantity in cart.items():
        cart_item = CartItem.objects.create(product_id=product_id,
                                            quantity=quantity,
                                            cart=cart_obj)
    cart_obj.update_cart_price()
