import json

from flask import Flask

from ecsdiLAB.ecsdimazon.controllers import Constants

app = Flask(__name__)


@app.route('/')
def hello_world():
    links = []
    for rule in app.url_map.iter_rules():
        methods = str(rule.methods)
        route = rule.rule
        links.append(methods + " : " + route)
    return json.dumps(links)


if __name__ == '__main__':
    app.run(port=Constants.PORT_APURCHASES)
