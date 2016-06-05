from flask import Flask, request
from rdflib import Graph

from ecsdiLAB.ecsdimazon.controllers import AgentUtil
from ecsdiLAB.ecsdimazon.controllers import Constants
from ecsdiLAB.ecsdimazon.data.PendingToSendService import PendingToSendService
from ecsdiLAB.ecsdimazon.messages import Ontologies, FIPAACLPerformatives

app = Flask(__name__)
service = None


@app.route('/comm', methods=['GET', 'POST'])
def comm():
    graph = Graph().parse(data=request.data, format='xml')
    ontology = AgentUtil.ontology_of_message(graph)
    if ontology == Ontologies.SEND_PRODUCTS_MESSAGE:
        return service.send_products(graph).serialize()
    else:
        return AgentUtil.build_message(Graph(), FIPAACLPerformatives.NOT_UNDERSTOOD, Ontologies.UNKNOWN_ONTOLOGY)


@app.route('/itstime', methods=['GET', 'POST', 'PUT'])
def time_to_send():
    return service.time_to_send()


if __name__ == '__main__':
    import sys

    if len(sys.argv) != 3:
        print "USAGE: python ASender {DIRECTORY_URI (with port)} {APURCHASES_URI (with port)}"
        exit(-1)
    service = PendingToSendService(sys.argv[1], sys.argv[2])
    app.run(port=Constants.PORT_ASENDER, debug=True)
