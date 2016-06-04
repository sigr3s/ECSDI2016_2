from flask import Flask, request
from rdflib import Graph

from ecsdiLAB.ecsdimazon.controllers import Constants
from ecsdiLAB.ecsdimazon.controllers.AgentUtil import *
from ecsdiLAB.ecsdimazon.controllers.senders.SenderDirectoryService import SenderDirectoryService
from ecsdiLAB.ecsdimazon.messages import Ontologies, FIPAACLPerformatives

app = Flask(__name__)

service = SenderDirectoryService()


def __execute_routing__(ontology, graph):
    if routings.get(ontology):
        return routings[ontology](graph)
    else:
        return build_message(Graph(), FIPAACLPerformatives.NOT_UNDERSTOOD, Ontologies.UNKNOWN_ONTOLOGY)


@app.route('/comm', methods=['POST', 'GET'])
def comm():
    graph = Graph().parse(data=request.data, format='xml')
    ontology = ontology_of_message(graph)
    __execute_routing__(ontology, graph)


routings = {
    Ontologies.SENDERS_LIST_REQUEST: service.senders_list,
    Ontologies.SENDERS_REGISTER_REQUEST: service.sender_register
}

if __name__ == '__main__':
    app.run(port=Constants.PORT_SENDER_DIRECTORY, debug=True)
