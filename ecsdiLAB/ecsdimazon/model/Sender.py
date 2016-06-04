class Sender:
    def __init__(self, name, negotiatiotion_uri):
        self.name = name
        self.negotiation_uri = negotiatiotion_uri

    @classmethod
    def from_graph(cls, graph):
        query = """SELECT ?x ?name ?negotiationUri
            WHERE {{
                ?x ns1:Name ?name.
                ?x ns1:negotiationUri ?negotiationUri.
            }}
            """
        qres = graph.query(query)
        for s, name, negotiation_uri in qres:
            return Sender(name, negotiation_uri)  # there will be only 1
