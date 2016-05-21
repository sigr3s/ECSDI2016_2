from flask import Flask, request, Response
from ecsdiLAB import ProductService
import json

app = Flask(__name__)


@app.route('/')
def hello_world():
    return ""


@app.route('/products/search', methods=['GET'])
def search_products():
    search_product_name = request.args.get('name')
    search_product_price_min = request.args.get('priceMin')
    search_product_price_max = request.args.get('priceMax')
    search_product_seller = request.args.get('seller')
    search_product_weight_max = request.args.get('weightMax')
    search_product_weight_min = request.args.get('weightMin')

    ps = ProductService()

    return ps.search(search_product_name, search_product_price_min, search_product_price_max, search_product_seller,
                     search_product_weight_min, search_product_weight_max)


if __name__ == '__main__':
    app.run()
