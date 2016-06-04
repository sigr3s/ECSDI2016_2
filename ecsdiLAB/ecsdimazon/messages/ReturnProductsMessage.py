from rdflib import Graph, Literal
from rdflib.namespace import Namespace, FOAF

from ecsdiLAB.ecsdimazon.controllers import Constants

from ecsdiLAB.ecsdimazon.model.User import User


class ReturnProductsMessage:
    def __init__(self, uuids, username):
        self.uuids = uuids
        self.username = username

    def to_graph(self):
        graph = Graph()
        n = Namespace(Constants.NAMESPACE)
        for uuid in self.uuids:
            p = n.__getattr__('#Product#' + str(uuid))
            graph.add((p, FOAF.Uuid, Literal(uuid)))
            graph.add((p, FOAF.Purchaser, Literal(self.username)))
        return graph

    @classmethod
    def list_to_graph(cls, spms):
        graph = Graph()
        for spm in spms:
            graph = graph + spm.to_graph()
        return graph

    @classmethod
    def from_graph(cls, graph):
        query = """SELECT ?x ?uuid ?purchaser
            WHERE {
                ?x ns1:Uuid ?uuid.
                ?x ns1:Purchaser ?purchaser.
            }
        """
        qres = graph.query(query)
        search_res = []
        purchaser = None;
        for p, uuid, purchaser in qres:
            search_res.append(uuid)
            purchaser = purchaser
        pm = ReturnProductsMessage(search_res,purchaser )
        return pm
