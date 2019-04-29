from . import webapi


def search_products(query='', take=10):
    return webapi.get('/s/0/1/0/Search/Search', params={
        'query': query,
        'take': take,
    })
