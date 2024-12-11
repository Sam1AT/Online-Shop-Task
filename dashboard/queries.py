from shopping.models import Cart
from django.db.models.functions import TruncDate, Concat
from django.db.models import Sum, F, Value


def cart_price_by_date_user():
    cart_data = (
        Cart.objects.annotate(date=TruncDate("created_at"))
        .annotate(name=Concat(F('user__first_name'), Value(' '),  F('user__last_name')))
        .values('name', 'date')
        .annotate(price=Sum(F('price')))
        .order_by('date', 'price')
    )

    return cart_data
