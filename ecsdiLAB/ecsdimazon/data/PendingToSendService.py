import random

import requests
import datetime
from rdflib import Graph, Namespace, Literal
from rdflib.namespace import FOAF

from ecsdiLAB.ecsdimazon.controllers import AgentUtil, Constants
from ecsdiLAB.ecsdimazon.messages import FIPAACLPerformatives, Ontologies


class PendingToSendService:
    PENDING_FILE_NAME = 'pending.rdf'

    PRIORITY_TO_DATE ={
        Constants.PRIORITY_LOW : 10 ,
        Constants.PRIORITY_MEDIUM : 5,
        Constants.PRIORITY_HIGH : 1
    }

    def __init__(self, directory_uri, purchases_uri):
        self.directory_uri = directory_uri + "/comm"
        self.purchases_uri = purchases_uri + "/comm"
        import os
        if not os.path.exists(self.PENDING_FILE_NAME):
            open(self.PENDING_FILE_NAME, 'w')
        self.pending = Graph().parse(self.PENDING_FILE_NAME, format="turtle")

    def send_products(self, graph):
        new_pending = self.pending + graph
        self.pending = new_pending
        self.pending.serialize(destination=self.PENDING_FILE_NAME, format='turtle')
        return AgentUtil.build_message(Graph(), FIPAACLPerformatives.AGREE, Ontologies.SEND_PRODUCTS_MESSAGE)

    def time_to_send(self):
        senders_graph = self.__ask_for_senders__()
        cheapest_sender = self.__negotiate__(senders_graph)
        final_price_message = self.__send_products__(cheapest_sender)
        r = requests.post(self.purchases_uri, AgentUtil.build_message(self.pending, FIPAACLPerformatives.INFORM,
                                                                      Ontologies.SENT_PRODUCTS_MESSAGE).serialize())
        self.pending = Graph()
        self.pending.serialize(destination=self.PENDING_FILE_NAME, format='turtle')
        return final_price_message

    def __ask_for_senders__(self):
        data = AgentUtil.build_message(Graph(), FIPAACLPerformatives.REQUEST, Ontologies.SENDERS_LIST_REQUEST)
        r = requests.post(self.directory_uri, data.serialize())
        return Graph().parse(data=r.text)

    def __negotiate__(self, senders_graph):
        query = """SELECT ?x ?name ?negotiationUri
            WHERE {{
                ?x ns1:Name ?name.
                ?x ns1:NegotiationUri ?negotiationUri.
            }}
            """
        qres = senders_graph.query(query)
        all_senders_with_price = []
        for s, name, negotiation_uri in qres:
            print 'Getting price for {}'.format(name.toPython())
            negotiation_uri = negotiation_uri.toPython() + "/comm"
            r = requests.post(negotiation_uri, data=AgentUtil.build_message(Graph(),
                                                                            FIPAACLPerformatives.REQUEST,
                                                                            Ontologies.SENDERS_PRICE_REQUEST).serialize())
            ppk = AgentUtil.field_of_message(Graph().parse(data=r.text), FOAF.PricePerKilo).toPython()
            print 'Price of {} is {}'.format(name.toPython(), ppk)
            all_senders_with_price.append((s, name, negotiation_uri, ppk))
        if not all_senders_with_price:
            print "ERROR: NO AGENTS REGISTERED IN THE DIRECTORY."
            exit(-1)

        all_senders_with_price_negotiated = []
        min_price = min(map(lambda x: x[3], all_senders_with_price))
        counter_offer_price = min_price - random.uniform(0.1, 1)
        for s, name, negotiation_uri, ppk in all_senders_with_price:
            counter_offer_graph = Graph()
            counter_offer_graph.add((s, FOAF.PricePerKilo, Literal(counter_offer_price)))
            r = requests.post(negotiation_uri, data=AgentUtil.build_message(counter_offer_graph,
                                                                            FIPAACLPerformatives.REQUEST,
                                                                            Ontologies.SENDERS_NEGOTIATION_REQUEST).serialize())
            ng = Graph().parse(data=r.text)
            if AgentUtil.performative_of_message(ng) == FIPAACLPerformatives.AGREE:
                all_senders_with_price_negotiated.append((s, name, negotiation_uri, counter_offer_price))
            else:
                all_senders_with_price_negotiated.append((s, name, negotiation_uri, ppk))

        min_price_negotiated = min(map(lambda x: x[3], all_senders_with_price_negotiated))
        selected_senders = filter(lambda x: x[3] == min_price_negotiated, all_senders_with_price_negotiated)
        if len(selected_senders) == 1:
            return selected_senders[0]
        else:
            return random.choice(selected_senders)

    def __send_products__(self, sender):
        s, name, negotiation_uri, ppk = sender
        ontology = Ontologies.SENDERS_SEND_PRODUCT_REQUEST
        performative = FIPAACLPerformatives.REQUEST
        graph = Graph()
        n = Namespace(Constants.NAMESPACE)
        s = n.__getattr__('#Sender#' + name)
        graph.add((s, FOAF.Weight, Literal(ppk)))
        graph.add((s, FOAF.AgreedPrice, Literal(ppk)))
        r = requests.post(negotiation_uri, data=AgentUtil.build_message(
            graph,
            performative,
            ontology
        ).serialize())
        final_price = AgentUtil.field_of_message(Graph().parse(data=r.text), FOAF.TotalPrice).toPython()
        msg = Graph()
        for s, p ,o in self.pending.triples((None,FOAF.Uuid,None)):
            for s2, p2, o2 in self.pending.triples((s, FOAF.Priority, None)):
                date = datetime.datetime.now() + datetime.timedelta(days=self.PRIORITY_TO_DATE.get(o2.toPython()))
                msg.add((s,FOAF.DeliveryDate,Literal(date)))
            msg.add((s,FOAF.Sender, Literal(name)))

        requests.post(self.purchases_uri,data=AgentUtil.build_message(msg,FIPAACLPerformatives.INFORM, Ontologies.SENT_PRODUCTS_MESSAGE).serialize())
        return "The final price of sending all pending products was {}".format(final_price)
