from rdflib import Graph, Literal
from rdflib.namespace import Namespace, FOAF

from ecsdiLAB.ecsdimazon.controllers import Constants


class UploadProductMessage:
    def __init__(self, ean, name, brand, price, height, width, weight, seller):
        self.ean = ean
        self.name = name
        self.brand = brand
        self.price = price
        self.height = height
        self.width = width
        self.weight = weight
        self.seller = seller

    def to_graph(self):
        graph = Graph()
        n = Namespace(Constants.NAMESPACE)
        p = n.__getattr__('#Product#' + str(self.ean))
        graph.add((p, FOAF.EAN, Literal(self.ean)))
        graph.add((p, FOAF.Name, Literal(self.name)))
        graph.add((p, FOAF.Brand, Literal(self.brand)))
        graph.add((p, FOAF.Price, Literal(self.price)))
        graph.add((p, FOAF.Height, Literal(self.height)))
        graph.add((p, FOAF.Width, Literal(self.width)))
        graph.add((p, FOAF.Weight, Literal(self.weight)))
        graph.add((p, FOAF.Seller, Literal(self.seller)))
        return graph

    @classmethod
    def list_to_graph(cls, upms):
        graph = Graph()
        for upm in upms:
            graph = graph + upm.to_graph()
        return graph

    @classmethod
    def from_graph(cls, graph):
        query = """SELECT ?x ?ean ?name ?brand ?price
                            ?height ?width ?weight ?seller
            WHERE {
                ?x ns1:EAN ?ean.
                ?x ns1:Name ?name.
                ?x ns1:Brand ?brand.
                ?x ns1:Price ?price.
                ?x ns1:Height ?height.
                ?x ns1:Width ?width.
                ?x ns1:Weight ?weight.
                ?x ns1:Seller ?seller.
            }"""
        qres = graph.query(query)
        for p, ean, name, brand, price, height, width, weight, seller in qres:
            return UploadProductMessage(
                ean.toPython(),
                name.toPython(),
                brand.toPython(),
                price.toPython(),
                height.toPython(),
                width.toPython(),
                weight.toPython(),
                seller.toPython())
