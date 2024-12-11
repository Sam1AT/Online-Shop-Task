from django.urls import path

from shopping.views import (
    AddToCartView,

)
urlpatterns = [
    path('add-item/', AddToCartView.as_view(), name='add_to_cart'),

]
