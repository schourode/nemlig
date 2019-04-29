from . import webapi


def add_product_to_basket(product_id, quantity):
    return webapi.post('/basket/AddToBasket', json={
        'productId': product_id,
        'quantity': quantity,
    })
