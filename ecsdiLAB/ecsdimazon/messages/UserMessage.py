from rdflib import Graph, Literal
from rdflib.namespace import Namespace, FOAF

from ecsdiLAB.ecsdimazon.controllers import Constants
from ecsdiLAB.ecsdimazon.model.BoughtProduct import BoughtProduct
from ecsdiLAB.ecsdimazon.model.Product import Product

from ecsdiLAB.ecsdimazon.model.User import User


class UserMessage:
    def __init__(self, user):
        self.user = user

    def to_graph(self):
        graph = Graph()
        n = Namespace(Constants.NAMESPACE)
        p = n.__getattr__('#User#' + str(self.user.username))
        graph.add((p, FOAF.Username, Literal(self.user.username)))
        graph.add((p, FOAF.Direction, Literal(self.user.direction)))
        return graph

    @classmethod
    def list_to_graph(cls, spms):
        graph = Graph()
        for spm in spms:
            graph = graph + spm.to_graph()
        return graph

    @classmethod
    def from_graph(cls, graph):
        query = """SELECT ?x ?username ?direction
            WHERE {
                ?x ns1:Username ?username.
                ?x ns1:Direction ?direction.
            }
        """
        qres = graph.query(query)
        for p, username, direction in qres:
            pm = UserMessage(User(username,direction))
            return pm
