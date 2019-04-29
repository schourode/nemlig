import json
import itertools
import logging
import os
import sys

sys.path.insert(0, '.')
import api as nemlig

log = logging.getLogger('nemlig.orders')

cache_dir = None


def refresh(depth):
    basic_order_history = nemlig.get_basic_order_history(take=depth)
    for order in basic_order_history['Orders']:
        if order['Status'] < 2:  # "Faktureret"
            log.debug(f"Ignoring order {order['OrderNumber']} (status = {order['Status']})")
            continue
        filepath = os.path.join(__orders_cache_path(), order['OrderNumber'] + '.json')
        if os.path.isfile(filepath):
            log.debug(f"Order {order['OrderNumber']} already in cache")
            continue
        order_history = nemlig.get_order_history(order['Id'])
        del order_history['Email']
        with open(filepath, 'w') as json_file:
            json.dump(order_history, json_file, indent=2)
        log.debug(f"Order {order['OrderNumber']} persisted to cache ...")
    log.debug('Reached order history EOF')


def most_recent(n):
    orders_dir = __orders_cache_path()
    filenames = os.listdir(orders_dir)
    in_order = reversed(sorted(filenames))
    for filename in itertools.islice(in_order, n):
        filepath = os.path.join(orders_dir, filename)
        with open(filepath, 'r') as json_file:
            yield json.load(json_file)


def __orders_cache_path():
    if not cache_dir:
        raise Exception('Uninitialized field: orders.cache_dir')
    orders_dir = os.path.join(cache_dir, 'orders')
    os.makedirs(orders_dir, exist_ok=True)
    return orders_dir
