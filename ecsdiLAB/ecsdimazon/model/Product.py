from rdflib import Graph, Literal

from ecsdiLAB.ecsdimazon.controllers import Constants
from ecsdiLAB.ecsdimazon.model.Brand import Brand
from ecsdiLAB.ecsdimazon.model.SellingCompany import SellingCompany
from rdflib.namespace import RDF, Namespace, OWL, FOAF


class Product:
    def __init__(self, ean, name, brand, price, weight, height, width, seller):
        self.ean = ean
        self.name = name
        self.brand = brand
        self.price = price
        self.weight = weight
        self.height = height
        self.width = width
        self.seller = seller

    def to_rdf_xml(self):
        graph = Graph()
        n = Namespace(Constants.NAMESPACE)
        p = n.__getattr__('#Product#' + str(self.ean))
        graph.add((p, FOAF.EAN, Literal(self.ean)))
        graph.add((p, FOAF.Name, Literal(self.name)))
        graph.add((p, FOAF.Brand, n.__getattr__('#Brand#' + str(self.brand.name))))
        graph.add((p, FOAF.Price, Literal(self.price)))
        graph.add((p, FOAF.Weight, Literal(self.weight)))
        graph.add((p, FOAF.Height, Literal(self.height)))
        graph.add((p, FOAF.Width, Literal(self.width)))
        graph.add((p, FOAF.Seller, n.__getattr__('#Seller#' + str(self.seller.name))))
        return graph.serialize(format='xml')

    @classmethod
    def from_rdf_xml(cls, graph):
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
            }}
        """
        qres = graph.query(query)
        search_res = []
        for p, ean, name, brand, price, weight, height, width, seller in qres:
            search_res.append(Product(ean, name, Brand(brand), price, weight, height, width, SellingCompany(seller)))
        return search_res
