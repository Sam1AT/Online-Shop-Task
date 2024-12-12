import copy

from django.test import TestCase, TransactionTestCase
from django.urls import reverse
from accounts.models import CustomUser

from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

import threading

from shopping.models import Product
from utils import get_redis_client


class AddToCartViewTests(TransactionTestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(email="testuser@yahoo.com", password="password")
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)

        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

        self.product = Product.objects.create(
            name="Test Product", stock=10, price=100.0
        )

        self.redis_client = get_redis_client()
        self.redis_client.flushall()

    def test_add_to_cart_valid(self):
        url = reverse("add_to_cart")
        data = {"product_id": self.product.id, "quantity": 2}

        response = self.client.post(url, data, format="json")

        print("Test:", response.status_code)

        self.assertEqual(response.status_code, 200)
        self.assertIn("message", response.data)
        self.assertEqual(response.data["message"], "Added to cart")
        self.assertIn(str(self.product.id), response.data["cart"])
        self.assertEqual(int(response.data["cart"][str(self.product.id)]), 2)

        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 8)

    def test_add_to_cart_invalid_product(self):

        url = reverse("add_to_cart")
        data = {"product_id": 9999, "quantity": 1}

        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data["error"], "Product with this id does not exists")

    def test_add_to_cart_insufficient_stock(self):

        url = reverse("add_to_cart")
        data = {"product_id": self.product.id, "quantity": 20}

        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertIn("Can't provide this amount for", response.data["error"])


    def add_to_cart(self, product_id, url):
        data = {"product_id": product_id, "quantity": 1}
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

        response = client.post(url, data, format="json")

    def test_concurrent_add_to_cart(self):

        url = reverse("add_to_cart")
        threads = []

        for _ in range(5):

            threads.append(threading.Thread(target=self.add_to_cart, args=(self.product.id, url)))

        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()

        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 5)

        cart_key = f"cart:{self.user.id}"
        cart = self.redis_client.hgetall(cart_key)
        self.assertEqual(int(cart[str(self.product.id)]), 5)