from rdflib import Graph, Literal

from ecsdiLAB.ecsdimazon.controllers import Constants
from ecsdiLAB.ecsdimazon.model.Brand import Brand
from ecsdiLAB.ecsdimazon.model.SellingCompany import SellingCompany
from rdflib.namespace import RDF, Namespace, OWL, FOAF


class BoughtProduct:
    def __init__(self, uuid, product):
        self.uuid = uuid
        self.product = product

    def to_graph(self):
        graph = Graph()
        n = Namespace(Constants.NAMESPACE)
        p = n.__getattr__('#BoughtProduct#' + str(self.uuid))
        graph.add((p, FOAF.Uuid, Literal(self.uuid)))
        graph.add((p, FOAF.EAN, Literal(self.product.ean)))
        graph.add((p, FOAF.Name, Literal(self.product.name)))
        graph.add((p, FOAF.Brand, n.__getattr__('#Brand#' + str(self.product.brand.name))))
        graph.add((p, FOAF.Price, Literal(self.product.price)))
        graph.add((p, FOAF.Weight, Literal(self.product.weight)))
        graph.add((p, FOAF.Height, Literal(self.product.height)))
        graph.add((p, FOAF.Width, Literal(self.product.width)))
        graph.add((p, FOAF.Seller, n.__getattr__('#Seller#' + str(self.product.seller.name))))
        return graph

    @classmethod
    def list_to_graph(cls, products):
        graph = Graph()
        for product in products:
            graph = graph + product.to_graph()
        return graph

