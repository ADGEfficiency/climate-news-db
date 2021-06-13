from shutil import rmtree

from climatedb.config import DBHOME
from climatedb.engines import *

import pytest


@pytest.fixture()
def setup():
    rmtree(DBHOME / 'temp', ignore_errors=True)
    yield
    rmtree(DBHOME / 'temp', ignore_errors=True)


def test_jsonlines(setup):
    payload = [
        {'url': 'line1'},
        {'url': 'line2'},
        {'url': 'line3'},
    ]

    non_payload = [
        {'url': 'line4'},
    ]

    """add data, get all data back"""
    fi = JSONLinesFile("temp/test.data", key='url')

    #  test add
    fi.add(payload)
    data = fi.get()
    assert data == payload

    #  test exists & not exists
    assert fi.exists(payload[0]['url'])
    assert not fi.exists(non_payload[0]['url'])

    #  do add duplicates
    fi.add(payload)
    fi.add(payload)
    data = fi.get()
    assert len(data) == len(payload) * 3


def test_html_fldr(setup):
    db = HTMLFolder('temp', key='id', value='html')

    payload = [
        {'id': '0', 'html': 'content0'},
        {'id': '1', 'html': 'content1'},
        {'id': '2', 'html': 'content2'},
    ]

    #  test add
    db.add(payload)
    data = db.get()

    #  test exists & not exists
    for d in payload:
        assert d in data
        assert db.exists(d['id'])

    assert not db.exists('4')

    #  won't add duplicates - it will rewrite the file


def test_json_fldr(setup):
    db = JSONFolder('temp', key='id')

    payload = [
        {'id': '0', 'html': 'content0'},
        {'id': '1', 'html': 'content1'},
        {'id': '2', 'html': 'content2'},
    ]

    #  test add
    db.add(payload)
    data = db.get()

    #  test exists & not exists
    for d in payload:
        assert d in data
        assert db.exists(d['id'])

    assert not db.exists('4')

    #  won't add duplicates - it will rewrite the file


def test_sqlite():
    schema = [
        ('url', 'TEXT'),
        ('id', 'INT')
    ]

    payload = [
        {'url': 'A', 'id': 1},
        {'url': 'B', 'id': 2},
        {'url': 'C', 'id': 3},
    ]
    #  test add
    db = SQLiteEngine(
        table='test',
        schema=schema,
        index='id',
        db='test'
    )
    db.add(payload)
    data = db.get()
    assert data == payload

    #  test exists & not exists
    for d in payload:
        assert db.exists('id', d['id'])

    assert not db.exists('id', '4')

    #  don't add duplicates
    db.add(payload)
    data = db.get()
    assert len(data) == len(payload)
