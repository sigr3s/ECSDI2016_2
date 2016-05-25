import json

from flask import Flask, request
from ecsdiLAB.ecsdimazon.context.ECSDIContext import ECSDIContext
from ecsdiLAB.ecsdimazon.controllers import Constants


from ecsdiLAB.ecsdimazon.controllers import Constants

app = Flask(__name__)

@app.route('/sender/send', methods=['POST'])
def purchase_products():
    info = json.loads(request.get_data(as_text=True))


if __name__ == '__main__':
    app.run(port=Constants.PORT_ASENDER)