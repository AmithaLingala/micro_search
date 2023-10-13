from flask import request, jsonify
from flask_restful import Resource, reqparse
from models.site_data import db, SearchSiteData, SQL
import json
import re


class Search(Resource):
    def _sanitize(self, content):
        if not content:
          return

        list_of_chars = [',', '""', '.', '+', "'"]
        pattern = '[' +  ''.join(list_of_chars) +  ']'
        return re.sub(pattern, '', content)


    def get(self):
        content = request.args.get('query')
        site = request.args.get('site')

        content = self._sanitize(content)
        
        if content is None or content.strip() == "":
            return jsonify([])        

        if site is None or site.strip() == "":
          site='.'

        query = SearchSiteData.search_bm25('{}'.format(content)).where(SearchSiteData.url.contains(site)).limit(10).dicts()

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
