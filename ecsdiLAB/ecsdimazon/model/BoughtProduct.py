from rdflib import Graph, Literal

from ecsdiLAB.ecsdimazon.controllers import Constants
from rdflib.namespace import RDF, Namespace, OWL, FOAF

from ecsdiLAB.ecsdimazon.model.Brand import Brand
from ecsdiLAB.ecsdimazon.model.Product import Product
from ecsdiLAB.ecsdimazon.model.SellingCompany import SellingCompany


class BoughtProduct:

    def __init__(self, uuid, product, purchaser, priority, payment, delivery_date, sender):
        self.uuid = uuid
        self.product = product
        self.priority = priority
        self.payment = payment
        self.purchaser = purchaser
        self.delivery_date = delivery_date
        self.sender = sender

    def to_graph(self):
        graph = Graph()
        n = Namespace(Constants.NAMESPACE)
        p = n.__getattr__('#BoughtProduct#' + str(self.uuid))
        graph.add((p, FOAF.Uuid, Literal(self.uuid)))
        graph.add((p, FOAF.EAN, Literal(self.product.ean)))
        graph.add((p, FOAF.Name, Literal(self.product.name)))
        graph.add((p, FOAF.Brand, n.__getattr__('#Brand#' + str(self.product.brand.name))))
        graph.add((p, FOAF.Price, Literal(self.product.price)))
        graph.add((p, FOAF.Weight, Literal(self.product.weight)))
        graph.add((p, FOAF.Height, Literal(self.product.height)))
        graph.add((p, FOAF.Width, Literal(self.product.width)))
        graph.add((p, FOAF.Purcahser, Literal(self.purchaser.username)))
        graph.add((p, FOAF.SendTo, Literal(self.purchaser.direction)))
        graph.add((p, FOAF.Payment, Literal(self.payment)))
        graph.add((p, FOAF.Priority, Literal(self.priority)))
        graph.add((p, FOAF.Seller, n.__getattr__('#Seller#' + str(self.product.seller.name))))
        graph.add((p, FOAF.DeliveryDate, Literal(self.delivery_date)))
        graph.add((p, FOAF.Sender, Literal(self.sender)))
        return graph

    @classmethod
    def list_to_graph(cls, products):
        graph = Graph()
        for product in products:
            graph = graph + product.to_graph()
        return graph

    @classmethod
    def from_graph(cls, graph):
        query = """SELECT ?x ?uuid ?ean ?name ?brand ?price ?weight ?height ?width ?purcahser ?sendto ?payment ?priority ?seller ?deliveryDate ?sender
            WHERE {
                ?x ns1:Uuid ?uuid.
                ?x ns1:EAN ?ean.
                ?x ns1:Name ?name.
                ?x ns1:Brand ?brand.
                ?x ns1:Price ?price.
                ?x ns1:Weight ?weight.
                ?x ns1:Height ?height.
                ?x ns1:Width ?width.
                ?x ns1:Purcahser ?purcahser.
                ?x ns1:SendTo ?sendto.
                ?x ns1:Payment ?payment.
                ?x ns1:Priority ?priority.
                ?x ns1:Seller ?seller.
                ?x ns1:DeliveryDate ?deliveryDate.
                ?x ns1:Sender ?sender.
            }
        """
        qres = graph.query(query)
        search_res = []
        for bp, uuid, ean, name, brand, price, weight, height, width, purcahser, sendto, payment, priority, seller, deliveryDate, sender in qres:
            search_res.append(BoughtProduct(
                uuid.toPython(),
                Product(ean, name, Brand(brand.toPython()), price, weight, height, width,
                        SellingCompany(seller.toPython())),
                purcahser.toPython(),
                priority.toPython(),
                payment.toPython(),
                deliveryDate.toPython(),
                sender.toPython()
            ))
        return search_res
