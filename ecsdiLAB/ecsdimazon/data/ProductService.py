import json
import uuid

from rdflib import Graph, Literal, URIRef
from rdflib.namespace import RDF, Namespace, OWL, FOAF

from ecsdiLAB.ecsdimazon.controllers import Constants
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
        if not os.path.exists('catalog.rdf'):
            open('catalog.rdf', 'w')
        self.products_in_catalog = Graph().parse("catalog.rdf", format="turtle")
        if not os.path.exists('purchases.rdf'):
            open('purchases.rdf', 'w')
        self.purchases = Graph().parse("purchases.rdf", format="turtle")

    def initialize(cls):
        PrE = Namespace("http://www.products.org/ontology/")
        PrEP = Namespace("http://www.products.org/ontology/property/")
        PrER = Namespace("http://www.products.org/ontology/resource/")
        cls.products.bind('prod', PrE)
        cls.products.bind('prodprop', PrEP)
        cls.products.bind('prodres', PrER)
        cls.products.add((PrE.InternalProduct, RDF.type, OWL.Class))

    def search(self, name, brand, price_min, price_max, ean):
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

    def save(self, product):
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

    def upload_in_catalog(self, product):
        query = """SELECT ?x ?ean
            WHERE {{
                ?x ns1:EAN ?ean.
            }}
            """.format("" if product.ean is None or str(product.ean) == 'None' else "?ean = " + str(product.ean))
        qres = self.products_in_catalog.query(query)
        upload_result = []
        for p, ean in qres:
            if str(ean) == str(product.ean):
                print "Found this ean"
                return upload_result

        n = Namespace(Constants.NAMESPACE)
        p = n.__getattr__('#Product#' + str(product.ean))
        self.products_in_catalog.add((p, FOAF.EAN, Literal(product.ean)))
        self.products_in_catalog.add((p, FOAF.Name, Literal(product.name)))
        self.products_in_catalog.add((p, FOAF.Brand, n.__getattr__('#Brand#' + str(product.brand))))
        self.products_in_catalog.add((p, FOAF.Price, Literal(product.price)))
        self.products_in_catalog.add((p, FOAF.Weight, Literal(product.weight)))
        self.products_in_catalog.add((p, FOAF.Height, Literal(product.height)))
        self.products_in_catalog.add((p, FOAF.Width, Literal(product.width)))
        self.products_in_catalog.add((p, FOAF.Seller, n.__getattr__('#Seller#' + str(product.seller))))
        self.products_in_catalog.serialize(destination='catalog.rdf', format='turtle')
        upload_result.append(Product(product.ean, product.name , Brand(product.brand), product.price,
                                     product.weight, product.height, product.width, SellingCompany(product.seller)))
        return upload_result

    def purchase(self, products, purchaser, priority, payment):
        n = Namespace(Constants.NAMESPACE)
        for ean in products:
            uri = n.__getattr__('#Product#' + str(ean))
            if not (uri, None, None) in self.products:
                return json.dumps(" Error, product is not in the store")
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
                self.purchases.serialize(destination='purchases.rdf', format='turtle')
                soldProducts.append(BoughtProduct(int_uuid,
                                                  Product(ean, name, Brand(brand), price, weight, height, width,
                                                          SellingCompany(seller)), purchaser, priority, payment))
        return soldProducts
