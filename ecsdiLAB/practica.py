from flask import Flask
import json

app = Flask(__name__)


@app.route('/')
def hello_world():
    return json.dumps({"asdFasd": [{"a":"b"},{"c": "d"}]})


if __name__ == '__main__':
    app.run()
