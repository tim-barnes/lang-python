import os
import uuid
import pytest
import time
import pprint
from copy import deepcopy

from mongoengine import DynamicDocument, DynamicField, connect, UUIDField, Q


class DynDoc(DynamicDocument):
    """
    Extensible document for diamonds
    """
    document_id = UUIDField(unique=True)
    record = DynamicField(required=True)


record_id = uuid.uuid4()

# If we need to normalize
# example_document = {
#     'document_id': record_id,
#     'schema_version': '0.0.5',
#     'datapoints': [
#         {
#             'path': 'header/ID',
#             'value': record_id,
#             'history': [
#                 {
#                     ts: timestamp,
#                     value: record_id
#                 }
#             ]
#         }
#     ]
# }


example_record = {
    'header': {
        'id': record_id
    },
    'data': {
        'simple_field': [1, 2, 3],
        'complex_field': {
            'foo': ['a', 'b'],
            'bar': [{
                'toto': {'coco': 'toto'},
                '__class__': 'ImALittleTeapot'
            },
            {
                'toto': {'coco': 'popo'},
                '__class__': 'ImALittleTeapot'
            }]
        }
    }
}


@pytest.fixture("session")
def mongo_conn():
    # time.sleep(5)
    return connect(host='mongodb://mongo/test',
                   username=os.environ['MONGO_USERNAME'],
                   password=os.environ['MONGO_PASSWORD'],
                   authentication_source='admin')


def __find(id):
    td = DynDoc.objects(document_id=id)
    return td.first()


def store_record(id, record):
    doc = __find(id)
    if doc:
        doc.record = record
    else:
        doc = DynDoc(document_id=id, record=record)

    doc.save()


def get_record(id):
    fetched = __find(id)
    return fetched.record


def len_records():
    return DynDoc.objects().count()


def __q_key(path, op):

    path = path.replace("/", "__")
    path = path.replace(".", "__")

    if op == "=":
        qkey = f"record__{path}"
    else:
        qkey = f"record__{path}__{op}"
    return qkey


def __query(query):
    results = DynDoc.objects(**query)
    for r in results:
        yield r.record


def query_unique(q):

    query = {
        __q_key("unique", "in"): q
    }
    return __query(query)


def query(path, value):
    query = {
        __q_key(path, "="): value
    }
    return __query(query)


def complex_query(tuples):
    parameters = [
        {
            __q_key(path, op): value
        } for path, op, value in tuples
    ]

    query = Q(**parameters[0])
    for p in parameters[1:]:
        query = query & Q(**p)

    results = DynDoc.objects(query)

    for r in results:
        yield r.record



def test_fetching_dynamic_record(mongo_conn):
    store_record(record_id, example_record)
    fetched = get_record(record_id)
    assert example_record == fetched


def test_fetching_empty_doc(mongo_conn):
    id = uuid.uuid4()
    store_record(id, {})
    fetched = get_record(id)

    assert fetched == {}


def test_count_docs(mongo_conn):
    old_len = len_records()

    id = uuid.uuid4()
    store_record(id, example_record)

    assert len_records() == old_len + 1


@pytest.fixture("session")
def unique_record(mongo_conn):
    example_unique = deepcopy(example_record)
    id = uuid.uuid4()
    example_unique['header']['id'] = id
    example_unique['header']['status'] = 'foo'
    example_unique['unique'] = ['x', 'y', 'z']
    example_unique['data']['complex_field']['bar'].append({
        'toto': {'coco': 'nono'},
        '__class__': 'ImALittleTeapot'
    })
    store_record(id, example_unique)

    pprint.pprint(example_unique)
    return example_unique


def test_query_dynamic_unique_field(mongo_conn, unique_record):

    found = [r for r in query_unique(['x'])]
    pprint.pprint(found)

    assert len(found) == 1
    assert found[0] == unique_record

def test_query(mongo_conn, unique_record):
    found = [r for r in query("header/status", 'foo')]
    pprint.pprint(found)

    assert len(found) == 1
    assert found[0] == unique_record


def test_complex_query1(mongo_conn, unique_record):

    found = [r for r in complex_query([
        ("header/status", "=", "foo"),
        # ("unique", "in", ['y'])
    ])]

    pprint.pprint(found)

    assert len(found) == 1
    assert found[0] == unique_record


def test_complex_query2(mongo_conn, unique_record):

    found = [r for r in complex_query([
        ("header/status", "=", "foo"),
        ("unique", "in", ['y'])
    ])]

    pprint.pprint(found)

    assert len(found) == 1
    assert found[0] == unique_record


def test_complex_query3(mongo_conn, unique_record):

    found = [r for r in complex_query([
        ("data/complex_field/foo", "nin", ['c', 'd']),
        ("data/complex_field/bar/toto/coco", "=", 'nono')
    ])]

    pprint.pprint(found)

    assert len(found) == 1
    assert found[0] == unique_record
