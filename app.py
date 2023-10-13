from flask import Flask, request
from flask_cors import CORS, cross_origin
from flask_restful import Api, Resource
from models.site_data import db, SearchSiteData
from api.search import Search
from api.index import Index
from dotenv import load_dotenv, dotenv_values
import os

load_dotenv()
app = Flask(__name__)
CORS(app)

api = Api(app)

HOST = os.getenv("HOST")
PORT = os.getenv("PORT")


db.connect()
db.create_tables([SearchSiteData])
SearchSiteData.rebuild()
SearchSiteData.optimize()

api.add_resource(Search, '/')
api.add_resource(Index, '/index')

if __name__ == '__main__':
    app.run(host=HOST, port=PORT)
