from flask import request
from flask_restful import Resource, reqparse
from models.site_data import SiteData,db
from controller.crawler import Crawler
import os
import json
from dotenv import load_dotenv, dotenv_values

load_dotenv()

SITES=os.getenv('SITES').split(',')


class Index(Resource):
  def put(self):
    rows = []
    for site in SITES:
      print("crawling {0}".format(site))
      crawler = Crawler(site)
      crawler.start()

      data = crawler.start()

      for page_data in data:
        row = SiteData.query.filter_by(url=page_data["url"]).first()
        if row:
            row.title = page_data["title"]
            row.summary = page_data["summary"]
            row.tags = page_data["tags"]
            row.content = page_data["content"]
        else:
            row = SiteData(**page_data)
        rows.append(row)

    db.session.add_all(rows)
    db.session.commit()

    return "Inserted {0} urls".format(len(rows))
