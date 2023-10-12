from flask import request
from flask_restful import Resource, reqparse
from micro_search.models.site_data import SiteData,db
from micro_search.crawler import Crawler

import json

SITES=["https://exeami.com", "https://codingotaku.com"]


class Crawl(Resource):
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
