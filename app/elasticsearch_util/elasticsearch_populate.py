from elasticsearch_connection import es_conn

if __name__ == "__main__":
    es_conn.index(index='messages', doc_type='song', id=1, body={
        'author': 'Aladdin',
        'song': 'A Whole New World',
        'lyrics': ['I can show you the world'],
        'awesomeness': 42
    })
