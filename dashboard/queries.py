from shopping.models import Cart
from django.db.models.functions import TruncDate, Concat, Cast
from django.db.models import Sum, F, Value, CharField


def cart_price_by_date_user():
    cart_data = (
        Cart.objects.annotate(date=Cast(TruncDate("created_at"), CharField()))
        .annotate(name=Concat(F('user__first_name'), Value(' '),  F('user__last_name')))
        .values('name', 'date')
        .annotate(price=Sum(F('price')))
        .order_by('date', '-price')
    )

    return cart_data
