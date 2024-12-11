import threading

from utils import get_redis_client
from .models import Product

redis_client = get_redis_client()

def listen_for_expired_keys():

    pubsub = redis_client.pubsub()
    pubsub.subscribe('__keyevent@0__:expired')

    for message in pubsub.listen():

        if message.get('type') == 'message':
            expired_key = message.get('data')
            print(f"Key expired: {expired_key}")
            handle_cart_expiration(expired_key)

def handle_cart_expiration(cart_key):
    user_id = cart_key.split(":")[2]

    cart_key = f'cart:{user_id}'
    cart = redis_client.hgetall(cart_key)

    if cart:
        for product_id, quantity in cart.items():
                product = Product.objects.get(id=product_id)
                product.stock += int(quantity)
                product.save()

        redis_client.delete(cart_key)
        print("-> Deleted and updated Products stocks")

def start_expiry_listener():
    listener_thread = threading.Thread(target=listen_for_expired_keys)
    listener_thread.daemon = True
    listener_thread.start()
