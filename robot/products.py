import json
import logging
import os
from statistics import median

log = logging.getLogger('nemlig.products')


class Product:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.ordinalities = list()
        self.quantities = list()

    def median_distance(self, window_size):
        window = self.ordinalities[:window_size+1]
        distances = [window[i] - window[i-1] for i in range(1, len(window))]
        return round(median(distances))

    def median_quantity(self, window_size):
        window = self.quantities[:window_size]
        return round(median(window))


def from_history(order_history):
    products = dict()
    for ix, order in enumerate(order_history):
        for line in order['Lines']:
            if not line['IsProductLine']:
                continue
            if line['AverageItemPrice'] == 0.0:
                continue
            product = products.get(line['ProductNumber'])
            if not product:
                product = Product(line['ProductNumber'], line['ProductName'])
                products[line['ProductNumber']] = product
            product.ordinalities.append(ix + 1)
            product.quantities.append(line['Quantity'])
    return products.values()


    # distances = {k: list(compute_distances(v)) for k,v in ordinalities.items()}
    # median_distances = {k: round(median(v[:window_size])) for k,v in distances.items() if v}
    # current_distances = {k: ordinalities[k][0] - median_distances[k] for k in median_distances}


# def compute_distances(ordinalities):
#     for i in range(1, len(ordinalities)):
#         yield ordinalities[i] - ordinalities[i - 1] - 1


# def extract_products(order):
