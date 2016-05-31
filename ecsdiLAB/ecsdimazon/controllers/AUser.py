import json

from flask import Flask, request
from rdflib import Graph

from ecsdiLAB.ecsdimazon.context.ECSDIContext import ECSDIContext
from ecsdiLAB.ecsdimazon.controllers import AgentUtil
from ecsdiLAB.ecsdimazon.controllers import Constants
from ecsdiLAB.ecsdimazon.messages import Ontologies
from ecsdiLAB.ecsdimazon.messages.SearchProductsMessage import SearchProductsMessage
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


@app.route('/comm', methods=['GET', 'POST'])
def comm():
    ontology = AgentUtil.ontology_of_message(request.data)
    routings[ontology](Graph().parse(data=request.data))


routings = {
    Ontologies.SEARCH_PRODUCT_MESSAGE: search_products
}

if __name__ == '__main__':
    app.run(port=Constants.PORT_AUSER, debug=True)
