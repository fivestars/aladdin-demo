import os
from elasticsearch import Elasticsearch

# TODO: Remove once external (aws) script is in place
if os.environ["ELASTICSEARCH_CREATE"] == "true":
    es_conn = Elasticsearch(hosts=os.environ["ELASTICSEARCH_HOST"])
