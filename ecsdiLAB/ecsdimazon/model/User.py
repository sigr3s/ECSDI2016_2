from rdflib import Graph, Literal

from ecsdiLAB.ecsdimazon.controllers import Constants
from rdflib.namespace import RDF, Namespace, OWL, FOAF


class User:
    def __init__(self, username, direction):
        self.username = username
        self.direction = direction

    def to_graph(self):
        graph = Graph()
        n = Namespace(Constants.NAMESPACE)
        p = n.__getattr__('#User#' + str(self.username))
        graph.add((p, FOAF.Uuid, Literal(self.direction)))
        return graph

    @classmethod
    def user_to_graph(cls, user):
        graph = Graph()
        graph = user.to_graph()
        return graph

