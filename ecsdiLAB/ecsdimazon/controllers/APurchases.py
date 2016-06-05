import json

import requests
from flask import Flask, request
from rdflib import Graph

from ecsdiLAB.ecsdimazon.context.ECSDIContext import ECSDIContext
from ecsdiLAB.ecsdimazon.controllers import AgentUtil
from ecsdiLAB.ecsdimazon.controllers import Constants
from ecsdiLAB.ecsdimazon.controllers.AgentUtil import build_message
from ecsdiLAB.ecsdimazon.messages import Ontologies, FIPAACLPerformatives
from ecsdiLAB.ecsdimazon.messages.PurchaseProductsMessage import PurchaseProductsMessage
from ecsdiLAB.ecsdimazon.messages.ReturnProductsMessage import ReturnProductsMessage
from ecsdiLAB.ecsdimazon.messages.SendProductsMessage import SendProductsMessage
from ecsdiLAB.ecsdimazon.model.BoughtProduct import BoughtProduct

app = Flask(__name__)
context = ECSDIContext()
agent_ASender = None

@app.route('/')
def hello_world():
    links = []
    for rule in app.url_map.iter_rules():
        methods = str(rule.methods)
        route = rule.rule
        links.append(methods + " : " + route)
    return json.dumps(links)

def return_products(graph):
    rpm = ReturnProductsMessage.from_graph(graph)
    return context.product_service.return_prod(rpm.uuid, rpm.username, rpm.reason)


def purchase_products(graph):
    ppm = PurchaseProductsMessage.from_graph(graph)
    products = context.product_service.purchase(ppm.eans, ppm.user, ppm.priority, ppm.payment)
    product_send = SendProductsMessage(products)
    send_url = agent_ASender + "/comm"
    requests.post(send_url, data=build_message(product_send.to_graph(), FIPAACLPerformatives.REQUEST,
                                               Ontologies.SEND_PRODUCTS_MESSAGE).serialize(
        format='xml'))
    return BoughtProduct.list_to_graph(products).serialize(format='xml')


@app.route('/comm', methods=['POST'])
def comm():
    graph = Graph().parse(data=request.data, format='xml')
    ontology = AgentUtil.ontology_of_message(graph)
    return routings[ontology](graph)


routings = {
    Ontologies.PURCHASE_PRODUCT_MESSAGE: purchase_products,
    Ontologies.RETURN_PRODUCT_MESSAGE: return_products,
    Ontologies.SENT_PRODUCTS_MESSAGE: context.product_service.sent_products
}

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 2:
        print "USAGE: python APurchases {ASENDER_URI}"
        exit(-1)
    agent_ASender = sys.argv[1]
    app.run(port=Constants.PORT_APURCHASES, debug=True)
