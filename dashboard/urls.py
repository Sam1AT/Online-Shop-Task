from django.urls import path
from dashboard.views import (
    GetCustomersTotalCart
)

urlpatterns = [
    path('list-of-carts', GetCustomersTotalCart.as_view(), name='list_of_carts'),


]
