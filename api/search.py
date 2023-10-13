from flask import request, jsonify
from flask_restful import Resource, reqparse
from models.site_data import db, SearchSiteData, SQL
import json


class Search(Resource):

    def get(self):
        content = request.args.get('query')
        site = request.args.get('site')

        if content is None:
            return jsonify([])

        content = content.replace('"', '""')
        if site is None:
          site='.'
        query = SearchSiteData.search_bm25('"{}"'.format(content)).where(SearchSiteData.url.contains(site)).limit(10).dicts()

        rows=[]
        for row in query:
            rows.append({
              'url': row['url'],
              'title': row['title'],
              'summary': row['summary'],
              'tags': row['tags'],
              'content': row['content']
            })

        return jsonify(rows)

    def delete(self, url):
        row = SiteData.query.filter_by(url=url).first()
        if row:
            db.session.delete(row)
            db.session.commit()
            return {'message': 'Deleted'}
        else:
            return {'message': 'url not found'}, 404
