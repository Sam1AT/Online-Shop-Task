from django.db import models

# Create your models here.
class Base(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Product(Base):
    name = models.CharField(max_length=255)
    price = models.IntegerField()
    stock = models.IntegerField()
