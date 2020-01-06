
from config.Config import Config

def autocomplete(query):
    config = Config.getInstance()
    client = config.getESClient()
    res = client.search(index="location_lookup", body={
        "size": 1,
        "query": {
         "query_string" : {
                 "query" : query
            }
        }
    })
    for hit in res['hits']['hits']:
        return hit["_source"]


def search(query):
    config = Config.getInstance()
    client = config.getESClient()
    res = client.search(index="location_lookup", body={
        "query": {
            "query_string": {
                "query": query
            }
        }
    })
    for hit in res['hits']['hits']:
       return hit["_source"]
