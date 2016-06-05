from flask import Flask, request
from rdflib import Graph

from ecsdiLAB.ecsdimazon.controllers import Constants
from ecsdiLAB.ecsdimazon.controllers.AgentUtil import *
from ecsdiLAB.ecsdimazon.controllers.senders.AgentSender import AgentSender
from ecsdiLAB.ecsdimazon.model.Sender import Sender

app = Flask(__name__)

agent = None


@app.route('/comm', methods=['POST', 'GET'])
def comm():
    graph = Graph().parse(data=request.data, format='xml')
    ontology = ontology_of_message(graph)
    return agent.comm(ontology, graph)


if __name__ == '__main__':
    import sys

    if len(sys.argv) != 3:
        print "USAGE: python AgentSehOorSender {THIS_AGENT_URI} {DIRECTORY_URI}"
        exit(-1)
    if not agent:
        agent = AgentSender(Sender('Oops', sys.argv[1]), sys.argv[2])
    app.run(port=Constants.PORT_OOPS_SENDER, debug=True)
