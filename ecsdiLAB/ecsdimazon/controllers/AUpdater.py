import json
import sys

from flask import Flask, request
from rdflib import Graph

from ecsdiLAB.ecsdimazon.context.ECSDIContext import ECSDIContext
from ecsdiLAB.ecsdimazon.controllers import AgentUtil
from ecsdiLAB.ecsdimazon.controllers import Constants
from ecsdiLAB.ecsdimazon.messages import Ontologies
from ecsdiLAB.ecsdimazon.messages.UploadProductMessage import UploadProductMessage
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


def upload_product(graph):
    upm = UploadProductMessage.from_graph(graph)
    upload_product_ean = upm.ean
    upload_product_name = upm.name
    upload_product_brand = upm.brand
    upload_product_price = upm.price
    upload_product_height = upm.height
    upload_product_widht = upm.width
    upload_product_weight = upm.weight

    product = Product(upload_product_ean, upload_product_name, upload_product_brand,
                      upload_product_price, upload_product_height, upload_product_widht,
                      upload_product_weight, upload_product_name)

    uploaded_product = context.product_service.upload_in_catalog(product)

    return Product.list_to_graph(uploaded_product).serialize()


@app.route('/comm', methods=['GET', 'POST'])
def comm():
    graph = Graph().parse(data=request.data, format='xml')
    ontology = AgentUtil.ontology_of_message(graph)
    return routings[ontology](graph)


routings = {
    Ontologies.UPLOAD_PRODUCT_MESSAGE: upload_product
}

if __name__ == '__main__':
    app.run(port=Constants.PORT_AUPDATER, debug=True)
