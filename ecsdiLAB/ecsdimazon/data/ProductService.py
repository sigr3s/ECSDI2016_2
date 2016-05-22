from rdflib import Graph
from rdflib.namespace import RDF, RDFS, Namespace, FOAF, OWL



class ProductService:

    def __init__(self):
        self.products = Graph().parse("products.rdf", format="turtle")

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