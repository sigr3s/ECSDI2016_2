import uuid

import datetime
from rdflib import Graph, Literal
from rdflib.namespace import RDF, Namespace, OWL, FOAF

from ecsdiLAB.ecsdimazon.controllers.AgentUtil import *
from ecsdiLAB.ecsdimazon.controllers import Constants
from ecsdiLAB.ecsdimazon.messages import FIPAACLPerformatives, Ontologies
from ecsdiLAB.ecsdimazon.model.BoughtProduct import BoughtProduct
from ecsdiLAB.ecsdimazon.model.Brand import Brand
from ecsdiLAB.ecsdimazon.model.Product import Product
from ecsdiLAB.ecsdimazon.model.SellingCompany import SellingCompany


class ProductService:
    def __init__(self):
        import os
        if not os.path.exists('catalog.rdf'):
            open('catalog.rdf', 'w')
        self.products = Graph().parse("catalog.rdf", format="turtle")
        if not os.path.exists('purchases.rdf'):
            open('purchases.rdf', 'w')
        self.purchases = Graph().parse("purchases.rdf", format="turtle")
        if not os.path.exists('returns.rdf'):
            open('returns.rdf', 'w')
        self.returns = Graph().parse("returns.rdf", format="turtle")

    def search(self, name, brand, price_min, price_max, ean):
        self.products = Graph().parse("catalog.rdf", format="turtle")
        query = """SELECT ?x ?ean ?name ?brand ?price ?weight ?height ?width ?seller
        WHERE {{
            ?x ns1:EAN ?ean.
            ?x ns1:Name ?name.
            ?x ns1:Brand ?brand.
            ?x ns1:Price ?price.
            ?x ns1:Weight ?weight.
            ?x ns1:Height ?height.
            ?x ns1:Width ?width.
            ?x ns1:Seller ?seller.
            FILTER (?price >= {0} && ?price <= {1} && regex(?name, "{2}", "i") {3} {4})
        }}
        """.format(price_min, price_max, name,
                   "&& ?brand = <" + brand + ">"
                   if brand and brand != "http://www.owl-ontologies.com/Ontology1463560793.owl#Brand#"
                   else "",
                   "" if ean is None or str(ean) == 'None' else " && ?ean = " + str(ean))
        print query
        qres = self.products.query(query)
        search_res = []
        for p, ean, name, brand, price, weight, height, width, seller in qres:
            search_res.append(Product(ean, name, Brand(brand), price, weight, height, width, SellingCompany(seller)))
        return search_res

    def upload_in_catalog(self, product):
        self.products = Graph().parse("catalog.rdf", format="turtle")
        query = """SELECT ?x ?ean
            WHERE {{
                ?x ns1:EAN ?ean.
            }}
            """.format("" if product.ean is None or str(product.ean) == 'None' else "?ean = " + str(product.ean))
        qres = self.products.query(query)
        upload_result = []
        for p, ean in qres:
            if str(ean) == str(product.ean):
                print "Found this ean"
                return upload_result

        n = Namespace(Constants.NAMESPACE)
        p = n.__getattr__('#Product#' + str(product.ean))

        self.products.add((p, FOAF.EAN, Literal(product.ean)))
        self.products.add((p, FOAF.Name, Literal(product.name)))
        self.products.add((p, FOAF.Brand, n.__getattr__('#Brand#' + str(product.brand))))
        self.products.add((p, FOAF.Price, Literal(product.price)))
        self.products.add((p, FOAF.Weight, Literal(product.weight)))
        self.products.add((p, FOAF.Height, Literal(product.height)))
        self.products.add((p, FOAF.Width, Literal(product.width)))
        self.products.add((p, FOAF.Seller, n.__getattr__('#Seller#' + str(product.seller))))
        self.products.serialize(destination='catalog.rdf', format='turtle')
        upload_result.append(Product(product.ean, product.name, Brand(product.brand), product.price,
                                     product.weight, product.height, product.width, SellingCompany(product.seller)))
        return upload_result

    def purchase(self, products, purchaser, priority, payment):
        n = Namespace(Constants.NAMESPACE)
        for ean in products:
            uri = n.__getattr__('#Product#' + str(ean))
            if not (uri, None, None) in self.products:
                return
        soldProducts = []
        for eanP in products:
            query = """SELECT ?x ?ean ?name ?brand ?price ?weight ?height ?width ?seller
            WHERE {{
                ?x ns1:EAN ?ean.
                ?x ns1:Name ?name.
                ?x ns1:Brand ?brand.
                ?x ns1:Price ?price.
                ?x ns1:Weight ?weight.
                ?x ns1:Height ?height.
                ?x ns1:Width ?width.
                ?x ns1:Seller ?seller.
                FILTER  ( {0} )
            }}
            """.format("?ean = " + str(eanP))
            qres = self.products.query(query)
            for p, ean, name, brand, price, weight, height, width, seller in qres:
                n = Namespace(Constants.NAMESPACE)
                uuid_guiones = uuid.uuid4()
                int_uuid = uuid_guiones.int
                bp = n.__getattr__('#BoughtProduct#' + str(int_uuid))
                self.purchases.add((bp, FOAF.Uuid, Literal(int_uuid)))
                self.purchases.add((bp, FOAF.Product, n.__getattr__('#Product#' + str(p))))
                self.purchases.add((bp, FOAF.Purchaser, purchaser.username))
                self.purchases.add((bp, FOAF.SendTo, purchaser.direction))
                self.purchases.add((bp, FOAF.Priority, priority))
                self.purchases.add((bp, FOAF.Payment, payment))
                self.purchases.add((bp, FOAF.DeliveryDate, Literal("undefined")))
                self.purchases.add((bp, FOAF.Sender, Literal("undefined")))
                self.purchases.serialize(destination='purchases.rdf', format='turtle')
                soldProducts.append(BoughtProduct(int_uuid,
                                                  Product(ean, name, Brand(brand), price, weight, height, width,
                                                          SellingCompany(seller)), purchaser, priority, payment,
                                                  "undefined", "undefined"))
        return soldProducts

    def return_prod(self, uuid, user, reason):
        n = Namespace(Constants.NAMESPACE)
        uri = n.__getattr__('#BoughtProduct#' + str(uuid))
        if not (uri, FOAF.Purchaser, user) in self.purchases:
            return build_message(Graph(), FIPAACLPerformatives.REFUSE, Ontologies.RETURN_PRODUCT_MESSAGE).serialize()
        if reason == Constants.REASON_NON_SATISFACTORY:
            for s, p, o in self.purchases.triples(uri, FOAF.DeliveryDate, None):
                delivery_date = datetime.datetime.strptime(o, "%Y-%m-%dT%H:%M:%S.%f")
                if (datetime.datetime.now() - datetime.timedelta(days=15)) < delivery_date:
                    return build_message(Graph(), FIPAACLPerformatives.REFUSE,
                                         Ontologies.RETURN_PRODUCT_MESSAGE).serialize()
        for s, p, o in self.purchases.triples((uri, FOAF.Product, None)):
            self.returns.add((uri, FOAF.Product, Literal(o)))
        self.returns.add((uri, FOAF.Reason, Literal(reason)))
        self.returns.add((uri, FOAF.Purchaser, Literal(user)))
        self.returns.serialize(destination='returns.rdf', format='turtle')
        self.purchases.remove((uri, None, None))
        self.purchases.serialize(destination='purchases.rdf', format='turtle')
        return build_message(Graph(), FIPAACLPerformatives.AGREE, Ontologies.RETURN_PRODUCT_MESSAGE).serialize()

    def sent_products(self, graph):
        for s, p, o in graph.triples((None, FOAF.Uuid, None)):
            for s2, p2, o2 in graph.triples((s, FOAF.DeliveryDate, None)):
                self.purchases.remove((s, FOAF.DeliveryDate, None))
                self.purchases.add((s, FOAF.DeliveryDate, o2))
            for s3, p3, o3 in graph.triples((s, FOAF.Sender, None)):
                self.purchases.remove((s, FOAF.Sender, None))
                self.purchases.add((s, FOAF.Sender, o3))
        self.purchases.serialize(destination='purchases.rdf', format='turtle')
        return self.purchases.serialize()
