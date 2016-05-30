import requests
from ecsdiLAB.ecsdimazon.controllers import Constants


def main():
    searchDirection = "http://localhost:" + str(Constants.PORT_AUSER) + "/products/search?"
    ean = raw_input("ean: ")
    if ean == "":
        name = raw_input("name: ")
        brand = raw_input("brand: ")
        price_min = raw_input("price min: ")
        price_max = raw_input("namprice max: ")
        searchDirection += "name=" + name + "&brand=" + brand + "&priceMin=" + price_min + "&priceMax=" + price_max
    else:
        searchDirection += "name=&ean=1"
    req = requests.get(searchDirection).text
    print req
    """products = Product.from_rdf_xml(Graph().parse(req, format='xml'))"""
    """
        TODO seleccionar producto para comprar
    """


if __name__ == "__main__":
    main()
