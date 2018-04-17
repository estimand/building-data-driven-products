from flask import current_app, g
from pydocumentdb import document_client


def get_client():
    if 'client' not in g:
        g.client = document_client.DocumentClient(
            current_app.config['COSMOSDB_ENDPOINT'],
            {'masterKey': current_app.config['COSMOSDB_KEY']}
        )
    return g.client


def get_db():
    client = get_client()
    if 'db' not in g:
        g.db = next(x for x in client.ReadDatabases()
                    if x['id'] == current_app.config['COSMOSDB_DATABASE'])
    return g.db


def get_similarities_collection():
    client = get_client()
    db = get_db()
    if 'similarities_coll' not in g:
        g.similarities_coll = next(x
                                   for x in client.ReadCollections(db['_self'])
                                   if x['id'] == 'similarities')
    client.UpsertUserDefinedFunction(g.similarities_coll['_self'], {
        'id': 'nMostSimilar',
        'body': 'function nMostSimilar(similarities, n=10) {\n'
                '    return similarities.sort((a, b) => b.similarity - a.similarity).slice(0, n);\n'
                '}',
    })
    return g.similarities_coll


def get_talks_collection():
    client = get_client()
    db = get_db()
    if 'talks_coll' not in g:
        g.talks_coll = next(x for x in client.ReadCollections(db['_self'])
                            if x['id'] == 'talks')
    return g.talks_coll


def get_similar_talks(talk_id, n=10):
    client = get_client()
    coll = get_similarities_collection()
    try:
        similarities = {
            x['other_id']: x['similarity']
            for x in next(x for x in client.QueryDocuments(coll['_self'], {
                'query': 'SELECT udf.nMostSimilar(s.similarities, @n) ' \
                         '       AS most_similar ' \
                         'FROM similarities s ' \
                         'WHERE s.id = @id',
                'parameters': [
                    {'name': '@id', 'value': talk_id},
                    {'name': '@n', 'value': n},
                ],
            }))['most_similar']
        }
    except StopIteration:
        return []
    talk_ids = ','.join(['"{}"'.format(x) for x in similarities.keys()])
    talks_info = list(query_talks({
        'query': 'SELECT t.id, t.title ' \
                 'FROM talks t ' \
                 'WHERE t.id IN ({})'.format(talk_ids),
    }))
    for talk in talks_info:
        talk['similarity'] = similarities[talk['id']]
    talks_info.sort(key=lambda x: x['similarity'], reverse=True)
    return talks_info


def query_talks(query):
    client = get_client()
    coll = get_talks_collection()
    return client.QueryDocuments(coll['_self'], query)
