from flask import request, jsonify
from flask_restful import Resource, reqparse
from micro_search.models.site_data import SiteData,db
from sqlalchemy.sql import text
import json

class Search(Resource):
  def get(self):
    content = request.args.get('query')
    site= request.args.get('site')

    if content is None:
      return jsonify([])

    site = site if site else ''
    site = "%{0}%".format(site)
    rows = db.session.execute(text("SELECT * FROM site_data_idx WHERE (site_data_idx MATCH :text) AND (url like :site)").params(text=content, site=site)).all()
    results = [tuple(row) for row in rows]
    return jsonify(results)
  
  def delete(self,url):
      row = SiteData.query.filter_by(url=url).first()
      if row:
          db.session.delete(row)
          db.session.commit()
          return {'message':'Deleted'}
      else:
          return {'message': 'url not found'},404
