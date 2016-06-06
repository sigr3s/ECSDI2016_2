import sys

import requests
from rdflib import Graph

from ecsdiLAB.ecsdimazon.controllers import Constants
from ecsdiLAB.ecsdimazon.controllers.AgentUtil import build_message, performative_of_message
from ecsdiLAB.ecsdimazon.messages import Ontologies, FIPAACLPerformatives
from ecsdiLAB.ecsdimazon.messages.PurchaseProductsMessage import PurchaseProductsMessage
from ecsdiLAB.ecsdimazon.messages.ReturnProductsMessage import ReturnProductsMessage
from ecsdiLAB.ecsdimazon.messages.SearchProductsMessage import SearchProductsMessage
from ecsdiLAB.ecsdimazon.messages.UserMessage import UserMessage
from ecsdiLAB.ecsdimazon.model.BoughtProduct import BoughtProduct
from ecsdiLAB.ecsdimazon.model.BoughtProductResponse import BoughtProductResponse
from ecsdiLAB.ecsdimazon.model.Product import Product
from ecsdiLAB.ecsdimazon.model.User import User


def main():
    global user
    username = raw_input("Nombre del usuario que usara el sistema: ")
    while username.strip().find(" ") != -1:
        print "El nombre de usuario no puede contener espacios"
        username = raw_input("Nombre del usuario que usara el sistema: ")
    direccion = raw_input("Direccion del usuario: ")
    user = User(username.strip(), direccion)
    login()
    option = -1
    while option != 0:
        print "0. Salir"
        print "1. Buscar productos"
        print "2. Ir a la cesta de la compra"
        print "3. Devolver un producto"
        print "4. Consultar compras"
        option = raw_input("Escoge una opcion: ")
        print
        try:
            option = int(option)

            if option not in [0, 1, 2, 3, 4]:
                print "Opcion incorrecta"
            else:
                if option == 1:
                    search_product()
                if option == 2:
                    show_cart()
                if option == 3:
                    return_product()
                if option == 4:
                    user_purchases()
        except ValueError:
            print "Este valor ha de ser numerico"
        print


def login():
    users = auser + "/comm"
    user_msg = UserMessage(user)
    response = requests.post(users, data=build_message(user_msg.to_graph(), 'QUERY',
                                                       Ontologies.USER_MESSAGE).serialize(format='xml'))


def dictionary_to_eans_request(eans):
    for key, value in cart.iteritems():
        i = 0
        ean_of_product = key.ean
        while i < value:
            eans.append(str(ean_of_product))
            i += 1


def user_purchases():
    users = auser + "/comm"
    user_msg = UserMessage(user)
    response = requests.post(users, data=build_message(user_msg.to_graph(), 'QUERY',
                                                       Ontologies.USER_PRODUCTS_MESSAGE).serialize(format='xml'))
    try:
        products_graph = Graph().parse(data=response.text, format='xml')
        products = BoughtProductResponse.from_graph(products_graph)
        for product in products:
            print "Nombre: " + product.name + ", Precio: " + str(product.price) + ", uuid: " + str(
                product.uuid) + ", Repartidor: " + str(product.sender) + ", Fecha de entrega: " + str(
                product.delivery_date)
    except:
        print "No has comprado ningun producto aun."
    print


def purchase_products():
    eans = []
    purchase_url = apurchases + "/comm"
    dictionary_to_eans_request(eans)
    product_purchase = PurchaseProductsMessage(eans, user, Constants.PRIORITY_HIGH, Constants.PAYMENT_PAYPAL)
    response = requests.post(purchase_url, data=build_message(product_purchase.to_graph(), 'BUY',
                                                          Ontologies.PURCHASE_PRODUCT_MESSAGE).serialize(format='xml'))

    if response.status_code == 200:
        products_graph = Graph().parse(data=response.text, format='xml')
        products = BoughtProduct.from_graph(products_graph)
        for product in products:
            print print_product(product.product) + ", uuid: " + str(product.uuid)
        global cart
        cart = {}


def return_product():
    users = auser + "/comm"
    user_msg = UserMessage(user)
    purchase_url = apurchases + "/comm"
    response = requests.post(users, data=build_message(user_msg.to_graph(), 'QUERY',
                                                       Ontologies.USER_PRODUCTS_MESSAGE).serialize(format='xml'))
    products = []
    try:
        products_graph = Graph().parse(data=response.text, format='xml')
        products = list(enumerate(BoughtProductResponse.from_graph(products_graph)))
    except:
        print "No tienes productos para devolver"
        print
        return
    for i, product in products:
        print "{}. {} Fecha de entrega: {}".format(i+1, product.name, product.delivery_date)
    print "Escribe el id (primer numero) del producto a devolver"
    idx = raw_input("")
    try:
        int(idx)
    except:
        print "Este valor ha de ser numerico"
        print
        return
    products = dict(products)
    if not products.get(int(idx)-1):
        print "WRONG! Try again."
        return_product()
    print "Selecciona el motivo de tu devolucion:"
    print Constants.REASON_DICT[1]
    print Constants.REASON_DICT[2]
    print Constants.REASON_DICT[3]
    reason = raw_input("")
    try:
        int(reason)
    except:
        print "Este valor ha de ser numerico"
        print
        return
    if reason not in ['1', '2', '3']:
        print "WRONG! Try again."
        return_product()
    try:
        return_prod = ReturnProductsMessage(products.get(int(idx)).uuid, user.username, Constants.REASON_DICT[int(reason)])
        response = requests.post(purchase_url, data=build_message(return_prod.to_graph(), FIPAACLPerformatives.REQUEST,
                                                                  Ontologies.RETURN_PRODUCT_MESSAGE).serialize(
                                                                  format='xml'))
        graph = Graph().parse(data=response.text)
        if performative_of_message(graph) == FIPAACLPerformatives.AGREE:
            print "Un repartidor de Oops vendra manana a recoger el producto."
            return
        else:
            print "Han pasado ya 15 dias para tu motivo, no puedes devolver el producto."
    except:
        print "Error al devolver."
    print


def search_product():
    url = auser + "/comm"
    print "Rellena los siguientes campos de busqueda, dejalos vacios si no quieres buscar por ese campo"
    ean = raw_input("Codigo de barras: ")
    if ean != "":
        try:
            int(ean)
        except ValueError:
            print "El codigo de barras ha de ser numerico"
            print
            return
        name = ''
        brand = ''
        price_min = 0
        price_max = sys.float_info.max
    else:
        ean = None
        name = raw_input("Nombre: ")
        brand = raw_input("Marca: ")
        price_min = raw_input("Precio minimo de busqueda: ")
        price_max = raw_input("Precio maximo de busqueda: ")
        if price_min == "":
            price_min = 0
        if price_max == "":
            price_max = sys.float_info.max
    try:
        product_search = SearchProductsMessage(ean, name.strip(), brand.strip(), price_min, price_max)
        response = requests.get(url, data=build_message(product_search.to_graph(), 'QUERY', Ontologies.SEARCH_PRODUCT_MESSAGE)
                                .serialize(format='xml'))
        print

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
    if len(sys.argv) != 3:
        print "USAGE: python UserInteface {AUSER_URI} {APURCHASES_URI}"
        exit(-1)
    auser = sys.argv[1]
    apurchases = sys.argv[1]
    global cart
    cart = {}
    main()
