from flask import request
from flask_restful import Resource, reqparse
from models.site_data import db,SearchSiteData
from controller.crawler import Crawler
import os
import json
from dotenv import load_dotenv, dotenv_values

load_dotenv()

SITES=os.getenv('SITES').split(',')


class Index(Resource):
  def put(self):
    rows_to_insert =[]
    rows_to_replace =[]

    for site in SITES:
      print("crawling {0}".format(site))
      crawler = Crawler(site)
      crawler.start()

      data = crawler.start()

      for page_data in data:
        row = self._insert_or_update({
          'url': page_data['url'],
          'title': page_data['title'],
          'summary': page_data['summary'],
          'tags': page_data['tags'],
          'content': page_data['content'],
        })

        if('rowid' in row):
          rows_to_replace.append(row)
        else:
          rows_to_insert.append(row);
        

    if len(rows_to_replace) > 0:
      SearchSiteData.replace_many(rows_to_replace).execute()

    if len(rows_to_insert) > 0:
      SearchSiteData.insert_many(rows_to_insert).execute()

    return {
      "Inserted": len(rows_to_insert),
      "Replaced": len(rows_to_replace)
    }

  def _insert_or_update(self, row):
    result = SearchSiteData.select().where(SearchSiteData.url == row['url'])

    if result.count() > 0:
      row['rowid'] = result.get().rowid
    return row
