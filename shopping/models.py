from django.db import models
from django.db.models import Sum, F

from accounts.models import CustomUser


class Base(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Product(Base):
    name = models.CharField(max_length=255)
    price = models.IntegerField()
    stock = models.IntegerField(default=0)


    def is_available(self, quantity):
        return self.stock >= quantity

    def __str__(self):
        return self.name

class CartItem(Base):
    cart = models.ForeignKey('Cart', related_name='cart_items', on_delete=models.CASCADE)

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return f"{self.product.name} | Q: {self.quantity}"

class Cart(Base):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    price = models.IntegerField(default=0)
    is_bought = models.BooleanField(default=False)

    def update_cart_price(self):
        sum = self.cart_items.annotate(
            total_item_price=F('quantity') * F('product__price')
        ).aggregate(total_price=Sum('total_item_price'))['total_price'] or 0

        self.price = sum
        self.save()

    def __str__(self):
        return f"{self.user} | Date: {self.created_at}"

