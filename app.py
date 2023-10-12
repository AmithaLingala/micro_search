from flask import Flask, request
from flask_cors import CORS, cross_origin
from flask_restful import Api, Resource

app = Flask(__name__)
CORS(app)

api = Api(app)

@app.route("/search")
def hello():
    return request.args.get('q')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

