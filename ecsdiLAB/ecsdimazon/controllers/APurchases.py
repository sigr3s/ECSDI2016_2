import json

from flask import Flask, request
from rdflib import Graph

from ecsdiLAB.ecsdimazon.context.ECSDIContext import ECSDIContext
from ecsdiLAB.ecsdimazon.controllers import Constants
from ecsdiLAB.ecsdimazon.model.Product import Product
from ecsdiLAB.ecsdimazon.controllers import AgentUtil
from ecsdiLAB.ecsdimazon.messages import Ontologies
from ecsdiLAB.ecsdimazon.messages.PurchaseProductsMessage import PurchaseProductsMessage

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


def purchase_products(graph):
    ppm = PurchaseProductsMessage.from_graph(graph)
    products = context.product_service.purchase(ppm.eans)
    return json.dumps(products)


@app.route('/comm', methods=['POST'])
def comm():
    ontology = AgentUtil.ontology_of_message(request.data)
    routings[ontology](Graph().parse(data=request.data))


routings = {
    Ontologies.PURCHASE_PRODUCT_MESSAGE: purchase_products
}

if __name__ == '__main__':
    app.run(port=Constants.PORT_APURCHASES)
