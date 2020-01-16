curl -X PUT "192.31.2.66:9200/location_lookup?pretty" -H 'Content-Type: application/json' -d'
{
    "settings": {
        "analysis": {
            "filter": {
                "autocomplete_filter": {
                    "type": "edge_ngram",
                    "min_gram": "1",
                    "max_gram": "20"
                }
            },
            "analyzer": {
                "autocomplete_analyzer": {
                    "filter": [
                        "lowercase",
                        "autocomplete_filter"
                    ],
                    "tokenizer": "standard"
                },
                "lowercase_analyzer": {
                    "tokenizer": "keyword",
                    "filter": [
                        "lowercase"
                    ]
                }
            }
        }
    },
    "mappings": {
        "location_lookup" : {
            "properties": {
                "keywords": {
                    "type": "text",
                    "fields": {
                        "autocomplete": {
                            "type": "text",
                            "analyzer": "autocomplete_analyzer",
                            "search_analyzer": "standard"
                        },
                        "verbatim": {
                            "type": "keyword"
                        },
                        "lowercase":{
                            "type": "text",
                            "analyzer": "lowercase_analyzer",
                            "search_analyzer": "standard"
                        }
                    }
                },
                "city": {
                    "type": "text",
                    "fields": {
                        "autocomplete": {
                            "type": "text",
                            "analyzer": "autocomplete_analyzer",
                            "search_analyzer": "standard"
                        },
                        "verbatim": {
                            "type": "keyword"
                        }
                    }
                },
                "state": {
                    "type": "text",
                    "fields": {
                        "autocomplete": {
                            "type": "text",
                            "analyzer": "autocomplete_analyzer",
                            "search_analyzer": "standard"
                        },
                        "verbatim": {
                            "type": "keyword"
                        }
                    }
                },
                "stateCode": {
                    "type": "text",
                    "fields": {
                        "autocomplete": {
                            "type": "text",
                            "analyzer": "autocomplete_analyzer",
                            "search_analyzer": "standard"
                        },
                        "verbatim": {
                            "type": "keyword"
                        }
                    }
                },
                "country": {
                    "type": "text",
                    "fields": {
                        "autocomplete": {
                            "type": "text",
                            "analyzer": "autocomplete_analyzer",
                            "search_analyzer": "standard"
                        },
                        "verbatim": {
                            "type": "keyword"
                        }
                    }
                },
                "countryCode": {
                    "type": "text",
                    "fields": {
                        "autocomplete": {
                            "type": "text",
                            "analyzer": "autocomplete_analyzer",
                            "search_analyzer": "standard"
                        },
                        "verbatim": {
                            "type": "keyword"
                        }
                    }
                },
                "continent": {
                    "type": "text",
                    "fields": {
                        "autocomplete": {
                            "type": "text",
                            "analyzer": "autocomplete_analyzer",
                            "search_analyzer": "standard"
                        },
                        "verbatim": {
                            "type": "keyword"
                        }
                    }
                },
                "continentCode": {
                    "type": "text",
                    "fields": {
                        "autocomplete": {
                            "type": "text",
                            "analyzer": "autocomplete_analyzer",
                            "search_analyzer": "standard"
                        },
                        "verbatim": {
                            "type": "keyword"
                        }
                    }
                },
                "zipCode": {
                    "type": "keyword",
                    "fields": {
                        "autocomplete": {
                            "type": "text",
                            "analyzer": "autocomplete_analyzer",
                            "search_analyzer": "standard"
                        }
                    }
                },
                "point": {
                    "type": "geo_point"
                }
            }
        }
    }
}
'