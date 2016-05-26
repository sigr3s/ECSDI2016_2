import json

from flask import Flask, request
from rdflib import Graph

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


@app.route('/comm', methods=['POST'])
def purchase_products():
    products_to_buy = Product.from_rdf_xml(Graph().parse(data=request.get_data(as_text=True), format='xml'))
    products = context.product_service.purchase(products_to_buy)
    return json.dumps(products)


if __name__ == '__main__':
    app.run(port=Constants.PORT_APURCHASES)
