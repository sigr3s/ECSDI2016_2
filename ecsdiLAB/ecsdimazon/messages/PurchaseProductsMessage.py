from rdflib import Graph, Literal
from rdflib.namespace import Namespace, FOAF

from ecsdiLAB.ecsdimazon.controllers import Constants


class PurchaseProductsMessage:
    def __init__(self, eans):
        self.eans = eans

    def to_graph(self):
        graph = Graph()
        n = Namespace(Constants.NAMESPACE)
        for ean in self.eans:
            p = n.__getattr__('#Product#' + str(ean))
            graph.add((p, FOAF.EAN, Literal(ean)))

        return graph


    @classmethod
    def list_to_graph(cls, spms):
        graph = Graph()
        for spm in spms:
            graph = graph + spm.to_graph()
        return graph

    @classmethod
    def from_graph(cls, graph):
        query = """SELECT ?x ?ean
            WHERE {
                ?x ns1:EAN ?ean.
            }
        """
        qres = graph.query(query)
        search_res = []
        for p, ean in qres:
           search_res.append(ean)
        pm = PurchaseProductsMessage(search_res)
        return pm
