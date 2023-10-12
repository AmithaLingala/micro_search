from flask import Flask, request
from flask_cors import CORS, cross_origin
from flask_restful import Api, Resource
from micro_search.models.site_data import db
from micro_search.api.search import Search
from micro_search.api.crawl import Crawl

app = Flask(__name__)
CORS(app)

api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///search.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all() 

api.add_resource(Search,'/search')
api.add_resource(Crawl, '/crawl')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

