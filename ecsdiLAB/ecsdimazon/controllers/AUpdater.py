import json

from flask import Flask, request

from ecsdiLAB.ecsdimazon.context.ECSDIContext import ECSDIContext
from ecsdiLAB.ecsdimazon.controllers import Constants
from ecsdiLAB.ecsdimazon.model.Product import Product

app = Flask(__name__)

context = ECSDIContext()

@app.route('/catalog/', methods=['POST'])
def new_product_in_catalog():
    product_json = json.loads(request.get_data(as_text=True))
    product_json["seller"] = "seller"
    product = Product.from_json(product_json)
    context.product_service.save(product)
    return json.dumps(product_json)

if __name__ == '__main__':
    app.run(port=Constants.PORT_AUPDATER)