from elasticsearch import Elasticsearch

def test_connection(connection):

    connection.index(index='posts', doc_type='blog', id=1, body={
        'author': 'Santa Clause',
        'blog': 'Slave Based Shippers of the North',
        'title': 'Using Celery for distributing gift dispatch',
        'topics': ['slave labor', 'elves', 'python',
                   'celery', 'antigravity reindeer'],
        'awesomeness': 0.2
    })

es_conn = Elasticsearch(hosts="aladdin-demo-elasticsearch")

test_connection(es_conn)
