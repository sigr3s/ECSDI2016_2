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
        if seller != "" and seller.find(" ") == -1:
            valid_seller = True
        else :
            print "El vendedor no puede estar vacio ni contener espacios"
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
                    print "El codigo de barras no puede estar vacio"
                    ean = raw_input("codigo de barras: ")
                correct = True
            except ValueError as ve:
                print "El codigo de barras tiene que ser un entero positivo"

        name = raw_input("nombre: ")
        while name.strip() == "" :
            print "El nombre no puede estar vacio"
            name = raw_input("nombre: ")

        brand = raw_input("marca: ")
        brand = brand.strip()
        while brand != "" and brand.find(" ") != -1:
            print "La marca no puede estar vacia ni contener espacios"
            brand = raw_input("marca: ")
            brand = brand.strip()

        correct = False
        while not correct:
            try:
                price = raw_input("precio: ")
                while (price.strip() == "" or float(price) < 0):
                    print "El precio no puede estar vacio"
                    price = raw_input("precio: ")
                correct = True
            except ValueError as ve:
                print "El precio tiene que ser un real positivo"

        correct = False
        while not correct:
            try:
                height = raw_input("altura: ")
                while (height.strip() == "" or float(height) < 0):
                    print "La altura no puede estar vacia"
                    height = raw_input("altura: ")
                correct = True
            except ValueError as ve:
                print "La altura tiene que ser un real positivo"

        correct = False
        while not correct:
            try:
                width = raw_input("anchura: ")
                while (width.strip() == "" or float(width) < 0):
                    print "La anchura no puede estar vacia"
                    width = raw_input("anchura: ")
                correct = True
            except ValueError as ve:
                print "La anchura tiene que ser un real positivo"

        correct = False
        while not correct:
            try:
                weight = raw_input("peso: ")
                while (weight.strip() == "" or float(weight) < 0):
                    print "El peso no puede estar vacio"
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
