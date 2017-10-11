import os
from elasticsearch import Elasticsearch

# es_conn = Elasticsearch(hosts=os.environ["ALADDIN_DEMO_ELASTICSEARCH_SERVICE_HOST"])
es_conn = Elasticsearch()
def test_connection():

    es_conn.index(index='posts', doc_type='blog', id=1, body={
        'author': 'Santa Clause',
        'blog': 'Slave Based Shippers of the North',
        'title': 'Using Celery for distributing gift dispatch',
        'topics': ['slave labor', 'elves', 'python',
                   'celery', 'antigravity reindeer'],
        'awesomeness': 0.2
    })

test_connection()
