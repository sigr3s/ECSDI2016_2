import requests
import sys
from rdflib import Graph
from ecsdiLAB.ecsdimazon.messages import Ontologies
from ecsdiLAB.ecsdimazon.controllers import Constants
from ecsdiLAB.ecsdimazon.controllers.AgentUtil import build_message
from ecsdiLAB.ecsdimazon.messages.UploadProductMessage import UploadProductMessage
from ecsdiLAB.ecsdimazon.model.Product import Product


def main():
    print "Introduzca su nombre de vendedor"
    seller = enter_seller_information()
    system_exit = False
    while not system_exit:
        create_product(seller)
        correct_response = False
        while not correct_response:
            system_exit = raw_input("Salir? (s/n) ")
            if system_exit == 's' or system_exit == 'n':
                if system_exit == 's':
                    system_exit = True
                else:
                    system_exit = False
                correct_response = True

def enter_seller_information():
    seller = ""
    valid_seller = False
    while not valid_seller:
        seller = raw_input("vendedor: ")
        seller = seller.strip()
        if seller != "":
            valid_seller = True
    return seller

def create_product(seller):
    try :
        print "Introduzca los parametros del producto"
        url = "http://localhost:" + str(Constants.PORT_AUPDATER) + "/comm"

        correct = False
        while not correct:
            try:
                ean = raw_input("codigo de barras: ")
                while (ean.strip() == "" or int(ean) <= 0):
                    ean = raw_input("codigo de barras: ")
                correct = True
            except ValueError as ve:
                print "El codigo de barras tiene que ser un entero positivo"

        name = raw_input("nombre: ")
        while name.strip() == "" :
            name = raw_input("nombre: ")

        brand = raw_input("marca: ")
        while brand.strip() == "":
            brand = raw_input("marca: ")

        correct = False
        while not correct:
            try:
                price = raw_input("precio: ")
                while (price.strip() == "" or int(price) <= 0):
                    price = raw_input("precio: ")
                correct = True
            except ValueError as ve:
                print "El precio tiene que ser un real positivo"

        correct = False
        while not correct:
            try:
                height = raw_input("altura: ")
                while (height.strip() == "" or int(height) <= 0):
                    height = raw_input("altura: ")
                correct = True
            except ValueError as ve:
                print "La altura tiene que ser un real positivo"

        correct = False
        while not correct:
            try:
                width = raw_input("anchura: ")
                while (width.strip() == "" or int(width) <= 0):
                    width = raw_input("anchura: ")
                correct = True
            except ValueError as ve:
                print "La anchura tiene que ser un real positivo"

        correct = False
        while not correct:
            try:
                weight = raw_input("peso: ")
                while (weight.strip() == "" or int(weight) <= 0):
                    weight = raw_input("peso: ")
                correct = True
            except ValueError as ve:
                print "El peso tiene que ser un real positivo"

        product_upload = UploadProductMessage(int(ean), name, brand, float(price), float(height), float(width), float(weight), seller)

        response = requests.get(url, data=build_message(product_upload.to_graph(), '', Ontologies.UPLOAD_PRODUCT_MESSAGE)
                                .serialize(format='xml'))

        try:
            products_graph = Graph().parse(data=response.text, format='xml')

            if products_graph.__len__() == 0:
                print "Ya existe un producto para este ean: " + ean
            else :
                products = Product.from_graph(products_graph)
                for product in products:
                    brand_split = str(product.brand).split('#')
                    seller_split = str(product.seller).split('#')
                    print "Se ha creado el producto:"
                    print "Codigo de barras: " + str(product.ean) + ", Nombre: " + str(product.name) + ", Marca: " + \
                          brand_split[len(brand_split) - 1] + ", Vendedor: " + seller_split[
                              len(seller_split) - 1] + ", Precio: " + str(product.price)
                    print "Altura: " + str(product.height) + ", Anchura: " + str(product.width) + ", Peso: " + str(product.weight)
        except:
            print "No se ha podido crear el producto"
    except ValueError as ve:
        print "Los parametros anadidos no son correctos"



if __name__ == "__main__":
    main()
