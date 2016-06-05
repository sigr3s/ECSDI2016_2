from rdflib import Graph, Literal
from rdflib.namespace import Namespace, FOAF

from ecsdiLAB.ecsdimazon.controllers import Constants

from ecsdiLAB.ecsdimazon.model.User import User


class ReturnProductsMessage:
    def __init__(self, uuid, username, reason):
        self.uuid = uuid
        self.username = username
        self.reason = reason

    def to_graph(self):
        graph = Graph()
        n = Namespace(Constants.NAMESPACE)
        p = n.__getattr__('#BoughtProduct#' + str(self.uuid))
        graph.add((p, FOAF.Uuid, Literal(self.uuid)))
        graph.add((p, FOAF.Purchaser, Literal(self.username)))
        graph.add((p, FOAF.Reason, Literal(self.reason)))
        return graph

    @classmethod
    def list_to_graph(cls, spms):
        graph = Graph()
        for spm in spms:
            graph = graph + spm.to_graph()
        return graph

    @classmethod
    def from_graph(cls, graph):
        query = """SELECT ?x ?uuid ?purchaser ?reason
            WHERE {
                ?x ns1:Uuid ?uuid.
                ?x ns1:Purchaser ?purchaser.
                ?x ns1:Reason ?reason
            }
        """
        qres = graph.query(query)
        for p, uuid, purchaser, reason in qres:
            return ReturnProductsMessage(uuid, purchaser, reason)
