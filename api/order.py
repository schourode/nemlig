from . import webapi


def get_basic_order_history(skip=0, take=10):
    return webapi.get('/order/GetBasicOrderHistory', params={
        'skip': skip,
        'take': take,
    })


def get_order_history(order_number):
    return webapi.get(f'/v2/order/GetOrderHistory/{order_number}')
