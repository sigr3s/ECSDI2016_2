from rdflib import Graph, Literal

from ecsdiLAB.ecsdimazon.controllers import Constants
from rdflib.namespace import RDF, Namespace, OWL, FOAF

from ecsdiLAB.ecsdimazon.model.Brand import Brand


class BoughtProductResponse:
    def __init__(self, uuid, ean, name, brand, price, seller, delivery_date, sender):
        self.uuid = uuid
        self.ean = ean
        self.name = name
        self.brand = brand
        self.price = price
        self.seller = seller
        self.delivery_date = delivery_date
        self.sender = sender

    def to_graph(self):
        graph = Graph()
        n = Namespace(Constants.NAMESPACE)
        p = n.__getattr__('#BoughtProduct#' + str(self.uuid))
        graph.add((p, FOAF.Uuid, Literal(self.uuid)))
        graph.add((p, FOAF.EAN, Literal(self.ean)))
        graph.add((p, FOAF.Name, Literal(self.name)))
        graph.add((p, FOAF.Brand, n.__getattr__('#Brand#' + str(self.brand))))
        graph.add((p, FOAF.Price, Literal(self.price)))
        graph.add((p, FOAF.Seller, n.__getattr__('#Seller#' + str(self.seller))))
        graph.add((p, FOAF.Sender, Literal(self.sender)))
        graph.add((p, FOAF.DeliveryDate, Literal(self.delivery_date)))
        return graph

    @classmethod
    def list_to_graph(cls, products):
        graph = Graph()
        for product in products:
            graph = graph + product.to_graph()
        return graph

    @classmethod
    def from_graph(cls, graph):
        query = """SELECT ?x ?uuid ?ean ?name ?brand ?price ?seller ?sender ?deliveryDate
               WHERE {
                   ?x ns1:Uuid ?uuid.
                   ?x ns1:EAN ?ean.
                   ?x ns1:Name ?name.
                   ?x ns1:Brand ?brand.
                   ?x ns1:Price ?price.
                   ?x ns1:Seller ?seller.
                   ?x ns1:Sender ?sender.
                   ?x ns1:DeliveryDate ?deliveryDate.
               }
           """
        qres = graph.query(query)
        search_res = []
        for bpr, uuid, ean, name, brand, price, seller, sender, deliveryDate in qres:
            search_res.append(BoughtProductResponse(
                uuid.toPython(),
                ean.toPython(),
                name.toPython(),
                Brand(brand.toPython()),
                price.toPython(),
                seller.toPython(),
                deliveryDate.toPython(),
                sender.toPython()
            ))
        return search_res