from pip._vendor import requests

from ecsdiLAB.ecsdimazon.controllers import Constants
from ecsdiLAB.ecsdimazon.model.Product import Product


def main():
    ean = raw_input("ean: ")
    name = raw_input("name: ")
    brand = raw_input("brand: ")
    price = raw_input("price: ")
    weight = raw_input("weight: ")
    height = raw_input("height: ")
    width = raw_input("width: ")
    seller = raw_input("seller: ")

    product = Product(ean,name,brand,price,weight,height,width,seller)
    productGraph = product.to_graph()

    url = "http://localhost:" + str(Constants.PORT_AUPDATER) + "/catalog"

    req = requests.post(url, productGraph)

    """req = requests.post(searchDirection,{ean,name,brand,price,weight,height,width,seller}).text"""
    print req

if __name__ == "__main__":
    main()
