from ecsdiLAB.ecsdimazon.model.Product import Product


class ExternalProduct(Product):

    def __init__(self, uuid, ean, name, brand, price, weight, height, width, seller):
        Product.__init__(self, uuid, ean, name, brand, price, weight, height, width, seller)