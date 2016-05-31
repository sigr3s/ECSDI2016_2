from pip._vendor import requests
from rdflib import Graph
from ecsdiLAB.ecsdimazon.controllers import Constants
from ecsdiLAB.ecsdimazon.model.Product import Product


def main():
    search_direction = "http://localhost:" + str(Constants.PORT_AUSER) + "/products/search?"
    ean = raw_input("ean: ")
    if ean == "":
        name = raw_input("name: ")
        brand = raw_input("brand: ")
        price_min = raw_input("price min: ")
        price_max = raw_input("namprice max: ")
        search_direction += "name=" + name + "&brand=" + brand + "&priceMin=" + price_min + "&priceMax=" + price_max
    else:
        search_direction += "ean=" + ean
    req = requests.get(search_direction).text
    print req
    gres = Graph().parse(data=req, format='xml')
    products = Product.from_graph(gres)
    """
        TODO seleccionar producto para comprar
    """
    for product in products:
        print product.name


if __name__ == "__main__":
    main()
