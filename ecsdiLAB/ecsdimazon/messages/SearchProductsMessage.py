from rdflib import Graph, Literal
from rdflib.namespace import Namespace, FOAF

from ecsdiLAB.ecsdimazon.controllers import Constants


class SearchProductsMessage:
    def __init__(self, ean, name, brand, price_min, price_max):
        self.ean = ean
        self.name = name
        self.brand = brand
        self.price_min = price_min
        self.price_max = price_max

    def to_graph(self):
        graph = Graph()
        n = Namespace(Constants.NAMESPACE)
        p = n.__getattr__('#Product#' + str(self.ean))
        graph.add((p, FOAF.EAN, Literal(self.ean)))
        graph.add((p, FOAF.Name, Literal(self.name)))
        graph.add((p, FOAF.Brand, n.__getattr__('#Brand#' + str(self.brand))))
        graph.add((p, FOAF.PriceMin, Literal(self.price_min)))
        graph.add((p, FOAF.PriceMax, Literal(self.price_max)))
        return graph

    @classmethod
    def list_to_graph(cls, spms):
        graph = Graph()
        for spm in spms:
            graph = graph + spm.to_graph()
        return graph

    @classmethod
    def from_graph(cls, graph):
        query = """SELECT ?x ?ean ?name ?priceMin ?priceMax ?brand
            WHERE {
                ?x ns1:EAN ?ean.
                ?x ns1:Name ?name.
                ?x ns1:Brand ?brand.
                ?x ns1:PriceMin ?priceMin.
                ?x ns1:PriceMax ?priceMax.
            }
        """
        qres = graph.query(query)
        for p, ean, name, price_min, price_max, brand in qres:
            return SearchProductsMessage(
                ean.toPython(),
                name.toPython(),
                brand.toPython(),
                price_min.toPython(),
                price_max.toPython())
