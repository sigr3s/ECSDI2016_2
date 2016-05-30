import json

from flask import Flask, request

from ecsdiLAB.ecsdimazon.context.ECSDIContext import ECSDIContext
from ecsdiLAB.ecsdimazon.controllers import Constants
from ecsdiLAB.ecsdimazon.model.Brand import Brand
from ecsdiLAB.ecsdimazon.model.Product import Product
from ecsdiLAB.ecsdimazon.model.SellingCompany import SellingCompany

app = Flask(__name__)

context = ECSDIContext()


@app.route('/')
def list_all_endpoints():
    links = []
    for rule in app.url_map.iter_rules():
        methods = str(rule.methods)
        route = rule.rule
        links.append(methods + " : " + route)
    return json.dumps(links)


@app.route('/products/', methods=['POST'])
def new_product():
    product_json = json.loads(request.get_data(as_text=True))
    product = Product.from_json(product_json)
    context.product_service.save(product)
    return json.dumps(product_json)


if __name__ == '__main__':
    app.run(port=Constants.PORT_AADMIN, debug=True)
