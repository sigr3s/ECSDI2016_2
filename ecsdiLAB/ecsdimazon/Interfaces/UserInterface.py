import requests
import sys
from rdflib import Graph
from ecsdiLAB.ecsdimazon.messages import Ontologies
from ecsdiLAB.ecsdimazon.controllers import Constants
from ecsdiLAB.ecsdimazon.messages.SearchProductsMessage import SearchProductsMessage
from ecsdiLAB.ecsdimazon.messages.PurchaseProductsMessage import PurchaseProductsMessage
from ecsdiLAB.ecsdimazon.controllers.AgentUtil import build_message
from ecsdiLAB.ecsdimazon.model.Product import Product


def main():
    option = -1
    while option != 0:
        print "0. Salir"
        print "1. Buscar productos"
        print "2. Ir a la cesta de la compra"
        option = raw_input("Escoge una opcion: ")
        try:
            option = int(option)
        except ValueError:
            pass
        if option not in [0, 1, 2]:
            print "Opcion incorrecta"
        else:
            if option == 1:
                search_product()
            if option == 2:
                show_cart()


def bought_products():
    eans = []
    purchase_url = "http://localhost:" + str(Constants.PORT_APURCHASES) + "/comm"
    ean_to_buy = raw_input("Ean of the product you want: ")
    eans.append(ean_to_buy)
    product_purchase = PurchaseProductsMessage(eans)
    response = requests.post(purchase_url, data=build_message(product_purchase.to_graph(), '',
                                                              Ontologies.PURCHASE_PRODUCT_MESSAGE).serialize(
        format='xml'))
    print response


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
            print str(i) + ". " + print_product(product)
            i += 1
        print
        list_of_products = raw_input("Introduce los productos que quieres o dejalo en blanco si no quieres nada de la lista: ")
        if list_of_products != "":
            lopSplit = list_of_products.strip().split(" ")
            try:
                i = 0
                for prod in lopSplit:
                    lopSplit[i] = int(prod) - 1
                    i += 1
                add_to_cart(lopSplit, products)
            except ValueError:
                print "todos los valores han de ser numericos"
    except:
        print "No hay productos que coincidan con los parametros pasados"
    print


def add_to_cart(lop, products):
    for prod_num in lop:
        try:
            how_many = cart[products[prod_num]]
            cart[products[prod_num]] = how_many + 1
        except:
            cart[products[prod_num]] = 1


def show_cart():
    for key, value in cart.iteritems():
        print print_product(key) + ": " + str(value)
    option = raw_input("Comprar? y/n")
    if(option == 'y'):
        purchase()
    print


def purchase():
    """todo"""


def print_product(product):
    brand_split = str(product.brand).split('#')
    seller_split = str(product.seller).split('#')
    return "Codigo de barras: " + str(product.ean) + ", Nombre: " + str(product.name) + ", Marca: " + \
          brand_split[len(brand_split) - 1] + ", Vendedor: " + seller_split[len(seller_split) - 1] + ", Precio: " + str(product.price)


if __name__ == "__main__":
    global cart
    cart = {}
    main()
