from rdflib import Graph


class ProductService:

    def __init__(self):
        self.products = Graph().parse("products.rdf", format="turtle")

    @classmethod
    def search(self, name, price_min, price_max, seller, weight_min, weight_max):
