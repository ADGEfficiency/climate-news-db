from shutil import rmtree

from climatedb.databases import *

import pytest


@pytest.fixture()
def setup():
    rmtree(DBHOME / 'temp', ignore_errors=True)
    yield
    rmtree(DBHOME / 'temp', ignore_errors=True)


def test_urls_db(setup):
    db = URLs(name='temp/test.jsonl', engine='jsonl', key='url')

    payload = [
        {'url': 'http://1.html', 'time': '2020-01-01'},
        {'url': 'http://2.html', 'time': '2020-01-02'},
        {'url': 'http://3.html', 'time': '2020-01-03'},
    ]

    #  check we don't add duplicates
    db.add(payload)
    db.add(payload)
    data = db.get()
    assert len(data) == 3

    #  check we only get the last record back
    data = db.get(1)
    assert len(data) == 1
    assert data[0] == payload[-1]

    #  check we only get the last two back
    data = db.get(2)
    assert len(data) == 2
    assert data == payload[-2:]


def test_raw_articles_db(setup):
    #  only HTMLFolder as an engine
    db = RawArticles('temp', key='id', value='html')

    payload = [
        {'id': '1', 'time': '2020-01-01', 'html': '<div>1</div>'},
        {'id': '2', 'time': '2020-01-02', 'html': '<div>2</div>'},
        {'id': '3', 'time': '2020-01-03', 'html': '<div>3</div>'},
    ]

    #  check we don't add duplicates
    db.add(payload)
    db.add(payload)
    data = db.get()
    assert len(data) == 3

    #  check we get the correct data back
    for d in payload:
        assert d['html'] == db.get(d['id'])['html']


def test_articles_db():
    for engine in ['sqlite', ]:

        payload = [
            {'id': 1, 'time': '2020-01-01', 'html': '<div>1</div>'},
            {'id': 2, 'time': '2020-01-02', 'html': '<div>2</div>'},
            {'id': 3, 'time': '2020-01-03', 'html': '<div>3</div>'},
        ]

        schema = (
            ('id', 'INT'),
            ('time', 'TEXT'),
            ('html', 'TEXT')
        )

        db = Articles(
            name='test',
            engine=engine,
            key='id',
            schema=schema
        )
        db.add(payload)

        #  test we get everything back
        data = db.get()
        assert data == payload

        #  check we don't add duplicates
        db.add(payload)
        db.add(payload)
        data = db.get()
        assert len(data) == 3

        #  check we get the correct data back
        for d in payload:
            assert d['html'] == db.get(d['id'])['html']
