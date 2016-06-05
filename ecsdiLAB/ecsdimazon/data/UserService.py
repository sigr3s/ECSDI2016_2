import json
import uuid

from rdflib import Graph, Literal, URIRef
from rdflib.namespace import RDF, Namespace, OWL, FOAF

from ecsdiLAB.ecsdimazon.controllers import Constants
from ecsdiLAB.ecsdimazon.model.BoughtProduct import BoughtProduct
from ecsdiLAB.ecsdimazon.model.BoughtProductResponse import BoughtProductResponse
from ecsdiLAB.ecsdimazon.model.Brand import Brand
from ecsdiLAB.ecsdimazon.model.Product import Product
from ecsdiLAB.ecsdimazon.model.SellingCompany import SellingCompany


class UserService:
    def __init__(self):
        import os
        if not os.path.exists('users.rdf'):
            open('users.rdf', 'w')
        self.users = Graph().parse("users.rdf", format="turtle")
        if not os.path.exists('purchases.rdf'):
            open('purchases.rdf', 'w')
        self.purchases = Graph().parse("purchases.rdf", format="turtle")
        if not os.path.exists('catalog.rdf'):
            open('catalog.rdf', 'w')
        self.products = Graph().parse("catalog.rdf", format="turtle")

    def register_or_update(self, user):
        n = Namespace(Constants.NAMESPACE)
        uri = n.__getattr__('#User#' + str(user.username))
        if not (uri, None, None) in self.users:
            self.users.add((uri, FOAF.Username, user.username))
            self.users.add((uri, FOAF.Direction, user.username))
        else:
            self.users.remove((uri, FOAF.Direction, None))
            self.users.add((uri, FOAF.Direction, user.direction))
        return user

    def get_user_purchases(self, user):
        self.purchases = Graph().parse("purchases.rdf", format="turtle")
        self.products = Graph().parse("catalog.rdf", format="turtle")
        query = """SELECT ?x ?prod ?purchaser ?uuid
            WHERE {{
                ?x ns1:Product ?prod.
                ?x ns1:Purchaser ?purchaser.
                ?x ns1:Uuid ?uuid.
                FILTER  ( regex(?purchaser, "{0}", "i") )
            }}
            """.format( str(user.username))
        qres = self.purchases.query(query)
        result = []
        for x, prod, purchaser, uuid in qres:
            str_split = prod.split('#')
            eanP = str_split[- 1]
            query = """SELECT ?x ?ean ?name ?brand ?price ?seller ?sender ?date
            WHERE {{
                ?x ns1:EAN ?ean.
                ?x ns1:Name ?name.
                ?x ns1:Brand ?brand.
                ?x ns1:Price ?price.
                ?x ns1:Seller ?seller.
                ?x ns1:Sender ?sender.
                ?x ns1:DeliveryDate ?date.
                FILTER  ( {0} )}}""".format(
                "?ean = " + str(eanP))
            qprod = self.products.query(query)
            for x, ean, name, brand, price, seller, sender, date in qprod:
                result.append(BoughtProductResponse(uuid, ean, name, brand, price, seller, date, sender))
        return result
