import threading
from django.db import transaction

from utils import get_redis_client
from shopping.utils import create_cart_in_db
from .models import Product

redis_client = get_redis_client()
listener_thread_started = False

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
        create_cart_in_db(cart, user_id)


        for product_id, quantity in cart.items():
                product = Product.objects.select_for_update().get(id=product_id)
                with transaction.atomic():
                    product.stock += int(quantity)
                    product.save()

        redis_client.delete(cart_key)
        print("-> Deleted and updated Products stocks")

def start_expiry_listener():
    global listener_thread_started

    if not listener_thread_started:
        listener_thread = threading.Thread(target=listen_for_expired_keys)
        listener_thread.daemon = True
        listener_thread.start()
        listener_thread_started = True
        print("Redis expiry listener thread started")
