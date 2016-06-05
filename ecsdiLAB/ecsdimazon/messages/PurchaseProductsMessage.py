import uuid

from rdflib import Graph, Literal
from rdflib.namespace import Namespace, FOAF

from ecsdiLAB.ecsdimazon.controllers import Constants

from ecsdiLAB.ecsdimazon.model.User import User


class PurchaseProductsMessage:
    def __init__(self, eans, user, priority, payment):
        self.eans = eans
        self.user = user
        self.priority = priority
        self.payment = payment

    def to_graph(self):
        graph = Graph()
        n = Namespace(Constants.NAMESPACE)
        for ean in self.eans:
            uuid_guiones = uuid.uuid4()
            int_uuid = uuid_guiones.int
            p = n.__getattr__('#Product#' + str(int_uuid))
            graph.add((p, FOAF.EAN, Literal(ean)))
            graph.add((p, FOAF.Purchaser, Literal(self.user.username)))
            graph.add((p, FOAF.SendTo, Literal(self.user.direction)))
            graph.add((p, FOAF.Priority, Literal(self.priority)))
            graph.add((p, FOAF.Payment, Literal(self.payment)))
        return graph

    @classmethod
    def list_to_graph(cls, spms):
        graph = Graph()
        for spm in spms:
            graph = graph + spm.to_graph()
        return graph

    @classmethod
    def from_graph(cls, graph):
        query = """SELECT ?x ?ean ?purchaser ?send ?priority ?payment
            WHERE {
                ?x ns1:EAN ?ean.
                ?x ns1:Purchaser ?purchaser.
                ?x ns1:SendTo ?send.
                ?x ns1:Priority ?priority.
                ?x ns1:Payment ?payment.
            }
        """
        qres = graph.query(query)
        search_res = []
        send = None
        priority = None
        payment = None
        purchaser = None
        for p, ean, purchaser, send, priority, payment in qres:
            search_res.append(ean)
            purchaser = purchaser
            send = send
            payment = payment
            priority = priority
        pm = PurchaseProductsMessage(search_res, User(purchaser, send), priority, payment)
        return pm
