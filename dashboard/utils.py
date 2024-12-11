from collections import defaultdict


def parse_cart_list(queryset):
    queryset = list(queryset)
    tmp_data = defaultdict(list)

    for data in queryset:
        tmp_data[data.get('date')].append({
            'name': data.get('name'),
            'price': data.get('price')
        })

    result = [
        {
            'date': date,
            'list': items
        }
        for date, items in tmp_data.items()
    ]

    return result
