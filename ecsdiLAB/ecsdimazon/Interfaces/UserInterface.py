import requests
from rdflib import Graph

from ecsdiLAB.ecsdimazon.controllers import Constants
from ecsdiLAB.ecsdimazon.model.Product import Product


def main():
    search_direction = "http://localhost:" + str(Constants.PORT_AUSER) + "/products/search?"
    ean = raw_input("ean: ")
    if ean is "":
        need_and = False
        name = raw_input("name: ")
        brand = raw_input("brand: ")
        price_min = raw_input("price min: ")
        price_max = raw_input("price max: ")
        if name is not "":
            search_direction += "name=" + name
            need_and = True
        if brand is not "":
            if need_and:
                search_direction += "&"
            search_direction += "brand=" + brand
            need_and = True
        if price_min is not "":
            if need_and:
                search_direction += "&"
            search_direction += "priceMin=" + price_min
            need_and = True
        if price_max is not "":
            if need_and:
                search_direction += "&"
            search_direction += "priceMax=" + price_max
    else:
        search_direction += "ean=" + ean
    print search_direction
    req = requests.get(search_direction).text
    if req == "":
        print "No hay productos con los parametros dados"
    else:
        products_graph = Graph().parse(data=req, format='xml')
        products = Product.from_graph(products_graph)
        for product in products:
            print product.name

    """
        TODO seleccionar producto para comprar
    """

if __name__ == "__main__":
    main()
