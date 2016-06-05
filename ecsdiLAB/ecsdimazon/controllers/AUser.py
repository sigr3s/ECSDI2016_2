import json
import sys

from flask import Flask, request
from rdflib import Graph

from ecsdiLAB.ecsdimazon.context.ECSDIContext import ECSDIContext
from ecsdiLAB.ecsdimazon.controllers import AgentUtil
from ecsdiLAB.ecsdimazon.controllers import Constants
from ecsdiLAB.ecsdimazon.messages import Ontologies
from ecsdiLAB.ecsdimazon.messages.ReturnProductsMessage import ReturnProductsMessage
from ecsdiLAB.ecsdimazon.messages.SearchProductsMessage import SearchProductsMessage
from ecsdiLAB.ecsdimazon.messages.UserMessage import UserMessage
from ecsdiLAB.ecsdimazon.model.BoughtProductResponse import BoughtProductResponse
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


def search_products(graph):
    spm = SearchProductsMessage.from_graph(graph)
    search_product_name = spm.name
    search_product_price_min = spm.price_min
    search_product_price_max = spm.price_max
    search_product_brand = spm.brand
    search_product_ean = spm.ean

    searched_products = context.product_service.search(search_product_name,
                                                       search_product_brand,
                                                       search_product_price_min,
                                                       search_product_price_max,
                                                       search_product_ean)
    return Product.list_to_graph(searched_products).serialize()


def user_prodcuts(graph):
    spm = UserMessage.from_graph(graph)
    user_prod = context.user_service.get_user_purchases(spm.user)
    return BoughtProductResponse.list_to_graph(user_prod).serialize()


def user(graph):
    spm = UserMessage.from_graph(graph)
    context.user_service.register_or_update(spm.user)
    return None


@app.route('/comm', methods=['GET', 'POST'])
def comm():
    graph = Graph().parse(data=request.data, format='xml')
    ontology = AgentUtil.ontology_of_message(graph)
    return routings[ontology](graph)


routings = {
    Ontologies.SEARCH_PRODUCT_MESSAGE: search_products,
    Ontologies.USER_MESSAGE: user,
    Ontologies.USER_PRODUCTS_MESSAGE: user_prodcuts
}

if __name__ == '__main__':
    app.run(port=Constants.PORT_AUSER, debug=True)
