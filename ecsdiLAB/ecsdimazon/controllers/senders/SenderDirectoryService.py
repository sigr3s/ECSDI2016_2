from rdflib import Graph
from rdflib.namespace import FOAF

from ecsdiLAB.ecsdimazon.controllers import Constants
from ecsdiLAB.ecsdimazon.controllers.AgentUtil import *
from ecsdiLAB.ecsdimazon.messages.FIPAACLPerformatives import *
from ecsdiLAB.ecsdimazon.messages.Ontologies import *
from ecsdiLAB.ecsdimazon.model.Sender import Sender

SENDERS_FILE_NAME = 'senders.rdf'


class SenderDirectoryService:
    def __init__(self):
        import os
        if not os.path.exists(SENDERS_FILE_NAME):
            open('catalog.rdf', 'w')
        self.senders = Graph().parse(SENDERS_FILE_NAME, format='turtle')

    def senders_list(self, graph):  # graph ignored on purpose, not needed
        query = """SELECT ?x ?name ?negotiationUri
            WHERE {{
                ?x ns1:Name ?name.
                ?x ns1:NegotiationUri ?negotiationUri.
            }}
            """
        qres = self.senders.query(query)
        search_res = Graph()
        for s, name, negotiation_uri in qres:
            search_res.add((s, FOAF.Name, name))
            search_res.add((s, FOAF.NegotiationUri, negotiation_uri))
        return build_message(search_res, INFORM, SENDERS_LIST_RESPONSE).serialize()

    def sender_register(self, graph):
        sender = Sender.from_graph(graph)
        n = Namespace(Constants.NAMESPACE)
        s = n.__getattr__('#Sender#' + str(sender.name))
        self.senders.add((s, FOAF.Name, Literal(sender.name)))
        self.senders.add((s, FOAF.NegotiationUri, Literal(sender.negotiation_uri)))
        self.senders.serialize(destination=SENDERS_FILE_NAME, format='turtle')
        return build_message(Graph(), AGREE, SENDERS_REGISTER_RESPONSE).serialize()
