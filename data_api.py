from __future__ import annotations
from string import Template
import requests
import json

class MongoDBDataAPI(object):
  base_url_template = Template('https://data.mongodb-api.com/app/data-$app_id/endpoint/data/beta/action/$action')
  def __init__(self, app_id: str, api_key: str, cluster_name: str) -> MongoDBDataAPI:
      self.app_id = app_id
      self.api_key = api_key
      self.cluster_name = cluster_name
      self.default_db = 'test'
      self.default_collection = __name__
  
  def insert_one(self, doc: dict, *args, **kwargs) -> int:
    db = kwargs.get('id', self.default_db)
    collection = kwargs.get('collection', self.default_collection)
    url = self.base_url_template.safe_substitute(dict(app_id=self.app_id, action='insertOne'))
    payload = json.dumps({
        "collection": collection,
        "database": db,
        "dataSource": self.cluster_name,
        "document": doc
    })
    headers = {"Content-Type": "application/json", "Access-Control-Request-Headers": "*", "api-key": self.api_key}
    print(payload)
    r = requests.post(url, headers=headers, data=payload)
    return r.status_code