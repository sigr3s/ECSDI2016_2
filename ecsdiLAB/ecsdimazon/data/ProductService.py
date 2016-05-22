from rdflib import Graph, Literal
from rdflib.namespace import RDF, Namespace, OWL, FOAF

from ecsdiLAB.ecsdimazon.controllers import Constants


class ProductService:
    PRODUCT_NAMESPACE = 'http://www.owl-ontologies.com/Ontology1463560793.owl#Product'

    def __init__(self):
        self.products = Graph().parse("/products.rdf", format="turtle")

    def initialize(cls):
        PrE = Namespace("http://www.products.org/ontology/")
        PrEP = Namespace("http://www.products.org/ontology/property/")
        PrER = Namespace("http://www.products.org/ontology/resource/")
        cls.products.bind('prod', PrE)
        cls.products.bind('prodprop', PrEP)
        cls.products.bind('prodres', PrER)
        cls.products.add((PrE.InternalProduct, RDF.type, OWL.Class))

    def search(self, name, price_min, price_max, seller, weight_min, weight_max):
        qres = self.products.query(

        )
        return

    def save(self, product):
        n = Namespace(Constants.NAMESPACE)
        p = n.__getattr__('Product'+product.ean)()
        self.products.add((p, FOAF.EAN, Literal(product.ean)))
        self.products.add((p, FOAF.Name, Literal(product.name)))
        self.products.add((p, FOAF.Brand, n.__getattr__('Brand'+product.brand)()))
        self.products.add((p, FOAF.Price, Literal(product.price)))
        self.products.add((p, FOAF.Weight, Literal(product.weight)))
        self.products.add((p, FOAF.Height, Literal(product.height)))
        self.products.add((p, FOAF.Width, Literal(product.width)))
        self.products.add((p, FOAF.Seller, n.__getattr__('Seller'+product.seller)()))
