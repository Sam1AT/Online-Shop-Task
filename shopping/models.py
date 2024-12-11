from django.db import models
from accounts.models import CustomUser
# Create your models here.
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
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()

class Cart(Base):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    CartItems = models.ForeignKey(CartItem, on_delete=models.DO_NOTHING)



