from ecsdiLAB.ecsdimazon.controllers import Constants
from ecsdiLAB.ecsdimazon.model.Product import Product
from ecsdiLAB.ecsdimazon.model.SellingCompany import SellingCompany


class InternalProduct(Product):
    def __init__(self, uuid, ean, name, brand, price, weight, height, width):
        Product.__init__(self, uuid, ean, name, brand, price, weight, height, width,
                         SellingCompany(Constants.OUR_SELLING_COMPANY_NAME))
