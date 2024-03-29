import uuid

from rdflib import Namespace, Literal
from rdflib.namespace import RDF

ACL = Namespace("http://www.nuin.org/ontology/fipa/acl#")


def build_message(gmess, perf, ontology, sender=None, receiver=None, content=None):
    """
    Construye un mensaje como una performativa FIPA acl
    Asume que en el grafo que se recibe esta ya el contenido y esta ligado al
    URI en el parametro contenido

    :param gmess: grafo RDF sobre el que se deja el mensaje
    :param perf: performativa del mensaje
    :param ontology: ontologia de mensaje
    :param sender: URI del sender
    :param receiver: URI del receiver
    :param content: URI que liga el contenido del mensaje
    :return:
    """

    mssid = 'message-' + str(uuid.uuid4())
    ms = ACL[mssid]
    gmess.bind('acl', ACL)
    gmess.add((ms, RDF.type, ACL.FipaAclMessage))
    gmess.add((ms, ACL.performative, Literal(perf)))
    gmess.add((ms, ACL.sender, Literal(sender)))
    gmess.add((ms, ACL.ontology, Literal(ontology)))
    if receiver is not None:
        gmess.add((ms, ACL.receiver, receiver))
    if content is not None:
        gmess.add((ms, ACL.content, content))
    return gmess


def ontology_of_message(gmess):
    for s, p, o in gmess.triples((None, ACL.ontology, None)):
        return str(o)


def performative_of_message(gmess):
    for s, p, o in gmess.triples((None, ACL.performative, None)):
        return str(o)

def field_of_message(gmess, predicate):
    for s, p, o in gmess.triples((None, predicate, None)):
        return o