import json

from rdflib import Graph, Literal
from flask import Flask, request

from ecsdiLAB.ecsdimazon.context.ECSDIContext import ECSDIContext
from ecsdiLAB.ecsdimazon.controllers import Constants
from ecsdiLAB.ecsdimazon.model.Product import Product

app = Flask(__name__)

context = ECSDIContext()

@app.route('/catalog', methods=['POST'])
def new_product_in_catalog():
    product = Product.from_graph(Graph().parse(data=request.get_data(as_text=True), format='xml'))
    context.product_service.upload_in_catalog(product)
    return json.dumps(product)

if __name__ == '__main__':
    app.run(port=Constants.PORT_AUPDATER,debug=True)