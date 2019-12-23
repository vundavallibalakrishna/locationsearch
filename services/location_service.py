
from config.Config import Config

if __name__ == '__main__':
    config = Config.getInstance()
    client = config.getESClient()


def autocomplete(query):
    res = client.search(index="location_lookup", body={
        "size": 1,
        "query": {
            "term": {
                "keywords.autocomplete": query,
                "boost": 1.0
            }
        }
    })
    for hit in res['hits']['hits']:
        print("%(createdOn)s %(title)s: %(jobCode)s" % hit["_source"])


def search(query):
    res = client.search(index="location_lookup", body={
        "query": {
            "match": {
                "message": query
            }
        }
    })
    for hit in res['hits']['hits']:
        print("%(createdOn)s %(title)s: %(jobCode)s" % hit["_source"])
