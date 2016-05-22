from flask import Flask

from ecsdiLAB.ecsdimazon.controllers import Constants

app = Flask(__name__)

if __name__ == '__main__':
    app.run(port=Constants.PORT_AUPDATER)