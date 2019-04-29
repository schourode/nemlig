import logging
import sys
from argparse import ArgumentParser

import orders
import products

sys.path.insert(0, '.')
import api as nemlig

log = logging.getLogger('nemlig.main')


def main(args):
    config = parse_args(args)
    if not (config.dry_run and config.no_refresh):
        if not (config.username and config.password):
            print("--username and --password are required unless --dry-run and --no-refresh")
            sys.exit(1)
        log.info(f"Logging into Nemlig.com as {config.username} ...")
        nemlig.login(config.username, config.password)
    orders.cache_dir = config.cache_dir
    if config.no_refresh:
        log.info("Using previous orders from cache only (--no-refresh)")
    else:
        log.info(f"Downloading {config.max_depth} past orders ...")
        orders.refresh(config.max_depth)
    history = orders.most_recent(config.max_depth)
    for product in products.from_history(history):
        if len(product.ordinalities) < config.window_min:
            log.debug(f"Ignoring '{product.name}' (not enough data)")
            continue
        current_distance = product.ordinalities[0]
        usual_distance = product.median_distance(config.window_max)
        if current_distance < usual_distance:
            log.debug(f"Ignoring '{product.name}' (still in stock)")
            continue
        if current_distance > usual_distance + config.forget_after:
            log.debug(f"Ignoring '{product.name}' (forgotten)")
            continue
        quantity = product.median_quantity(config.window_max)
        log.info(f"Ordering {quantity} x '{product.name}'")
        if not config.dry_run:
            try:
                nemlig.add_product_to_basket(product.id, quantity)
            except nemlig.NemligException as ex:
                log.warn(f"{product.name} -> {ex}")


def parse_args(args):
    parser = ArgumentParser()
    parser.add_argument("-u", "--username", help="Nemlig.com username (email address)")
    parser.add_argument("-p", "--password", help="Nemlig.com password")
    parser.add_argument("--cache-dir", default=".nemlig", help="Path to cache dir")
    parser.add_argument("--no-refresh", action="store_true", help="Use orders from cache only")
    parser.add_argument("--window-min", default=2, help="Min number of recent purchases of a specific product to consider")
    parser.add_argument("--window-max", default=4, help="Max number of recent purchases of a specific product to consider")
    parser.add_argument("--max-depth", default=100, help="Number of past orders to consider")
    parser.add_argument("--forget-after", default=3, help="Number of times to suggest purchaces of product before forgetting about it")
    parser.add_argument("--dry-run", action="store_true", help="Don't add products to Nemlig.com basket")
    return parser.parse_args(args)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main(sys.argv[1:])
