from rdflib import Graph, Namespace, Literal
from rdflib.namespace import FOAF
from ecsdiLAB.ecsdimazon.controllers import Constants


class Sender:
    def __init__(self, name, negotiatiotion_uri):
        self.name = name
        self.negotiation_uri = negotiatiotion_uri

    @classmethod
    def from_graph(cls, graph):
        query = """SELECT ?x ?name ?negotiationUri
            WHERE {{
                ?x ns1:Name ?name.
                ?x ns1:NegotiationUri ?negotiationUri.
            }}
            """
        qres = graph.query(query)
        for s, name, negotiation_uri in qres:
            return Sender(name, negotiation_uri)  # there will be only 1

    def to_graph(self):
        graph = Graph()
        n = Namespace(Constants.NAMESPACE)
        p = n.__getattr__('#Sender#' + str(self.name))
        graph.add((p, FOAF.Name, Literal(self.name)))
        graph.add((p, FOAF.NegotiationUri, Literal(self.negotiation_uri)))
        return graph
