import requests
import sys
from rdflib import Graph
from ecsdiLAB.ecsdimazon.messages import Ontologies
from ecsdiLAB.ecsdimazon.controllers import Constants
from ecsdiLAB.ecsdimazon.controllers.AgentUtil import build_message
from ecsdiLAB.ecsdimazon.messages.UploadProductMessage import UploadProductMessage
from ecsdiLAB.ecsdimazon.model.Product import Product


def main():
    seller = enter_seller_information()
    system_exit = False
    while not system_exit:
        create_product(seller)
        correct_response = False
        while not correct_response:
            system_exit = raw_input("Salir? (y/n) ")
            if system_exit == 'y' or system_exit == 'n':
                if system_exit == 'y':
                    system_exit = True
                else:
                    system_exit = False
                correct_response = True

def enter_seller_information():
    seller = ""
    valid_seller = False
    while not valid_seller:
        seller = raw_input("seller: ")
        if seller != "":
            valid_seller = True
    return seller

def create_product(seller):
    url = "http://localhost:" + str(Constants.PORT_AUPDATER) + "/comm"
    ean = raw_input("ean: ")
    if ean is "":
        return
    name = raw_input("name: ")
    brand = raw_input("brand: ")
    price = raw_input("price: ")
    height = raw_input("height: ")
    width = raw_input("width: ")
    weight = raw_input("weight: ")

    product_upload = UploadProductMessage(ean, name, brand, price, height, width, weight, seller)

    response = requests.get(url, data=build_message(product_upload.to_graph(), '', Ontologies.UPLOAD_PRODUCT_MESSAGE)
                            .serialize(format='xml'))

    try:
        products_graph = Graph().parse(data=response.text, format='xml')
        """products = Product.from_graph(products_graph)
        i = 1
        for product in products:
            brand_split = str(product.brand).split('#')
            seller_split = str(product.seller).split('#')
            print str(i) + ". Codigo de barras: " + str(product.ean) + ", Nombre: " + str(product.name) + ", Marca: " + \
                  brand_split[len(brand_split) - 1] + ", Vendedor: " + seller_split[
                      len(seller_split) - 1] + ", Precio: " + str(product.price)
            i += 1
            """
    except:
        print "No se ha podido crear el producto"


if __name__ == "__main__":
    main()
