import requests
import sys
from rdflib import Graph
from ecsdiLAB.ecsdimazon.messages import Ontologies
from ecsdiLAB.ecsdimazon.controllers import Constants
from ecsdiLAB.ecsdimazon.messages.ReturnProductsMessage import ReturnProductsMessage
from ecsdiLAB.ecsdimazon.messages.SearchProductsMessage import SearchProductsMessage
from ecsdiLAB.ecsdimazon.messages.PurchaseProductsMessage import PurchaseProductsMessage
from ecsdiLAB.ecsdimazon.controllers.AgentUtil import build_message
from ecsdiLAB.ecsdimazon.model.BoughtProduct import BoughtProduct
from ecsdiLAB.ecsdimazon.model.Product import Product
from ecsdiLAB.ecsdimazon.model.User import User


def main():
    option = -1
    while option != 0:
        print "0. Salir"
        print "1. Buscar productos"
        print "2. Ir a la cesta de la compra"
        print "3. Devolver un producto"
        option = raw_input("Escoge una opcion: ")
        try:
            option = int(option)
        except ValueError:
            pass
        if option not in [0, 1, 2, 3]:
            print "Opcion incorrecta"
        else:
            if option == 1:
                search_product()
            if option == 2:
                show_cart()
            if option == 3:
                return_product()


def dictionary_to_eans_request(eans):
    for key, value in cart.iteritems():
        i = 0
        ean_of_product = key.ean
        while i < value:
            eans.append(str(ean_of_product))
            i += 1


def purchase_products():
    eans = []
    purchase_url = "http://localhost:" + str(Constants.PORT_APURCHASES) + "/comm"
    username = raw_input("Nombre de usuario: ")
    direction = raw_input("Direccion de envio: ")
    dictionary_to_eans_request(eans)

    product_purchase = PurchaseProductsMessage(eans, User(username,direction), Constants.PRIORITY_HIGH, Constants.PAYMENT_PAYPAL)
    response = requests.post(purchase_url, data=build_message(product_purchase.to_graph(), 'BUY',
                                                              Ontologies.PURCHASE_PRODUCT_MESSAGE).serialize(format='xml'))

    ticket = Graph().parse(data=response.text)
    print response.text
    print BoughtProduct.from_graph(ticket)
    if response.status_code == 200:
        global cart
        cart = {}


def return_product():
    purchase_url = "http://localhost:" + str(Constants.PORT_APURCHASES) + "/comm"
    username = raw_input("Nombre de usuario que quiere devolver productos: ")
    print "Escribe una lista con los uuid de los productos a devolver separados por espacios"
    ids_prod = raw_input("")
    if ids_prod.strip() == "":
        split_ids = ids_prod.strip().split(" ")
        try:
            uuids = []
            for id in split_ids:
                uuids.append(int(id))
            return_prod = ReturnProductsMessage(uuids, username)
            response = requests.post(purchase_url, data=build_message(return_prod.to_graph(), 'DELETE',
                                                                      Ontologies.RETURN_PRODUCT_MESSAGE).serialize(
                                                                      format='xml'))
            print response
        except ValueError:
            print "Todos los uuid han de ser numericos"

def search_product():
    url = "http://localhost:" + str(Constants.PORT_AUSER) + "/comm"
    print "Rellena los siguientes campos de busqueda, dejalos vacios si no quieres buscar por ese campo"
    ean = raw_input("Codigo de barras: ")
    name = ''
    brand = ''
    price_min = 0
    price_max = sys.float_info.max
    if ean is "":
        ean = None
        name = raw_input("Nombre: ")
        brand = raw_input("Marca: ")
        price_min = raw_input("Precio minimo de busqueda: ")
        price_max = raw_input("Precio maximo de busqueda: ")
        if price_min == "":
            price_min = 0
        if price_max == "":
            price_max = sys.float_info.max

    product_search = SearchProductsMessage(ean, name, brand, price_min, price_max)

    response = requests.get(url, data=build_message(product_search.to_graph(), 'QUERY', Ontologies.SEARCH_PRODUCT_MESSAGE)
                            .serialize(format='xml'))

    try:
        products_graph = Graph().parse(data=response.text, format='xml')
        products = Product.from_graph(products_graph)
        i = 1
        for product in products:
            print str(i) + ". " + print_product(product)
            i += 1
        print
        print "Haz una lista con los productos que quieres meter en el carrito separado por espacios. (num producto)x(cuantos quieres)"
        print "o dejalo en blanco si no quieres nada"
        list_of_products = raw_input("")
        if list_of_products != "":
            lopSplit = list_of_products.strip().split(" ")
            try:
                add_to_cart(lopSplit, products)
            except ValueError:
                print "Todos los valores han de ser numericos"
    except Exception as ex:
        print ex
        print "No hay productos que coincidan con los parametros pasados"
    print


def add_to_cart(lop, products):
    for prod_num in lop:
        prod_num_split = prod_num.split("x")
        try:
            how_many = cart[products[int(prod_num_split[0]) - 1]]
            cart[products[prod_num]] = how_many + int(prod_num_split[1])
        except:
            cart[products[int(prod_num_split[0]) - 1]] = int(prod_num_split[1])


def show_cart():
    if len(cart) != 0:
        for key, value in cart.iteritems():
            print print_product(key) + ". " + str(value) + " unidades"
        option = raw_input("Comprar? y/n: ")
        if (option == 'y'):
            purchase_products()
    else:
        print "No tienes productos en tu cesta"
    print


def print_product(product):
    brand_split = str(product.brand).split('#')
    seller_split = str(product.seller).split('#')
    return "Codigo de barras: " + str(product.ean) + ", Nombre: " + str(product.name) + ", Marca: " + \
           brand_split[len(brand_split) - 1] + ", Vendedor: " + seller_split[
               len(seller_split) - 1] + ", Precio: " + str(product.price)


if __name__ == "__main__":
    global cart
    cart = {}
    main()
