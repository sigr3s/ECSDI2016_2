import json

import sys
from flask import Flask, request

from ecsdiLAB.ecsdimazon.context.ECSDIContext import ECSDIContext
from ecsdiLAB.ecsdimazon.controllers import Constants
from ecsdiLAB.ecsdimazon.model.Product import Product

app = Flask(__name__)

context = ECSDIContext()


@app.route('/')
def hello_world():
    links = []
    for rule in app.url_map.iter_rules():
        methods = str(rule.methods)
        route = rule.rule
        links.append(methods + " : " + route)
    return json.dumps(links)


@app.route('/products/search', methods=['GET'])
def search_products():
    search_product_name = request.args.get('name', "")
    search_product_price_min = request.args.get('priceMin', 0)
    search_product_price_max = request.args.get('priceMax', sys.maxint)
    search_product_brand = request.args.get('brand', None)
    search_product_ean = request.args.get('ean', None)

    searched_products = context.product_service.search(search_product_name,
                                                       search_product_brand,
                                                       search_product_price_min,
                                                       search_product_price_max,
                                                       search_product_ean)
    return Product.list_to_graph(searched_products).serialize()


if __name__ == '__main__':
    app.run(port=Constants.PORT_AUSER, debug=True)
