from ecsdiLAB.ecsdimazon.model.Brand import Brand
from ecsdiLAB.ecsdimazon.model.SellingCompany import SellingCompany


class Product:
    def __init__(self, ean, name, brand, price, weight, height, width, seller):
        self.ean = ean
        self.name = name
        self.brand = brand
        self.price = price
        self.weight = weight
        self.height = height
        self.width = width
        self.seller = seller

    def to_json(self):
        product_json = {"ean": self.ean, "name": self.name, "brand": self.brand.name, "price": self.price,
                        "weight": self.weight, "height": self.height, "width": self.width, "seller": self.seller.name}
        return product_json

    @classmethod
    def from_json(cls, product_json):
        return Product(product_json["ean"],
                       product_json["name"],
                       Brand(product_json["brand"]),
                       product_json["price"],
                       product_json["weight"],
                       product_json["height"],
                       product_json["width"],
                       SellingCompany(product_json["seller"]))
