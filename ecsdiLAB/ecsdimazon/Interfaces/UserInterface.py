import requests
import sys
from rdflib import Graph
from ecsdiLAB.ecsdimazon.messages import Ontologies
from ecsdiLAB.ecsdimazon.controllers import Constants
from ecsdiLAB.ecsdimazon.messages.SearchProductsMessage import SearchProductsMessage
from ecsdiLAB.ecsdimazon.controllers.AgentUtil import build_message
from ecsdiLAB.ecsdimazon.model.Product import Product


def main():
    system_exit = False
    while not system_exit:
        search_product()
        correct_response = False
        while not correct_response:
            system_exit = raw_input("Salir? (y/n) ")
            if system_exit == 'y' or system_exit == 'n':
                if system_exit == 'y':
                    system_exit = True
                else:
                    system_exit = False
                correct_response = True

    """
        TODO seleccionar producto para comprar
    """


def search_product():
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

    response = requests.get(url, data=build_message(product_search.to_graph(), '', Ontologies.SEARCH_PRODUCT_MESSAGE)
                            .serialize(format='xml'))

    try:
        products_graph = Graph().parse(data=response.text, format='xml')
        products = Product.from_graph(products_graph)
        i = 1
        for product in products:
            brand_split = str(product.brand).split('#')
            seller_split = str(product.seller).split('#')
            print str(i) + ". Codigo de barras: " + str(product.ean) + ", Nombre: " + str(product.name) + ", Marca: " + brand_split[len(brand_split)-1] + ", Vendedor: " + seller_split[len(seller_split)-1] + ", Precio: " + str(product.price)
            i += 1
    except:
        print "No hay productos que coincidan con los parametros pasados"


if __name__ == "__main__":
    main()
