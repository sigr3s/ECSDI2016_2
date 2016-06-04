import requests
import sys
from rdflib import Graph
from ecsdiLAB.ecsdimazon.messages import Ontologies
from ecsdiLAB.ecsdimazon.controllers import Constants
from ecsdiLAB.ecsdimazon.messages.SearchProductsMessage import SearchProductsMessage
from ecsdiLAB.ecsdimazon.messages.PurchaseProductsMessage import PurchaseProductsMessage
from ecsdiLAB.ecsdimazon.controllers.AgentUtil import build_message
from ecsdiLAB.ecsdimazon.model.Product import Product


def main():
    url = "http://localhost:" + str(Constants.PORT_AUSER) + "/comm"
    ean = raw_input("ean: ")
    name = ''
    brand = ''
    price_min = 0
    price_max = sys.float_info.max
    if ean is "":
        ean = None
        name = raw_input("name: ")
        brand = raw_input("brand: ")
        price_min = raw_input("price min: ")
        price_max = raw_input("price max: ")
        if price_min == "":
            price_min = 0
        if price_max == "":
            price_max = sys.float_info.max

    product_search = SearchProductsMessage(ean, name, brand, price_min, price_max)
    print url

    response = requests.get(url, data=build_message(product_search.to_graph(), '', Ontologies.SEARCH_PRODUCT_MESSAGE).serialize(format='xml'))
    print response
    if response == "":
        print "No hay productos con los parametros dados"
    else:
        products_graph = Graph().parse(data=response.text, format='xml')
        products = Product.from_graph(products_graph)
        for product in products:
            print product.name
    eans = []
    purchase_url = "http://localhost:" + str(Constants.PORT_APURCHASES) + "/comm"
    eanToBuy = raw_input("Ean of the product you want: ")
    eans.append(eanToBuy)
    product_purchase = PurchaseProductsMessage(eans)
    response = requests.post(purchase_url, data=build_message(product_purchase.to_graph(), '',
                                                    Ontologies.PURCHASE_PRODUCT_MESSAGE).serialize(format='xml'))
    print response
    """
        TODO seleccionar producto para comprar
    """

if __name__ == "__main__":
    main()
